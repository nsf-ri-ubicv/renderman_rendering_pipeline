import pymongo as pm
import gridfs
from celery.task import task
from celery.task.sets import TaskSet

try:
    from collections import OrderedDict
except ImportError:
    print "Python 2.7+ OrderedDict collection not available"
    try:
        from ordereddict import OrderedDict
        logger.warn("Using backported OrderedDict implementation")
    except ImportError:
        raise ImportError("Backported OrderedDict implementation "
                          "not available. To install it: "
                          "'pip install -vUI ordereddict'")

from thorender.image_generation import renderman_render
from thorender.image_generation import get_hex_string
from thorender.image_generation import get_config
from thorender.image_generation import ImageConfigs



def get_global_connection(host, port):
    CONN = pm.Connection(host, port, document_class=OrderedDict)
    return CONN


@task
def render_task(config, host, port, dbname, colname, key):
    image_string = renderman_render(config['image'])
    conn = get_global_connection(host, port)
    db = conn[dbname]
    im_fs = gridfs.GridFS(db, colname)
    result = OrderedDict([('config', config), ('__key__', key)])
    filename = get_hex_string(result)
    result['filename'] = filename
    im_fs.put(image_string, **result)
    conn.disconnect()
    return filename


def set_render_tasks(host, port, dbname, colname, key, config_gen_path):
    config_gen = get_config(config_gen_path)
    IC = ImageConfigs(config_gen)
    hex_key = key + '_' + get_hex_string(config_gen)
    results = []
    job = TaskSet(tasks=[render_task.subtask((config,
                                       host,
                                       port,
                                       dbname,
                                       colname,
                                       hex_key)) for config in IC.configs])
    results = job.apply_async()

#    for config in IC.configs:
#        result = render_task.delay(config,
#                                   host,
#                                   port,
#                                   dbname,
#                                   colname, 
#                                   hex_key
#                                   )
#        results.append(result)
    return results, hex_key
    
