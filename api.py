import os
import json

import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.autoreload
from tornado.options import define, options

import pymongo as pm

define("port", default=8000, help="run on the given port", type=int)


class App(tornado.web.Application):
    def __init__(self,ioloop):
        handlers = [(r"/",img_handler),
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
    

class front_handler(tornado.web.RequestHandler):

    def get(self):
    
        conn = pm.Connection()
        db = conn['dicarlocox_3dmodels']
        coll = db['3ds_test_images']
        

        MB26969_3ds.bmp

class img_handler(tornado.web.RequestHandler):
    
    def get(self):
        args = self.request.arguments
        for k in args.keys():
            args[k] = args[k][0]
        
        tag = args.get('tag')
        
        conn = pm.Connection()
        db = conn['dicarlocox_3dmodels']
        coll = db['3ds_test_images']        
 
        if tag:
                

            
            recs = coll.find({'keywords':tag})
            
            self.write('<html>')
            
            for r in recs:
                #self.write('<img src="' + str(r['filepath']) + '" height="200px"/>')
                path = r['filepath'].split('/')[-1]
                self.write('<img src="http://dicarlocox-3dmodels-images.s3.amazonaws.com/' + str(path) + '" height="200px"/>')
            
            self.write('</html>')
            
        else:
        
            L = coll.distinct('keywords')
            
            self.write('<html>')
            
            for r in L:
                self.write('<a href="/?tag=' + str(r) + '" />' + str(r) + '</a> ') 
            
            self.write('</html>')
        
    
if __name__ == "__main__":
    main()
