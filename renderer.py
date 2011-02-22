import os
import math
import hashlib
import tempfile
import itertools
import cPickle

from string import Template

import numpy as np
import boto

TX_DEFAULT = -2.5
TDELTA_DEFAULT = .1
RDELTA_DEFAULT = math.pi/16
MODEL_DIR = 'MODELS'
BG_DIR = 'BACKGROUNDS'

def get_t(t,r,d,tdefault,ddefault):
    if t is None:
        if r is None:
            t = [tdefault]
        else:
            tmin,tmax = r
            if d is None:
                d = ddefault
            t = np.arange(tmin,tmax,d)
    return t


def params_to_id(p):
    K = p.keys()
    K.sort()
    newp = [(k,p[k]) for k in K]
    return hashlib.sha1(repr(newp)).hexdigest()

def render(out_dir, 
           model_id,
           tx = None,
           ty = None,
           tz = None,
           rxy = None,
           ryz = None,
           rxz = None,
           txrange = None,
           tyrange = None,
           tzrange = None,
           rxyrange = None,
           ryzrange = None,
           rxzrange = None,
           txdelta = None,
           tydelta = None,
           tzdelta = None,
           rxydelta = None,
           rxzdelta = None,
           ryzdelta = None,
           bg_id = None, 
           bg_angle = None,
           kenv = 1,
           ):

    if isinstance(model_id,str):
        model_id = [model_id]
    
    tx = get_t(tx,txrange,txdelta,TX_DEFAULT,TDELTA_DEFAULT)
    ty = get_t(ty,tyrange,tydelta,0,TDELTA_DEFAULT)
    tz = get_t(tz,tzrange,tzdelta,0,TDELTA_DEFAULT)
    rxy = get_t(rxy,rxyrange,rxydelta,0,RDELTA_DEFAULT)
    ryz = get_t(ryz,ryzrange,ryzdelta,0,RDELTA_DEFAULT)
    rxz = get_t(rxz,rxzrange,rxzdelta,0,RDELTA_DEFAULT)
               
    if not isinstance(tx,list):
        tx = [tx]
    if not isinstance(ty,list):
        ty = [ty]
    if not isinstance(tz,list):
        tz = [tz]  
    if not isinstance(rxy,list):
        rxy = [rxy]
    if not isinstance(ryz,list):
        ryz = [ryz]
    if not isinstance(rxz,list):
        rxz = [rxz]     
     
    if not isinstance(kenv,list):
        kenv = [kenv]
           
    param_names = ['model_id','tx','ty','tz','rxy','ryz','rxz','kenv']
    params = [dict(zip(param_names,p)) for p in itertools.product(model_id,tx,ty,tz,rxy,ryz,rxz,kenv)]
        
    conn = boto.connect_s3()
    bbucket = conn.get_bucket('dicarlocox-backgrounds')    
    
    if bg_id is None:
        bg_list = [x.name for x in bbucket.list()]
        R = np.random.randint(len(bg_list),size = (len(params),))
        for (r,p) in zip(R,params):
            p['bg_id'] = bg_list[r]
        
    else:
        if isinstance(bg_id,str):
            bg_id = [bg_id]
        new_params = []
        for p in params:
            for bg in bg_id:
                new_p = p.copy()
                new_p['bg_id'] = bg
                new_params.append(new_p)
        params = new_params
    
    if bg_angle is None:
        #R1 = 2*np.pi*np.random.random(len(params))
        #R2 = 2*np.pi*np.random.random(len(params))
        R1 = [0]*len(params)
        R2 = [0]*len(params)
        for (r1,r2,p) in zip(R1,R2,params):
            p['bg_phi'] = r1
            p['bg_psi'] = r2
    
    else:
        if len(bg_angle) == 2 and isinstance(bg_angle[0],float):
            bg_angle = [bg_angle]
        
        new_params = []
        for p in params:
            for bga in bg_angle:
                new_p = p.copy()
                new_p['bg_phi'] = bga[0]
                new_p['bg_psi'] = bga[1]
                new_params.append(new_p)
        params = new_params       

    bucket = conn.get_bucket('dicarlocox-3dmodels-renderedimages')
    mbucket = conn.get_bucket('dicarlocox-3dmodels-v1')

    tmpl = Template(open('scene.pyt').read())
    
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)
    if not os.path.exists(BG_DIR):
        os.makedirs(BG_DIR)
        
    for p in params:
        s = params_to_id(p)
        k = bucket.get_key(s)
        out_file = os.path.abspath(os.path.join(out_dir,s + '.tif'))
        if k:
            k.get_contents_to_filename(out_file)
        else:
            model_id = p['model_id']
            model_dir =  os.path.join(MODEL_DIR,model_id)
            if not os.path.exists(model_dir):
                get_model(model_id,mbucket) 
                
            bg_id = p['bg_id']
            bg_file = os.path.abspath(os.path.join(BG_DIR,bg_id))
            if not os.path.exists(bg_file):
                k = bbucket.get_key(bg_id)
                k.get_contents_to_filename(bg_file)
                                
            model_dir = os.path.abspath(os.path.join(MODEL_DIR,model_id))
            obj_file = os.path.abspath(os.path.join(model_dir,model_id + '.obj'))
                       
            pdict = {'OBJ':obj_file, 
                     'KENV' : p['kenv'], 
                     'ENVMAP':bg_file,
                     'PHI':p['bg_phi'],
                     'PSI':p['bg_psi'],
                     'TX':p['tx'],
                     'TY':p['ty'],
                     'TZ':p['tz'],
                     'RXY':p['rxy'],
                     'RYZ':p['ryz'],
                     'RXZ':p['rxz'],
                     'OUTFILE': out_file,
                     }
            
            scene = tmpl.substitute(pdict)
            scenepath = os.path.join(model_dir,'scene_' + s + '.py')
            F = open(scenepath,'w')
            F.write(scene)
            F.close()
            
            os.system('cd ' + model_dir + '; render.py -r3delight scene_' + s + '.py')
            
            #k = Key(bucket)
            #k.name = s
            #k.get_contents_from_filename(out_file)
              
        F = open(os.path.join(out_dir,s + '.params'),'w')
        cPickle.dump(p,F)
        F.close()
    
        
                
    
def get_model(model_id,bucket):
    tmpdir = tempfile.mkdtemp()
    k = bucket.get_key(model_id + '.tar.gz')
    k.get_contents_to_filename(os.path.join(tmpdir,model_id + '.zip'))
    os.system('cd ' + tmpdir + '; tar -xzvf ' + model_id + '.zip')
    
    path = os.path.join(tmpdir,'3dmodels',model_id)
    os.system('mv ' + path + ' ' + MODEL_DIR)
    os.system('rm -rf ' + tmpdir)        
            