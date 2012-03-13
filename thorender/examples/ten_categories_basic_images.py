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
          ])
]
import copy

imagesets = []

#3d hdr backgrounds
for m in base_images:
    mc = copy.deepcopy(m)
    mc['bg_query'] = SON([('type','3d hdr')])
    mc['bg_phi'] = SON([('$gt',-pi),('$lt',pi)])
    mc['bg_psi'] = SON([('$gt',-pi),('$lt',pi)])
    imagesets.append(mc)

config = {'images' : imagesets
}
