import os
import math
import hashlib
import tempfile
import itertools
import cPickle

from string import Template

import numpy as np
import boto

MODEL_DIR = 'MODELS'
BG_DIR = 'BACKGROUNDS'

TX_DEFAULT = -2.5
TY_DEFAULT = 0
TZ_DEFAULT = 0
RXY_DEFAULT = 0
RXZ_DEFAULT = 0
RYZ_DEFAULT = 0
BG_ANGLE_DEFAULT = (0,0)
KENV_DEFAULT = 8

def new_val(x):
    if isinstance(x,dict):
        keys = x.keys()
        keys.sort()
        return [(k,new_val(x[k])) for k in keys]
    elif isinstance(x,list):
        return [new_val(y) for y in x]
    elif isinstance(x,tuple):
        return tuple([new_val(y) for y in x])
    else:
        return x
        
    
def params_to_id(p):
    newp = new_val(p)
    return hashlib.sha1(repr(newp)).hexdigest()
    
    
def mtl_fixer(path,model_id,libpath):
    F = open(path).read()
    F = F.replace("C:\\My 3D Models\\" + model_id + "\\\\",libpath)
    F = F.replace("C:\\Program Files\\Autodesk\\3ds Max 2011\\maps\\Backgrounds\\",libpath)
    F = F.replace("C:\\Program Files\\Autodesk\\3ds Max 2011\\maps\\Reflection\\",libpath)
    f = open(path,'w')
    f.write(F)
    f.close()
    
    
def get_model(model_id,bucket):
    tmpdir = tempfile.mkdtemp()
    k = bucket.get_key(model_id + '.tar.gz')
    k.get_contents_to_filename(os.path.join(tmpdir,model_id + '.zip'))
    os.system('cd ' + tmpdir + '; tar -xzvf ' + model_id + '.zip')
    
    path = os.path.join(tmpdir,'3dmodels',model_id)
    os.system('mv ' + path + ' ' + MODEL_DIR)
    os.system('rm -rf ' + tmpdir)        
              

def render_single_image(cache_bucket, 
                        model_bucket, 
                        bbucket,
                        out_dir, 
                        bg_id,
                        model_params,
                        kenv = KENV_DEFAULT,
                        bg_phi = BG_ANGLE_DEFAULT[0],
                        bg_psi = BG_ANGLE_DEFAULT[1]):

    bucket = cache_bucket
    mbucket = model_bucket
    
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)
    if not os.path.exists(BG_DIR):
        os.makedirs(BG_DIR)
            
    for p in model_params:
        assert 'model_id' in p
        p['tx'] = p.get('tx',TX_DEFAULT)
        p['ty'] = p.get('ty',TY_DEFAULT)
        p['tz'] = p.get('tz',TZ_DEFAULT)
        p['rxy'] = p.get('rxy', RXY_DEFAULT)
        p['rxz'] = p.get('rxz', RXZ_DEFAULT)
        p['ryz'] = p.get('ryz', RYZ_DEFAULT)

    params = {'bg_id':bg_id,'bg_phi': bg_phi, 'bg_psi':bg_psi, 'model_params':model_params,'kenv':kenv} 
    ID_STRING = params_to_id(params)
    k = bucket.get_key(ID_STRING)
    out_file = os.path.abspath(os.path.join(out_dir,ID_STRING + '.tif'))
    
    if k:
        k.get_contents_to_filename(out_file)
    else:
        bg_file = os.path.abspath(os.path.join(BG_DIR,bg_id))
        if not os.path.exists(bg_file):
            k = bbucket.get_key(bg_id)
            k.get_contents_to_filename(bg_file) 
            
        for p in model_params:
            model_id = p['model_id']
            model_dir =  os.path.join(MODEL_DIR,model_id)
            if not os.path.exists(model_dir):
                get_model(model_id,mbucket) 
                                
            model_dir = os.path.abspath(os.path.join(MODEL_DIR,model_id))
            obj_file = os.path.abspath(os.path.join(model_dir,model_id + '.obj'))
            mtl_path = os.path.abspath(os.path.join(model_dir,model_id + '.mtl'))   
            mtl_fixer( mtl_path,model_id,model_dir + '/')  
            p['obj_file'] = obj_file

        model_param_string = repr(model_params)
    
        tmpl = Template(open('scene.pyt').read())
                   
        pdict = {'KENV' : kenv, 
                 'ENVMAP':bg_file,
                 'PHI':bg_phi,
                 'PSI':bg_psi,
                 'OUTFILE': out_file,
                 'MODEL_PARAM_STRING': model_param_string
                 }

        make_dir = os.path.abspath(os.path.join(out_dir,'make_dir'))
        os.system('mkdir ' + make_dir)
        
        scene = tmpl.substitute(pdict)
        scenepath = os.path.abspath(os.path.join(make_dir,'scene_' + ID_STRING + '.py'))
        F = open(scenepath,'w')
        F.write(scene)
        F.close()
        print("SCENEPATH",scenepath)
        
        os.system('cd ' + make_dir + '; render.py -r3delight ' + scenepath)
        os.system('rm -rf ' + make_dir)

          
    F = open(os.path.join(out_dir,ID_STRING + '.params'),'w')
    cPickle.dump(params,F)
    F.close()
    

def render(out_dir, params_list,callback=None):

    conn = boto.connect_s3()
    bbucket = conn.get_bucket('dicarlocox-backgrounds')    
    cache_bucket = conn.get_bucket('dicarlocox-3dmodels-renderedimages')
    model_bucket = conn.get_bucket('dicarlocox-3dmodels-v1')    
    bg_list = [x.name for x in bbucket.list()]
    
    for params in params_list:
        params = params.copy();
        bg_id = params.pop('bg_id',bg_list[np.random.randint(len(bg_list))])
        model_params = params.pop('model_params')
        render_single_image(cache_bucket, 
                            model_bucket, 
                            bbucket,
                            out_dir, 
                            bg_id,
                            model_params,
                            **params)
                            
    if callback:
        callback()
        
        
     