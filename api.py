import os
import json
import tempfile   

import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.autoreload
from tornado.options import define, options

import renderer

try:
    import pymongo as pm
    import pymongo.json_util as json_util
except:
    print("pymongo not installed; frontend functionaliy not available")


define("port", default=9999, help="run on the given port", type=int)


class App(tornado.web.Application):
    """
        Tornado app which serves the API.
    """
    def __init__(self,ioloop):
        handlers = [(r"/3dmodels",ThreeDModelHandler),
                    (r"/backgrounds",BackgroundHandler),
                    (r"/render",RenderHandler),
                    (r"/renderq",QsubRenderHandler),
                    (r"/db/([\S]+)/([\S]+)",DataHandler),
                    (r"/file/([\S]+)/([\S]+)/([\S]+)",FileHandler),
                    (r"/dicarlocox-3dmodels-v1/(.*)",
                                                tornado.web.StaticFileHandler,
                                                {'path':os.path.join(os.path.dirname(__file__), 
                                                "dicarlocox-3dmodels-v1")})
                   ]
        settings = dict(debug=True,io_loop=ioloop)
        tornado.web.Application.__init__(self, handlers, **settings)


def main():
    """
        function which starts up the tornado IO loop and the app. 
    """
    tornado.options.parse_command_line()
    ioloop = tornado.ioloop.IOLoop.instance()
    http_server = tornado.httpserver.HTTPServer(App(ioloop))
    http_server.listen(options.port)
    tornado.autoreload.start()
    ioloop.start()
    


def getQuerySequence(args):  
    """
        simple REST interface for MongoDB.
    """
    querySequence = args.pop('querySequence',None)
    
    if querySequence is None:
        
        querySequence = []

        
        field = args.get('distinct')
        if field:
            action = 'distinct'
        else:
            action = args.get('action','find')
        
        assert action in ['find','find_one','count','distinct']
    
        posargs = ()
        kargs = {}
        if action in ['find','find_one']:
            posargs = (json.loads(args.get('query','{}')),)
            fields = args.get('fields',None)
            if fields:
                kargs['fields'] = json.loads(fields)
        else:
            if args.get('query'):
               d = {'action':'find','args':(json.loads(args['query']),)}
            querySequence.append(d)
        
            if action == 'distinct':
                posargs = (field or args['field'],)
            else:
                posargs = ()
        
        actionDict = {'action' : action}
        if posargs:
            actionDict['args'] = posargs
        if kargs:
            actionDict['kargs'] = kargs
        
        querySequence.append(actionDict)
        
        skip = args.get('skip')
        if skip:
            querySequence.append({'action':'skip','args':(int(skip),)})
        limit = args.get('limit')
        if limit:
            querySequence.append({'action':'limit','args':(int(limit),)})
           
        
    else:
        querySequence = json.loads(querySequence)
        
    for (i,x) in enumerate(querySequence):
        querySequence[i] = (x.get('action'),[x.get('args',()),x.get('kargs',{})])
        
    return querySequence


import gridfs
class FileHandler(tornado.web.RequestHandler):
    def get(self,dbname,fsname,filename):
        connection = pm.Connection()
        db = connection[dbname]
        fs = gridfs.GridFS(db,fsname)
        fh = fs.get_version(filename)
        s = fh.read()

        self.set_header("Content-Type", "x-gzip")
        self.set_header("Content-Disposition", "attachment; filename="+filename)
        self.write(s)
        

class MongoDBHandler(tornado.web.RequestHandler):
    """
        base handler for mongodb access. 
    """
    def get(self,*args):
    
        self.get_connected(*args)

        args = self.request.arguments
        for k in args.keys():
            args[k] = args[k][0]
            
        args = dict([(str(x),y) for (x,y) in args.items()])    
        
        callback = args.pop('callback',None)    
        
        querySequence = getQuerySequence(args)     
        
        c = self.collection       
        for (a,[pos,kw]) in querySequence:
            c = getattr(c,a)(*pos,**kw)    
        if isinstance(c,pm.cursor.Cursor):
            resp = list(c)
        else:
            resp = c
        
        if callback:
            self.write(callback + '(')
        self.write(json.dumps(resp,default = json_util.default))   
        if callback:
            self.write(')')    


class DataHandler(MongoDBHandler):    
    
    def get_connected(self,dbname,colname):
        self.connection = pm.Connection()
        self.db = self.connection[dbname]
        self.collection = self.db[colname]          
    
    
class ThreeDModelHandler(MongoDBHandler):
    """
        DB handler for model DB
        This handler is accessible via get requests on localhost:9999/3dmodels?
    """
    
    def get_connected(self):
        self.connection = pm.Connection()
        self.db = self.connection['dicarlocox_3dmodels']
        self.collection = self.db['3ds_test_images']  
        
        
class BackgroundHandler(MongoDBHandler):
    """
        DB handler for backgrounds DB
        This handler is accessible via get requests on localhost:9999/backgrounds?
    """
    
    def get_connected(self):
        self.connection = pm.Connection()
        self.db = self.connection['dicarlocox_3dmodels']
        self.collection = self.db['3d_spherical_backgrounds'] 
    
  

class RenderHandler(tornado.web.RequestHandler):
    """
        main renderer handler
        
        This handler is accessible via get requests on localhost:9999/render?
        
        
        This API allows you to specify N images to be rendered and returned as a .zip archive
        
        Each image consists of one or more 3d models rendered on an HDR background, with various
        variance parameters set for each model.
        
        
        The basic syntax for these get requests is, to get N images:
        
             params_list=[img_1,img_2, ...., img_N]]
             
         where img_i is a dictionary specifying how to render the ith image.  
         
         Each such dictionary is of the following form:
         
             {"model_params":[{model_spec_1},{model_spec_2}, ..., {model_spec_n}]
              "bg_id" : bg_id_val,
              "bg_phi" : bg_phi_val
              "bg_psi" : bg_psi_val
              "kenv": kenv_val}
        
        where:  
            a) the "model_spec" elements are dictionaries passing parameters 
               specifying how to render each model within the image
            b) the bg_id parameter specifies which background image to choose.  
               Optional -- default is to choose randomly.
            c) bg_phi, bg_psi are the angles within the background image (which is a HDR).
               Optional -- default is  0,0.
            d) kenv is the optional vslue for the background lighting, default is 7.
            
        The "model_spec" format is:
            {"model_id" : model_id,
             "tx" : tx,"ty" : ty, "tz":tz,
             "rxy" : rxy
             &c}
             
        e.g. all the model-related params saying which model to render, and how. 
        
        An example:
        
            http://localhost:9999/render?params_list=[{"model_params":[{"model_id":"MB31635","rxy":3.14}]}]       
             
    """
    
    @tornado.web.asynchronous
    def get(self):
        args = self.request.arguments
        for k in args.keys():
            args[k] = args[k][0]
            try:
                args[k] = json.loads(args[k])
            except:
                pass
            
        params_list = args.pop('params_list')

        self.temp_dir = self.get_tempdir()
        
        self.render(params_list)

    def get_tempdir(self):
        return tempfile.mkdtemp()
        
    def callback(self):
     
        temp_dir = self.temp_dir
        temp_cdir, temp_idir = os.path.split(temp_dir)
        os.system('cd ' + temp_cdir + '; tar -czvf ' + temp_idir + '.tar.gz ' + temp_idir)
        
        self.set_header("Content-Type", "x-gzip")
        self.set_header("Content-Disposition", "attachment; filename="+temp_idir + '.tar.gz')
        outfile = os.path.join(temp_cdir,temp_idir + '.tar.gz')
        self.write(open(outfile).read())
        
        os.system('rm -rf ' + temp_dir)
        
        self.finish()
        
    def render(self,params_list):
        renderer.render(self.temp_dir,params_list,callback=self.callback)

import hashlib
import numpy as np

def random_id():
    return hashlib.sha1(str(np.random.randint(10,size=(32,)))).hexdigest()    


class QsubRenderHandler(RenderHandler):

    def render(self,params_list):
        renderer.render_qsub(self.temp_dir,params_list,callback=self.callback)
        
    def get_tempdir(self):
        d = os.path.join('/home/render/render_wd',random_id())
        os.mkdir(d)
        return d
   
    
if __name__ == "__main__":
    main()
    
    
    
