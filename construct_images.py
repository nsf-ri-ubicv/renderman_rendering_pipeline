import pymongo as pm
import sqlite3
import os
from utils import createCertificate
import boto
import tabular
from boto.s3.key import Key

def get_modeldb(creates='../ModelBankLibrary.db'):
    conn = boto.connect_s3()
    bucket = conn.get_bucket('dicarlocox-3dmodels-v1')
    k = Key(bucket)
    k.key = 'ModelBankLibrary.db'
    k.get_contents_to_filename(creates)
    
    
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
        pmrec = {'id':rec[1], 'name':rec[2], 'keywords':kw, 'type':'modelbank','filepath':filename}
        coll.insert(pmrec)
          
    X = tb.tabarray(SVfile = '../model_manifests/faces.csv')
    for x in X:
        rec = {'id':x['ID'],'name':x['ID'],'keywords':['face'],'type':'facegen'}
        coll.insert(pmrec)
    X = tb.tabarray(SVfile = '../model_manifests/dosch_antique_furniture.csv')
    for x in X:
        rec = {'id':x['ID'],'name':x['ID'],'keywords':['furniture','antique'],'type':'dosch'}
        coll.insert(pmrec) 
    X = tb.tabarray(SVfile = '../model_manifests/dosch_cats.csv')
    for x in X:
        rec = {'id':x['ID'],'name':x['ID'],'keywords':['feline','cat','animal'],'type':'dosch'}
        coll.insert(pmrec) 
    X = tb.tabarray(SVfile = '../model_manifests/dosch_clothing_items.csv')
    for x in X:
        rec = {'id':x['ID'],'name':x['ID'],'keywords':['household','clothing accessory'],'type':'dosch'}
        coll.insert(pmrec)
    X = tb.tabarray(SVfile = '../model_manifests/dosch_dogs.csv')
    for x in X:
        rec = {'id':x['ID'],'name':x['ID'],'keywords':['canine','dog','animal'],'type':'dosch'}
        coll.insert(pmrec)       
    X = tb.tabarray(SVfile = '../model_manifests/dosch_mammals.csv')
    for x in X:
        rec = {'id':x['ID'],'name':x['ID'],'keywords':['mammal','animal'],'type':'dosch'}
        coll.insert(pmrec)         
    X = tb.tabarray(SVfile = '../model_manifests/dosch_mens_clothing.csv')
    for x in X:
        rec = {'id':x['ID'],'name':x['ID'],'keywords':['mens clothing','clothing'],'type':'dosch'}
        coll.insert(pmrec)   
    X = tb.tabarray(SVfile = '../model_manifests/dosch_reptiles.csv')
    for x in X:
        rec = {'id':x['ID'],'name':x['ID'],'keywords':['reptile','animal'],'type':'dosch'}
        coll.insert(pmrec) 
    X = tb.tabarray(SVfile = '../model_manifests/dosch_ships.csv')
    for x in X:
        rec = {'id':x['ID'],'name':x['ID'],'keywords':['ship','transportation','boat'],'type':'dosch'}
        coll.insert(pmrec)   
    X = tb.tabarray(SVfile = '../model_manifests/dosch_womens_clothing.csv')
    for x in X:
        rec = {'id':x['ID'],'name':x['ID'],'keywords':['womens clothing','clothing'],'type':'dosch'}
        coll.insert(pmrec)           
        
    createCertificate(creates,'made it')
  
import tabular as tb

def make_background_db( creates = '../background_certificate.txt',depends_on=('../3d_hdr_backgrounds.csv','../2d_grayscale_backgrounds.csv')):

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
        
    X = tb.tabarray(SVfile = depends_on[0])
    recs = [{'name':x['Path'][:-4],'path':x['Path'],'description':x['Description'],'type':'3d hdr'} for x in X]
    for rec in recs:
        coll.insert(rec)
        
        
    X = tb.tabarray(SVfile = depends_on[1])
    recs = [{'name':x['Path'][:-4],'path':x['Path'],'type':'2d grayscale'} for x in X]
    for rec in recs:
        coll.insert(rec)        
        
if __name__ == '__main__':
    if not os.path.exists('Temp'):  
        os.mkdir('Temp')
    os.chdir('Temp')
    get_modeldb()
    create_mongodb()
    #make_background_db()