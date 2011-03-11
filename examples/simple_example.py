import boto
import renderer


# would be nice if the following stuff were encapsulated in the library
# e.g. ls_models + ls_backgrounds

conn = boto.connect_s3()

bbucket = conn.get_bucket('dicarlocox-backgrounds')    
cache_bucket = conn.get_bucket('dicarlocox-3dmodels-renderedimages')
model_bucket = conn.get_bucket('dicarlocox-3dmodels-v1')

bg_list = [x.name for x in bbucket.list()]
model_list = [x.name for x in model_bucket.list()]
model_id_list = [ x.rstrip('.tar.gz') for x in model_list]


# this is where the 'real' stuff starts

models = []
models.append(  {   'bg_id' : bg_list[0],
                    'model_params' :
                        [ {'model_id' : model_id_list[0]} ]                         
                })

print(models)
                
renderer.render('/tmp', models)
