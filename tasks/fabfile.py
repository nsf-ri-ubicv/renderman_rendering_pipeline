import pymongo as pm
import gridfs
import time

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

STATE_NEW = 0
STATE_RUNNING = 1
STATE_DONE = 2
STATE_ERROR = 3
POLLING_INTERVAL = 4
SLEEP_LIMIT = 1000


def set_render_tasks(host, port, dbname, colname, key, config_gen_path):
    config_gen = get_config(config_gen_path)
    IC = ImageConfigs(config_gen)
    port = int(port)
    conn = pm.Connection(host, port, document_class=OrderedDict)
    db = conn[dbname]
    coll = db[colname]
    _ids = []
    for c in IC.configs:
        job = OrderedDict([('config', c), ('__key__', key), ('state', STATE_NEW)])
        _id = coll.insert(job, safe=True)
        _ids.append(_id)
    return _ids


def mongo_worker(host, port, dbname, colname, fsname, key):
    port = int(port)
    conn = pm.Connection(host, port, document_class=OrderedDict)
    db = conn[dbname]
    coll = db[colname]
    im_fs = gridfs.GridFS(db, fsname)
    slept = 0
    while True:
        job = coll.find_one({'__key__': key, 'state': STATE_NEW})
        if job:
            config = job['config']
            slept = 0
            coll.update({'_id': job['_id']}, {'$set':{'state': STATE_RUNNING}}, safe=True)
            image_string = renderman_render(config['image'])
            result = OrderedDict([('config', config), ('__key__', key)])
            filename = get_hex_string(result)
            result['filename'] = filename
            im_fs.put(image_string, **result)
            coll.update({'_id': job['_id']}, {'$set':{'state': STATE_DONE}}, safe=True)
        else:
            if slept >= SLEEP_LIMIT:
                break
            else:
                time.sleep(POLLING_INTERVAL)
                slept += POLLING_INTERVAL
