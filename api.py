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

try:
    import pymongo as pm
    import pymongo.json_util as json_util
except:
    print("pymongo not installed; frontend functionaliy not available")

from renderer import render


define("port", default=9999, help="run on the given port", type=int)


class App(tornado.web.Application):
    """
        Tornado app which serves the API.
    """
    def __init__(self,ioloop):
        handlers = [(r"/models",model_handler),
                    (r"/backgrounds",background_handler),
                    (r"/render",render_handler),
                    (r"/dicarlocox-3dmodels-v1/(.*)",
                     tornado.web.StaticFileHandler,
                     {'path':os.path.join(os.path.dirname(__file__), "dicarlocox-3dmodels-v1")}
                    )
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
    
        action = args.pop('action','find')
        
        assert action in ['find','find_one','count','distinct']
    
        posargs = ()
        kargs = {}
        if action in ['find','find_one']:
            posargs = (json.loads(args.pop('query','{}')),)
            fields = args.pop('fields',None)
            if fields:
                kargs['fields'] = json.loads(fields)
        elif action == 'distinct':
            posargs = (args.pop('field'),)
        else:
            posargs = ()
        
        actionDict = {'action' : action}
        if posargs:
            actionDict['args'] = posargs
        if kargs:
            actionDict['kargs'] = kargs
            
        querySequence = [actionDict]
    else:
        querySequence = json.loads(querySequence)
        
    for (i,x) in enumerate(querySequence):
        querySequence[i] = (x.get('action'),[x.get('args',()),x.get('kargs',{})])
        
    return querySequence

    
class mongodb_handler(tornado.web.RequestHandler):
    """
        base handler for mongodb access. 
    """
    def get(self):

        args = self.request.arguments
        for k in args.keys():
            args[k] = args[k][0]
            
        args = dict([(str(x),y) for (x,y) in args.items()])    
        
        callback = args.pop('callback',None)    
        
        querySequence = getQuerySequence(args)     
        
        c = self.COLL        
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
    
    
class model_handler(mongodb_handler):
    
    CONN = pm.Connection()
    DB = CONN['dicarlocox_3dmodels']
    COLL = DB['3ds_test_images']  
        
        
class background_handler(tornado.web.RequestHandler):
    
    CONN = pm.Connection()
    DB = CONN['dicarlocox_3dmodels']
    COLL = DB['3d_spherical_backgrounds'] 
    
  

class render_handler(tornado.web.RequestHandler):

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

        self.temp_dir = tempfile.mkdtemp()
        
        render(self.temp_dir,params_list,callback=self.callback)


    def callback(self):
     
        temp_dir = self.temp_dir
        temp_cdir, temp_idir = os.path.split(temp_dir)
        os.system('cd ' + temp_cdir + '; tar -czvf ' + temp_idir + '.tar.gz ' + temp_idir)
        
        self.set_header("Content-Encoding", "gzip")
        self.set_header("Content-Disposition", "attachment; filename="+temp_idir + '.tar.gz')
        outfile = os.path.join(temp_cdir,temp_idir + '.tar.gz')
        self.write(open(outfile).read())
        
        os.system('rm -rf ' + temp_dir)
        
        self.finish()

    
if __name__ == "__main__":
    main()
    
    
    
