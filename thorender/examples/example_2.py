import itertools
import copy
from math import pi

from bson import SON

MODEL_CATEGORIES = {'cars' : ['MB26897','MB28855','MB27827','MB28498',
                              'MB28343','MB31083','MB31079','MB31620',
                              'MB28490','MB31095'],

                    'cats_and_dogs' : ['shorthair_cat','leopard',
                                       'lynx','oriental','panther',
                                       'doberman', 'goldenretriever',
                                       'dalmatian', 'bloodhound','bullmastiff'],

                    'reptiles' : ['MB30418','MB29694', 'chameleon',
                                  'crocodile','gecko','iguana','leatherback',
                                  'terapin','tortoise','salamander'],

                    'guns' : ['MB27069','MB27350','MB30684','MB28771',
                              'MB27860','MB29066','MB29726',
                              'MB30472','MB30027','MB30680'],

                    'boats' : ['MB27840','MB27239','MB28586','MB29022','MB28646',
                               'MB29366','MB29346','MB29698',
                               'MB29762','MB31331'],

                    'planes' : ['MB26937','MB27203','MB27211',
                                'MB27463','MB27876','MB27732',
                                'MB27530','MB29650',
                                'MB28651','MB28243'],

                    'faces' : ['face0001','face0002','face0003',
                               'face0005','face0006',
                               'face1','face2','face3',
                               'face5','face6'],

                    'chair' : ['MB29826','MB29342','MB28514','MB27139',
                               'MB27680','MB27675','MB27692',
                               'MB27684','MB27679','MB27696'],

                    'table' : ['MB30374','MB30082','MB28811','MB27386',
                               'MB28462','MB28077','MB28049','MB30386',
                               'MB30926','MB28214'],

                    'plants' : ['MB29862','MB30366','MB28415','MB30422',
                                'MB30150','MB31632','MB30370','MB30114',
                                'MB30762','MB30814'],

                    'buildings' : ['MB27471','MB28886','MB28807',
                                   'MB29870','MB27835','MB31131',
                                   'MB29802', 'MB30810','MB28921',
                                   'MB28934']}
                  
MODELS = list(itertools.chain(*MODEL_CATEGORIES.values()))

NUM_IMAGES = 2
USE_CANONICAL = True

just_models = [SON([('model_ids', m),
                  ('use_canonical',USE_CANONICAL),
                  ('generator','renderman'),
                  ('selection','gridded'),
                  ('ty', 0),
                  ('tz', 0),
                  ('s', 1),
                  ('ryz', 0),
                  ('rxy', 0), 
                  ('rxz', 0),
                  ('label', SON([('invariance', 'base_models'),
                                 ('category', k)])),
                  ('bg_ids', ['gray.tdl'])
               ]) for k, m in MODEL_CATEGORIES.items()]
          
          
just_backgrounds = SON([('model_ids',[None]),
                    ('num_images', 10 * NUM_IMAGES),
                    ('generator','renderman'),
                    ('selection','random'),
                    ('bg_query', SON([('type','3d hdr')])),
                    ('bg_phi', SON([('$gt',-pi),('$lt',pi)])),
                    ('bg_psi', SON([('$gt',-pi),('$lt',pi)])),
                    ('ty', None),
                    ('tz', None),
                    ('s', None), 
                    ('ryz', None),
                    ('rxz', None),
                    ('ryz', None),
                    ('label', SON([('invariance', 'base_backgrounds'),
                                   ('category', None)])),
                   ])

image_bases = [[
          #translation alone
          SON([('model_ids', m),
               ('num_images',NUM_IMAGES),
               ('use_canonical',USE_CANONICAL),
               ('generator','renderman'),
               ('selection','random'),
               ('ty',SON([('$gt',-.6),('$lt',.6)])),
               ('tz',SON([('$gt',-.6),('$lt',.6)])),
                  ('s', 1),
                  ('ryz', 0),
                  ('rxy', 0), 
                  ('rxz', 0),
               ('label',SON([('invariance', 'translation'),
                             ('category', k)]))
          ]), 
          #scale alone
          SON([('model_ids', m),
               ('num_images',NUM_IMAGES),
               ('use_canonical',USE_CANONICAL),
               ('generator','renderman'),
               ('selection','random'),
               ('s',SON([('$gt',.5),('$lt',2)])),
                  ('ty', 0),
                  ('tz', 0),
                  ('ryz', 0),
                  ('rxy', 0), 
                  ('rxz', 0),
               ('label',SON([('invariances', ['scale']),
                             ('category', k)]))
          ]),
          #in-plane rotation alone
          SON([('model_ids', m),
               ('num_images',NUM_IMAGES),
               ('use_canonical',USE_CANONICAL),
               ('generator','renderman'),
               ('selection','random'),
               ('ryz',SON([('$gt',-pi),('$lt',pi)])),
                  ('ty', 0),
                  ('tz', 0),
                  ('s', 1),
                  ('rxy', 0), 
                  ('rxz', 0),
               ('label',SON([('invariance', 'inplane_rotation'),
                             ('category', k)]))
          ]),
          #out-of-plane rotation alone
          SON([('model_ids', m),
               ('num_images',NUM_IMAGES),
               ('use_canonical',USE_CANONICAL),
               ('generator','renderman'),
               ('selection','random'),
               ('rxy',SON([('$gt',-pi),('$lt',pi)])),
               ('rxz',SON([('$gt',-pi),('$lt',pi)])),
                  ('ty', 0),
                  ('tz', 0),
                  ('s', 1),
                  ('ryz', 0),
               ('label',SON([('invariance', 'outplane_rotation'),
                             ('category', k)]))
          ]),
          #level 1
          SON([('model_ids', m),
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
               ('label',SON([('invariance', 'level_1'),
                             ('category', k)]))
          ]),
          #level 2
          SON([('model_ids', m),
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
               ('label',SON([('invariance', 'level_2'),
                             ('category', k)]))
          ]),
          #level 3
          SON([('model_ids', m),
               ('num_images',NUM_IMAGES),
               ('use_canonical',USE_CANONICAL),
               ('generator','renderman'),
               ('selection','random'),
               ('ty',SON([('$gt',-.3),('$lt',.3)])),
               ('tz',SON([('$gt',-.3),('$lt',.3)])),
               ('s',SON([('$gt',1/1.3),('$lt',1.3)])),
               ('rxy',SON([('$gt',-pi/3),('$lt',pi/3)])),
               ('rxz',SON([('$gt',-pi/3),('$lt',pi/3)])),
               ('ryz',SON([('$gt',-pi/3),('$lt',pi/3)])),
               ('label',SON([('invariance', 'level_3'),
                             ('category', k)]))
          ]),
          #level 4
          SON([('model_ids', m),
               ('num_images',NUM_IMAGES),
               ('use_canonical',USE_CANONICAL),
               ('generator','renderman'),
               ('selection','random'),
               ('ty',SON([('$gt',-.4),('$lt',.4)])),
               ('tz',SON([('$gt',-.4),('$lt',.4)])),
               ('s',SON([('$gt',1/1.4),('$lt',1.4)])),
               ('rxy',SON([('$gt',-pi/2),('$lt',pi/2)])),
               ('rxz',SON([('$gt',-pi/2),('$lt',pi/2)])),
               ('ryz',SON([('$gt',-pi/2),('$lt',pi/2)])),
               ('label',SON([('invariance', 'level_4'),
                             ('category', k)]))
          ]),
          #level 5
          SON([('model_ids', m),
               ('num_images',NUM_IMAGES),
               ('use_canonical',USE_CANONICAL),
               ('generator','renderman'),
               ('selection','random'),
               ('ty',SON([('$gt',-.5),('$lt',.5)])),
               ('tz',SON([('$gt',-.5),('$lt',.5)])),
               ('s',SON([('$gt',1/1.5),('$lt',1.5)])),
               ('rxy',SON([('$gt',-2*pi/3),('$lt',2*pi/3)])),
               ('rxz',SON([('$gt',-2*pi/3),('$lt',2*pi/3)])),
               ('ryz',SON([('$gt',-2*pi/3),('$lt',2*pi/3)])),
               ('label',SON([('invariance', 'level_5'),
                             ('category', k)]))
          ]),
          #level 6
          SON([('model_ids', m),
               ('num_images',NUM_IMAGES),
               ('use_canonical',USE_CANONICAL),
               ('generator','renderman'),
               ('selection','random'),
               ('ty',SON([('$gt',-.6),('$lt',.6)])),
               ('tz',SON([('$gt',-.6),('$lt',.6)])),
               ('s',SON([('$gt',1/1.6),('$lt',1.6)])),
               ('rxy',SON([('$gt',-pi),('$lt',pi)])),
               ('rxz',SON([('$gt',-pi),('$lt',pi)])),
               ('ryz',SON([('$gt',-pi),('$lt',pi)])),
               ('label',SON([('invariance', 'level_6'),
                             ('category', k)]))
          ]) 
] for k, m in MODEL_CATEGORIES.items()]

image_bases = list(itertools.chain(*image_bases))

imagesets = []

#gray background
for m in image_bases:
    mc = copy.deepcopy(m)
    mc['label']['background'] = 'gray'
    mc['bg_ids'] = ['gray.tdl']
    imagesets.append(mc)
    
#3d hdr backgrounds
for m in image_bases:
    mc = copy.deepcopy(m)
    mc['label']['background'] = '3d_hdr'
    mc['bg_query'] = SON([('type','3d hdr')])
    mc['bg_phi'] = SON([('$gt',-pi),('$lt',pi)])
    mc['bg_psi'] = SON([('$gt',-pi),('$lt',pi)])
    imagesets.append(mc)

config = {'images' : imagesets + just_models + [just_backgrounds]
}
