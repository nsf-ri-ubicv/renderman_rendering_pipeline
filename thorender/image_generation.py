import os
import tempfile
import itertools
import random
import urllib
import json
import hashlib

import numpy as np
import gridfs
import pymongo as pm
from bson import SON

import renderer
from sge_utils import qsub


BASE_URL = 'http://50.19.109.25'
MODEL_URL = BASE_URL + ':9999/3dmodels?'
BG_URL =  BASE_URL + ':9999/backgrounds?'
DB_NAME = 'thor'


def get_config(config_fname):
    config_path = os.path.abspath(config_fname)
    print("Config file:", config_path)
    config = {}
    execfile(config_path, {},config)
    return config['config']
    
    
def get_config_string(configs):
    return hashlib.sha1(repr(configs)).hexdigest()
    
    
def generate_images(im_hash,config_gen, remove=False):
    conn = pm.Connection(document_class = SON)
    db = conn[DB_NAME]
    im_coll = db['images.files']
    im_fs = gridfs.GridFS(db,'images')
    if remove:
        remove_existing(im_coll,im_fs,im_hash)
    IC = ImageConfigs(config_gen)
    for (i,x) in enumerate(IC.configs):
        if (i/100)*100 == i:
            print(i,x)       
        image_string = IC.render_image(x['image'])
        y = SON([('config',x)])
        filename = get_config_string(x)
        y['filename'] = filename
        y['__hash__'] = im_hash
        im_fs.put(image_string,**y)
    return None, IC
    

def generate_and_insert_single_image(x,im_hash):
    conn = pm.Connection(document_class = SON)
    db = conn[DB_NAME]
    im_coll = db['images.files']
    im_fs = gridfs.GridFS(db,'images')
    image_string = render_image(None,x['image']) 
    y = SON([('config',x)])
    filename = get_config_string(x)
    y['filename'] = filename
    y['__hash__'] = im_hash
    im_fs.put(image_string,**y)

   
def generate_images_parallel(im_hash, config_gen, remove=False):
    conn = pm.Connection(document_class = SON)
    db = conn[DB_NAME]
    im_coll = db['images.files']
    im_fs = gridfs.GridFS(db,'images')
    if remove:
        remove_existing(im_coll,im_fs,im_hash)
    IC = ImageConfigs(config_gen)
    jobids = []
    for (i,x) in enumerate(IC.configs):
        jobid = qsub(generate_and_insert_single_image,(x,im_hash),
                     opstring='-pe orte 2 -l qname=rendering.q -o /home/render/image_jobs -e /home/render/image_jobs')  
        jobids.append(jobid)

    return {'child_jobs':jobids}, IC

    
def image_protocol_hash(config_path):
    config = get_config(config_path)
    image_hash = get_config_string(config['images'])
    return image_hash

    
def image_protocol(config_path, write=False, parallel=False):
    config_gen = get_config(config_path) 
    im_hash = image_protocol_hash(config_path)
    if parallel:
        func = generate_images_parallel
    else:
        func = generate_images
    return func(im_hash, config_gen), im_hash


def remove_existing(coll,fs, hash):
    existing = coll.find({'__hash__':hash})
    for e in existing:
        fs.delete(e['_id'])


def render_image(IC,config,returnfh=False):
    generator = config['generator']
    if generator == 'renderman':
        return renderman_render(config,returnfh=returnfh)
    else:
        raise ValueError, 'image generator not recognized'

class ImageConfigs(object):
    def __init__(self,config_gen_spec):
        self.configs = config_gen(self,config_gen_spec)
    
    def render_image(self,config,returnfh = False):
        return render_image(self,config,returnfh = returnfh)
         

def chain(iterables):
    for (ind,it) in enumerate(iterables):
        for element in it:
            yield ind,element

class config_gen(object):
    def __init__(self,IC,config):
        if not isinstance(config['images'],list):
            config['images'] = [config['images']]
        self.im_configs = config['images']
        param_list = []
        for I in config['images']:    
            if I['selection'] == 'specific':
                newparams = specific_config_gen(IC,I)
            elif I['selection'] == 'gridded':
                newparams = gridded_config_gen(IC,I)
            elif I['selection'] == 'random':
                newparams = random_config_gen(IC,I)
            
            param_list.append(newparams)
            
        self.param_list = chain(param_list)

            
    def __iter__(self):
        return self
        
    def next(self):
        ind,x = self.param_list.next()
        x['image']['generator'] = self.im_configs[ind]['generator']
        return x
            
        
def specific_config_gen(IC,config):
    images = config['specs']
    return [SON([('image',m)]) for m in images]  
    
def random_config_gen(IC,config):
    if config['generator'] == 'renderman':
        return renderman_random_config_gen(config)
        
def gridded_config_gen(IC,config):
    if config['generator'] == 'renderman':
        return renderman_config_gen(config)

def renderman_config_gen(args):
    ranger = lambda v : np.arange(args[v]['$gt'],args[v]['$lt'],args['delta']).tolist() if isinstance(v,dict) else [args.get(v)]
    
    tx = ranger('tx')
    ty = ranger('ty')
    tz = ranger('tz')
    rxy = ranger('rxy')
    rxz = ranger('rxz')
    ryz = ranger('ryz')
    sx = ranger('sx')
    sy = ranger('sy')
    sz = ranger('sz')
    kenv = ranger('kenv')
    model_ids = args['model_ids']

    param_names = ['tx','ty','tz','rxy','rxz','ryz','sx','sy','sz','kenv','model_id']
    ranges = [tx,ty,tz,rxy,rxz,ryz,sx,sy,sz,kenv,model_ids]
    params = [SON([('image' , SON(filter(lambda x: x[1] is not None, zip(param_names,p))))]) for p in itertools.product(*ranges)]  


    chooser = lambda v : (lambda : v[random.randint(0,len(v)-1)])    
    random_ranger = lambda v : (((chooser(np.arange(v['$gt'],v['$lt'],v['delta'])) if v.get('delta') else (lambda : (v['$lt'] - v['$gt']) * random.random() + v['$gt'])))  if isinstance(v,dict) else v) if v else None
    
    if 'bg_ids' in args:
        bg_ids = args['bg_ids']
    elif 'bg_query' in args:
        bg_query = args['bg_query']
        bg_ids = json.loads(urllib.urlopen(BG_URL + 'query=' + json.dumps(bg_query) + '&distinct=path').read())
    else:
        bg_ids = None
    funcs = []
    if bg_ids:
        funcs.append(('bg_id',chooser(bg_ids)))
    if 'bg_phi' in args:
        funcs.append(('bg_phi',random_ranger(args['bg_phi'])))
    if 'bg_psi' in args:
        funcs.append(('bg_psi',random_ranger(args['bg_psi'])))
        
        
        
    for param in params:
        p = param['image']
        if args.get('use_canonical'):
            p['use_canonical'] = args['use_canonical']    
        for (k,f) in funcs:
            if f:
                p[k] = f()
        if args.get('res'):
            p['res'] = args['res']
    
    return params
    

def renderman_random_config_gen(args):
    chooser = lambda v : (lambda : v[random.randint(0,len(v)-1)])    
    ranger = lambda v : (((chooser(np.arange(v['$gt'],v['$lt'],v['delta'])) if v.get('delta') else (lambda : (v['$lt'] - v['$gt']) * random.random() + v['$gt'])))  if isinstance(v,dict) else v) if v else None
    num = args['num_images']
    funcs = [(k,ranger(args.get(k))) for k in ['tx','ty','tz','rxy','rxz','ryz','sx','sy','sz','s','bg_phi','bg_psi']]

    if not 'model_ids' in args:
        models = json.loads(urllib.urlopen(MODEL_URL + 'action=distinct&field=id').read())
    else:
        models = args['model_ids']
    funcs1 = [('model_id',chooser(models))]
    if 'bg_ids' in args:
        bg_ids = args['bg_ids']
        funcs1.append(('bg_id',chooser(bg_ids)))
    elif 'bg_query' in args:
        bg_query = args['bg_query']
        bg_ids = json.loads(urllib.urlopen(BG_URL + 'query=' + json.dumps(bg_query) + '&distinct=path').read())
        funcs1.append(('bg_id',chooser(bg_ids)))
        
    if 'kenvs' in args:
        kenvs = args['kenvs']
        funcs1.append(('kenv',chooser(kenvs)))
    
    params = []
    for i in range(num):
        p = SON([])
        if args.get('use_canonical'):
            p['use_canonical'] = args['use_canonical']    
        for (k,f) in funcs + funcs1:
            if f:
                p[k] = f()
        if args.get('res'):
            p['res'] = args['res']

        params.append(SON([('image',p)]))
        
    return params


def get_canonical_view(m):
    v = json.loads(urllib.urlopen(MODEL_URL + 'query={"id":"' + m + '"}&fields=["canonical_view"]').read())[0]
    if v.get('canonical_view'):
        return v['canonical_view']
    
    
def renderman_render(config,returnfh = False):
    config = config.to_dict()
    
    params_list = [{}]
    param = params_list[0]
    if 'bg_id' in config:
        param['bg_id'] = config.pop('bg_id')
    if 'bg_phi' in config:
        param['bg_phi'] = config.pop('bg_phi')
    if 'bg_psi' in config:
        param['bg_phi'] = config.pop('bg_psi')
    if 'kenv' in config:
        param['kenv'] = config.pop('kenv')
    if 'res' in config:
        param['res_x'] = param['res_y'] = config['res']
    use_canonical = config.pop('use_canonical',False)
    if use_canonical:
        v = get_canonical_view(config['model_id'])
        if v:
            config['rotations'] = [{'rxy':v['rxy'],'rxz':v['rxz'],'ryz':v['ryz']},
                                   {'rxy':config.pop('rxy',0),'rxz':config.pop('rxz',0),'ryz':config.pop('ryz',0)}]
    param['model_params'] = [config]   

    orig_dir = os.getcwd()
    os.chdir(os.path.join(os.environ['HOME'] , 'render_wd'))
    tmp = tempfile.mkdtemp()
    renderer.render(tmp,params_list)
    imagefile = [os.path.join(tmp,x) for x in os.listdir(tmp) if x.endswith('.tif')][0]
    os.chdir(orig_dir)
     
    fh = open(imagefile)
    if returnfh:
        return fh
    else:
        return fh.read()



