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

import pymongo as pm

from renderer import render


define("port", default=8000, help="run on the given port", type=int)


class App(tornado.web.Application):
    def __init__(self,ioloop):
        handlers = [(r"/",choose_handler),
                    (r"/choose",choose_handler), 
                    (r"/show",show_handler),
                    (r"/models",model_handler),
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
    tornado.options.parse_command_line()
    ioloop = tornado.ioloop.IOLoop.instance()
    http_server = tornado.httpserver.HTTPServer(App(ioloop))
    http_server.listen(options.port)
    tornado.autoreload.start()
    ioloop.start()
    

class choose_handler(tornado.web.RequestHandler):

    def get(self):
        args = self.request.arguments
        for k in args.keys():
            args[k] = args[k][0]
        
        by = args.get('by','keyword')
        
        if by == 'keyword':
            dist_by = 'keywords'
        else:
            dist_by = 'name'
        
        
        conn = pm.Connection()
        db = conn['dicarlocox_3dmodels']
        coll = db['3ds_test_images']        
          
        L = coll.distinct(dist_by)
        
        self.write('<html>')
        
        if by == 'keyword':
            self.write('<a href="/choose?by=name"/>Choose By Name')
        else:
            self.write('<a href="/choose?by=keyword"/>Choose By Keyword')
            
        for r in L:
            self.write('<a href="/show?' + by + '=' + r + '" />' + r + '</a> ') 
        
        self.write('</html>')
        
            
class show_handler(tornado.web.RequestHandler):

    def get(self):
        args = self.request.arguments
        for k in args.keys():
            args[k] = args[k][0]
        
        val = args.get('keyword')
        if val:
            by = 'keywords'
        else:
            val = args['name']
            by = 'name'

        
        conn = pm.Connection()
        db = conn['dicarlocox_3dmodels']
        coll = db['3ds_test_images']   
        
        recs = coll.find({by:val})
        
        self.write('<html>')
        
        for r in recs:
            path = r['filepath'].split('/')[-1]
            model_id = r['id']
            self.write('<span><img src="http://dicarlocox-3dmodels-images.s3.amazonaws.com/' + str(path) + '" height="200px"/><a href="/render?model_id=' + model_id + '"/>' + model_id + '</a></span>')
        
        self.write('</html>')       
        
        
class model_handler(tornado.web.RequestHandler):
    
    def get(self):
        args = self.request.arguments
        for k in args.keys():
            args[k] = args[k][0]
        
        query = json.loads(args.get('query'))
        
        conn = pm.Connection()
        db = conn['dicarlocox_3dmodels']
        coll = db['3ds_test_images']        
 
        resp = list(coll.find(query))
        self.write(json.dumps(resp))
        
   
class background_handler(tornado.web.RequestHandler):
    
    def get(self):
        args = self.request.arguments
        for k in args.keys():
            args[k] = args[k][0]
        
        query = json.loads(args.get('query'))
        
        conn = pm.Connection()
        db = conn['dicarlocox_3dmodels']
        coll = db['3d_spherical_backgrounds']        
 
        resp = list(coll.find(query))
        self.write(json.dumps(resp))   
        


class render_handler(tornado.web.RequestHandler):

    def get(self):
        args = self.request.arguments
        for k in args.keys():
            args[k] = args[k][0]
            try:
                args[k] = json.loads(args[k])
            except:
                pass
            
        model_id = args.pop('model_id')
        
        #make temp_dir
        
        temp_dir = tempfile.mkdtemp()
        temp_cdir, temp_idir = os.path.split(temp_dir)
        
        render(temp_dir,model_id,**args)
       
        os.system('cd ' + temp_cdir + '; tar -czvf ' + temp_idir + '.tar.gz ' + temp_idir)
        
        self.set_header("Content-Encoding", "gzip")
        self.set_header("Content-Disposition", "attachment; filename="+temp_idir + '.tar.gz')
        outfile = os.path.join(temp_cdir,temp_idir + '.tar.gz')
        self.write(open(outfile).read())
        
        os.system('rm -rf ' + temp_dir)
    
if __name__ == "__main__":
    main()
