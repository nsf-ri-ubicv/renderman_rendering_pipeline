import pymongo as pm
import sqlite3
import os
from starflow.utils import MakeDir
from utils import createCertificate
import boto
from boto.s3.key import Key

# def unzip(depends_on='../dicarlocox-3dmodels-v1-zips/',creates=('../dicarlocox-3dmodels-v1/','../ModelBankLibrary.db')):
#     MakeDir(creates[0])
#     L = os.listdir(depends_on)
#     for l in L:
#         if l.endswith('.tar.gz'):
#             os.system('tar -xzvf ' + depends_on + l + ' -C ' + creates[0])
#             os.system('mv ' + creates[0] + '3dmodels/* ' + creates[0])
#             os.system('rm -rf ' + creates[0] + '3dmodels')
#     os.system('cp ' + depends_on + 'ModelBankLibrary.db ' + '../')
    

def get_modeldb(creates='../ModelBankLibrary.db'):
    conn = boto.connect_s3()
    bucket = conn.get_bucket('dicarlocox-3dmodels-v1')
    k = Key(bucket)
    k.key = 'ModelBankLibrary.bd'
    k.set_contents_to_filename(creates)
    
    
def create_mongodb(depends_on = '../ModelBankLibrary.db', creates = '../certificate.txt'):
    conn = sqlite3.connect('../ModelBankLibrary.db')
    c = conn.cursor()
    c.execute('select * from products;')
    
    conn = pm.Connection()
    db = conn['dicarlocox_3dmodels']
    db.drop_collection('3ds_test_images')
    coll = db['3ds_test_images']
    for rec in c:
        kw = rec[11].split()
        kw = [x for x in kw if x]
        filename = rec[1] + '_3ds.bmp'
        pmrec = {'id':rec[1], 'name':rec[2], 'keywords':kw, 'filepath':filename}
        coll.insert(pmrec)
        
    
    createCertificate(creates,'made it')
    
def make_background_db( creates = '../background_certificate.txt'):

    conn = pm.Connection()
    db = conn['dicarlocox_3dmodels']
    db.drop_collection('3d_spherical_backgrounds')   
    
    coll = db['3d_spherical_backgrounds']
    
    recs = [{'name': 'backlot', 'path':'backlot.tdl'},
     {'name': 'apartment', 'path':'apartment.tdl'},
     {'name': 'empty room', 'path':'empty_room.tdl'},
     {'name': 'office', 'path':'office.tdl'}
     ]
     
    for rec in recs:
        coll.insert(rec)
        