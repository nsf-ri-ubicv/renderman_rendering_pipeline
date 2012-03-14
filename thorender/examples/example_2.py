import itertools
import copy
from math import pi
from collections import OrderedDict

MODEL_CATEGORIES = {'cars' : ['MB26897','MB28855','MB27827','MB28498',
                              'MB28343','MB29642', 'MB31079','MB31620',
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

just_models = [OrderedDict([('model_ids', m),
                  ('use_canonical',USE_CANONICAL),
                  ('generator','renderman'),
                  ('selection','gridded'),
                  ('ty', 0),
                  ('tz', 0),
                  ('s', 1),
                  ('ryz', 0),
                  ('rxy', 0), 
                  ('rxz', 0),
                  ('label', OrderedDict([('invariance', 'base_models'),
                                 ('category', k)])),
                  ('bg_ids', ['gray.tdl'])
               ]) for k, m in MODEL_CATEGORIES.items()]
          
          
just_backgrounds = OrderedDict([('model_ids',[None]),
                    ('num_images', 10 * NUM_IMAGES),
                    ('seed', 0),
                    ('generator','renderman'),
                    ('selection','random'),
                    ('bg_query', OrderedDict([('type','3d hdr')])),
                    ('bg_phi', OrderedDict([('$gt',-pi),('$lt',pi)])),
                    ('bg_psi', OrderedDict([('$gt',-pi),('$lt',pi)])),
                    ('ty', None),
                    ('tz', None),
                    ('s', None), 
                    ('ryz', None),
                    ('rxz', None),
                    ('ryz', None),
                    ('label', OrderedDict([('invariance', 'base_backgrounds'),
                                   ('category', None)])),
                   ])

image_bases = [[
          #translation alone
          OrderedDict([('model_ids', m),
               ('num_images',NUM_IMAGES),
               ('use_canonical',USE_CANONICAL),
               ('generator','renderman'),
               ('selection','random'),
               ('ty',OrderedDict([('$gt',-.6),('$lt',.6)])),
               ('tz',OrderedDict([('$gt',-.6),('$lt',.6)])),
                  ('s', 1),
                  ('ryz', 0),
                  ('rxy', 0), 
                  ('rxz', 0),
               ('label',OrderedDict([('invariance', 'translation'),
                             ('category', k)]))
          ]), 
          #scale alone
          OrderedDict([('model_ids', m),
               ('num_images',NUM_IMAGES),
               ('use_canonical',USE_CANONICAL),
               ('generator','renderman'),
               ('selection','random'),
               ('s',OrderedDict([('$gt',.5),('$lt',2)])),
                  ('ty', 0),
                  ('tz', 0),
                  ('ryz', 0),
                  ('rxy', 0), 
                  ('rxz', 0),
               ('label',OrderedDict([('invariances', ['scale']),
                             ('category', k)]))
          ]),
          #in-plane rotation alone
          OrderedDict([('model_ids', m),
               ('num_images',NUM_IMAGES),
               ('use_canonical',USE_CANONICAL),
               ('generator','renderman'),
               ('selection','random'),
               ('ryz',OrderedDict([('$gt',-pi),('$lt',pi)])),
                  ('ty', 0),
                  ('tz', 0),
                  ('s', 1),
                  ('rxy', 0), 
                  ('rxz', 0),
               ('label',OrderedDict([('invariance', 'inplane_rotation'),
                             ('category', k)]))
          ]),
          #out-of-plane rotation alone
          OrderedDict([('model_ids', m),
               ('num_images',NUM_IMAGES),
               ('use_canonical',USE_CANONICAL),
               ('generator','renderman'),
               ('selection','random'),
               ('rxy',OrderedDict([('$gt',-pi),('$lt',pi)])),
               ('rxz',OrderedDict([('$gt',-pi),('$lt',pi)])),
                  ('ty', 0),
                  ('tz', 0),
                  ('s', 1),
                  ('ryz', 0),
               ('label',OrderedDict([('invariance', 'outplane_rotation'),
                             ('category', k)]))
          ]),
          #level 1
          OrderedDict([('model_ids', m),
               ('num_images',NUM_IMAGES),
               ('use_canonical',USE_CANONICAL),
               ('generator','renderman'),
               ('selection','random'),
               ('ty',OrderedDict([('$gt',-.1),('$lt',.1)])),
               ('tz',OrderedDict([('$gt',-.1),('$lt',.1)])),
               ('s',OrderedDict([('$gt',1/1.1),('$lt',1.1)])),
               ('rxy',OrderedDict([('$gt',-pi/12),('$lt',pi/12)])),
               ('rxz',OrderedDict([('$gt',-pi/12),('$lt',pi/12)])),
               ('ryz',OrderedDict([('$gt',-pi/12),('$lt',pi/12)])),
               ('label',OrderedDict([('invariance', 'level_1'),
                             ('category', k)]))
          ]),
          #level 2
          OrderedDict([('model_ids', m),
               ('num_images',NUM_IMAGES),
               ('use_canonical',USE_CANONICAL),
               ('generator','renderman'),
               ('selection','random'),
               ('ty',OrderedDict([('$gt',-.2),('$lt',.2)])),
               ('tz',OrderedDict([('$gt',-.2),('$lt',.2)])),
               ('s',OrderedDict([('$gt',1/1.2),('$lt',1.2)])),
               ('rxy',OrderedDict([('$gt',-pi/6),('$lt',pi/6)])),
               ('rxz',OrderedDict([('$gt',-pi/6),('$lt',pi/6)])),
               ('ryz',OrderedDict([('$gt',-pi/6),('$lt',pi/6)])),
               ('label',OrderedDict([('invariance', 'level_2'),
                             ('category', k)]))
          ]),
          #level 3
          OrderedDict([('model_ids', m),
               ('num_images',NUM_IMAGES),
               ('use_canonical',USE_CANONICAL),
               ('generator','renderman'),
               ('selection','random'),
               ('ty',OrderedDict([('$gt',-.3),('$lt',.3)])),
               ('tz',OrderedDict([('$gt',-.3),('$lt',.3)])),
               ('s',OrderedDict([('$gt',1/1.3),('$lt',1.3)])),
               ('rxy',OrderedDict([('$gt',-pi/3),('$lt',pi/3)])),
               ('rxz',OrderedDict([('$gt',-pi/3),('$lt',pi/3)])),
               ('ryz',OrderedDict([('$gt',-pi/3),('$lt',pi/3)])),
               ('label',OrderedDict([('invariance', 'level_3'),
                             ('category', k)]))
          ]),
          #level 4
          OrderedDict([('model_ids', m),
               ('num_images',NUM_IMAGES),
               ('use_canonical',USE_CANONICAL),
               ('generator','renderman'),
               ('selection','random'),
               ('ty',OrderedDict([('$gt',-.4),('$lt',.4)])),
               ('tz',OrderedDict([('$gt',-.4),('$lt',.4)])),
               ('s',OrderedDict([('$gt',1/1.4),('$lt',1.4)])),
               ('rxy',OrderedDict([('$gt',-pi/2),('$lt',pi/2)])),
               ('rxz',OrderedDict([('$gt',-pi/2),('$lt',pi/2)])),
               ('ryz',OrderedDict([('$gt',-pi/2),('$lt',pi/2)])),
               ('label',OrderedDict([('invariance', 'level_4'),
                             ('category', k)]))
          ]),
          #level 5
          OrderedDict([('model_ids', m),
               ('num_images',NUM_IMAGES),
               ('use_canonical',USE_CANONICAL),
               ('generator','renderman'),
               ('selection','random'),
               ('ty',OrderedDict([('$gt',-.5),('$lt',.5)])),
               ('tz',OrderedDict([('$gt',-.5),('$lt',.5)])),
               ('s',OrderedDict([('$gt',1/1.5),('$lt',1.5)])),
               ('rxy',OrderedDict([('$gt',-2*pi/3),('$lt',2*pi/3)])),
               ('rxz',OrderedDict([('$gt',-2*pi/3),('$lt',2*pi/3)])),
               ('ryz',OrderedDict([('$gt',-2*pi/3),('$lt',2*pi/3)])),
               ('label',OrderedDict([('invariance', 'level_5'),
                             ('category', k)]))
          ]),
          #level 6
          OrderedDict([('model_ids', m),
               ('num_images',NUM_IMAGES),
               ('use_canonical',USE_CANONICAL),
               ('generator','renderman'),
               ('selection','random'),
               ('ty',OrderedDict([('$gt',-.6),('$lt',.6)])),
               ('tz',OrderedDict([('$gt',-.6),('$lt',.6)])),
               ('s',OrderedDict([('$gt',1/1.6),('$lt',1.6)])),
               ('rxy',OrderedDict([('$gt',-pi),('$lt',pi)])),
               ('rxz',OrderedDict([('$gt',-pi),('$lt',pi)])),
               ('ryz',OrderedDict([('$gt',-pi),('$lt',pi)])),
               ('label',OrderedDict([('invariance', 'level_6'),
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
    mc['seed'] = len(imagesets)
    imagesets.append(mc)
    
#3d hdr backgrounds
for m in image_bases:
    mc = copy.deepcopy(m)
    mc['label']['background'] = '3d_hdr'
    mc['bg_query'] = OrderedDict([('type','3d hdr')])
    mc['bg_phi'] = OrderedDict([('$gt',-pi),('$lt',pi)])
    mc['bg_psi'] = OrderedDict([('$gt',-pi),('$lt',pi)])
    mc['seed'] = len(imagesets)
    imagesets.append(mc)

config = {'images' : imagesets + just_models + [just_backgrounds]
}
