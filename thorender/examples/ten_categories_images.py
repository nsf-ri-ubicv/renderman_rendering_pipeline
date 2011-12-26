from math import pi

from starflow.utils import ListUnion

from bson import SON
from thorender.model_categories import MODEL_CATEGORIES

MODELS = ListUnion(MODEL_CATEGORIES.values())

NUM_IMAGES = 1000
USE_CANONICAL = True

base_images = [
          #just the images
          SON([('model_ids',MODELS),
               ('use_canonical',USE_CANONICAL),
               ('generator','renderman'),
               ('selection','gridded')
          ]),
          #tz alone
          SON([('model_ids',MODELS),
               ('num_images',NUM_IMAGES),
               ('use_canonical',USE_CANONICAL),
               ('generator','renderman'),
               ('selection','random'),
               ('tz',SON([('$gt',-.6),('$lt',.6)])),
          ]),
          #ty alone
          SON([('model_ids',MODELS),
               ('num_images',NUM_IMAGES),
               ('use_canonical',USE_CANONICAL),
               ('generator','renderman'),
               ('selection','random'),
               ('ty',SON([('$gt',-.6),('$lt',.6)])),
          ]),
          #translation alone
          SON([('model_ids',MODELS),
               ('num_images',NUM_IMAGES),
               ('use_canonical',USE_CANONICAL),
               ('generator','renderman'),
               ('selection','random'),
               ('ty',SON([('$gt',-.6),('$lt',.6)])),
               ('tz',SON([('$gt',-.6),('$lt',.6)])),
          ]), 
          #in-plane rotation alone
          SON([('model_ids',MODELS),
               ('num_images',NUM_IMAGES),
               ('use_canonical',USE_CANONICAL),
               ('generator','renderman'),
               ('selection','random'),
               ('ryz',SON([('$gt',-pi),('$lt',pi)])),
          ]),
          #out-of-plane rotation alone
          SON([('model_ids',MODELS),
               ('num_images',NUM_IMAGES),
               ('use_canonical',USE_CANONICAL),
               ('generator','renderman'),
               ('selection','random'),
               ('rxy',SON([('$gt',-pi/2),('$lt',pi/2)])),
               ('rxz',SON([('$gt',-pi/2),('$lt',pi/2)])),
          ]),
          #all rotation
          SON([('model_ids',MODELS),
               ('num_images',NUM_IMAGES),
               ('use_canonical',USE_CANONICAL),
               ('generator','renderman'),
               ('selection','random'),
               ('rxy',SON([('$gt',-pi/2),('$lt',pi/2)])),
               ('rxz',SON([('$gt',-pi/2),('$lt',pi/2)])),
               ('ryz',SON([('$gt',-pi),('$lt',pi)])),
          ]),
          #scale alone
          SON([('model_ids',MODELS),
               ('num_images',NUM_IMAGES),
               ('use_canonical',USE_CANONICAL),
               ('generator','renderman'),
               ('selection','random'),
               ('s',SON([('$gt',.5),('$lt',2)])),
          ]),
          #translation + inplane rotation
          SON([('model_ids',MODELS),
               ('num_images',NUM_IMAGES),
               ('use_canonical',USE_CANONICAL),
               ('generator','renderman'),
               ('selection','random'),
               ('ty',SON([('$gt',-.6),('$lt',.6)])),
               ('tz',SON([('$gt',-.6),('$lt',.6)])),
               ('ryz',SON([('$gt',-pi),('$lt',pi)])),
          ]),
          #translation + all rotation
          SON([('model_ids',MODELS),
               ('num_images',NUM_IMAGES),
               ('use_canonical',USE_CANONICAL),
               ('generator','renderman'),
               ('selection','random'),
               ('ty',SON([('$gt',-.6),('$lt',.6)])),
               ('tz',SON([('$gt',-.6),('$lt',.6)])),
               ('rxy',SON([('$gt',-pi/2),('$lt',pi/2)])),
               ('rxz',SON([('$gt',-pi/2),('$lt',pi/2)])),
               ('ryz',SON([('$gt',-pi),('$lt',pi)])),
          ]),
          #inplane rotation + scale
          SON([('model_ids',MODELS),
               ('num_images',NUM_IMAGES),
               ('use_canonical',USE_CANONICAL),
               ('generator','renderman'),
               ('selection','random'),
               ('s',SON([('$gt',.5),('$lt',2)])),
               ('ryz',SON([('$gt',-pi),('$lt',pi)])),
          ]),
          #all rotation + scale
          SON([('model_ids',MODELS),
               ('num_images',NUM_IMAGES),
               ('use_canonical',USE_CANONICAL),
               ('generator','renderman'),
               ('selection','random'),
               ('s',SON([('$gt',.5),('$lt',2)])),
               ('rxy',SON([('$gt',-pi/2),('$lt',pi/2)])),
               ('rxz',SON([('$gt',-pi/2),('$lt',pi/2)])),
               ('ryz',SON([('$gt',-pi),('$lt',pi)])),
          ]),
          #translation + inplane rotation + scale 
          SON([('model_ids',MODELS),
               ('num_images',NUM_IMAGES),
               ('use_canonical',USE_CANONICAL),
               ('generator','renderman'),
               ('selection','random'),
               ('ty',SON([('$gt',-.6),('$lt',.6)])),
               ('tz',SON([('$gt',-.6),('$lt',.6)])),
               ('s',SON([('$gt',.5),('$lt',2)])),
               ('ryz',SON([('$gt',-pi),('$lt',pi)])),
          ]),
          #everything 
          SON([('model_ids',MODELS),
               ('num_images',NUM_IMAGES),
               ('use_canonical',USE_CANONICAL),
               ('generator','renderman'),
               ('selection','random'),
               ('ty',SON([('$gt',-.6),('$lt',.6)])),
               ('tz',SON([('$gt',-.6),('$lt',.6)])),
               ('s',SON([('$gt',.5),('$lt',2)])),
               ('rxy',SON([('$gt',-pi/2),('$lt',pi/2)])),
               ('rxz',SON([('$gt',-pi/2),('$lt',pi/2)])),
               ('ryz',SON([('$gt',-pi),('$lt',pi)])),
          ]),
          #level 1
          SON([('model_ids',MODELS),
               ('num_images',NUM_IMAGES),
               ('use_canonical',USE_CANONICAL),
               ('generator','renderman'),
               ('selection','random'),
               ('ty',SON([('$gt',-.1),('$lt',.1)])),
               ('tz',SON([('$gt',-.1),('$lt',.1)])),
               ('s',SON([('$gt',1/1.1),('$lt',1.1)])),
               ('rxy',SON([('$gt',-pi/12),('$lt',pi/12)])),
               ('rxz',SON([('$gt',-pi/12),('$lt',pi/12)])),
               ('ryz',SON([('$gt',-pi/12),('$lt',pi/12)])),
          ]),
          #level 2
          SON([('model_ids',MODELS),
               ('num_images',NUM_IMAGES),
               ('use_canonical',USE_CANONICAL),
               ('generator','renderman'),
               ('selection','random'),
               ('ty',SON([('$gt',-.2),('$lt',.2)])),
               ('tz',SON([('$gt',-.2),('$lt',.2)])),
               ('s',SON([('$gt',1/1.2),('$lt',1.2)])),
               ('rxy',SON([('$gt',-pi/6),('$lt',pi/6)])),
               ('rxz',SON([('$gt',-pi/6),('$lt',pi/6)])),
               ('ryz',SON([('$gt',-pi/6),('$lt',pi/6)])),
          ]),
          #level 3
          SON([('model_ids',MODELS),
               ('num_images',NUM_IMAGES),
               ('use_canonical',USE_CANONICAL),
               ('generator','renderman'),
               ('selection','random'),
               ('ty',SON([('$gt',-.3),('$lt',.3)])),
               ('tz',SON([('$gt',-.3),('$lt',.3)])),
               ('s',SON([('$gt',1/1.3),('$lt',1.3)])),
               ('rxy',SON([('$gt',-pi/4),('$lt',pi/4)])),
               ('rxz',SON([('$gt',-pi/4),('$lt',pi/4)])),
               ('ryz',SON([('$gt',-pi/4),('$lt',pi/4)])),
          ]),
          #level 4
          SON([('model_ids',MODELS),
               ('num_images',NUM_IMAGES),
               ('use_canonical',USE_CANONICAL),
               ('generator','renderman'),
               ('selection','random'),
               ('ty',SON([('$gt',-.4),('$lt',.4)])),
               ('tz',SON([('$gt',-.4),('$lt',.4)])),
               ('s',SON([('$gt',1/1.4),('$lt',1.4)])),
               ('rxy',SON([('$gt',-pi/3),('$lt',pi/3)])),
               ('rxz',SON([('$gt',-pi/3),('$lt',pi/3)])),
               ('ryz',SON([('$gt',-pi/3),('$lt',pi/3)])),
          ]),
          #level 5
          SON([('model_ids',MODELS),
               ('num_images',NUM_IMAGES),
               ('use_canonical',USE_CANONICAL),
               ('generator','renderman'),
               ('selection','random'),
               ('ty',SON([('$gt',-.5),('$lt',.5)])),
               ('tz',SON([('$gt',-.5),('$lt',.5)])),
               ('s',SON([('$gt',1/1.5),('$lt',1.5)])),
               ('rxy',SON([('$gt',-5*pi/12),('$lt',5*pi/12)])),
               ('rxz',SON([('$gt',-5*pi/12),('$lt',5*pi/12)])),
               ('ryz',SON([('$gt',-5*pi/12),('$lt',5*pi/12)])),
          ]),
          #level 6
          SON([('model_ids',MODELS),
               ('num_images',NUM_IMAGES),
               ('use_canonical',USE_CANONICAL),
               ('generator','renderman'),
               ('selection','random'),
               ('ty',SON([('$gt',-.6),('$lt',.6)])),
               ('tz',SON([('$gt',-.6),('$lt',.6)])),
               ('s',SON([('$gt',1/1.6),('$lt',1.6)])),
               ('rxy',SON([('$gt',-pi/2),('$lt',pi/2)])),
               ('rxz',SON([('$gt',-pi/2),('$lt',pi/2)])),
               ('ryz',SON([('$gt',-pi/2),('$lt',pi/2)])),
          ])
]
import copy

imagesets = []

#gray background
for m in base_images:
    mc = copy.deepcopy(m)
    mc['bg_ids'] = ['gray.tdl']
    imagesets.append(mc)
    
#3d hdr backgrounds
for m in base_images:
    mc = copy.deepcopy(m)
    mc['bg_query'] = SON([('type','3d hdr')])
    mc['bg_phi'] = SON([('$gt',-pi),('$lt',pi)])
    mc['bg_psi'] = SON([('$gt',-pi),('$lt',pi)])
    imagesets.append(mc)

config = {'images' : imagesets
}
