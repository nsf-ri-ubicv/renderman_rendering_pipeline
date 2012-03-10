SCENE_SETUP = """
import numpy
import cgkit.ri as ri
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


Globals(
    resolution = ($RES_X, $RES_Y),
    pixelsamples = (16,16),
    output = "$OUTFILE",
    displaymode = "rgba",
    output_framebuffer = False,
    rib = 'Imager "background"  "string bgtexture" "$BACKGROUND"'
)

cos = numpy.cos
sin = numpy.sin

phi = $PHI
psi = $PSI

target_x = cos(phi)*cos(psi)
target_y = sin(phi)*cos(psi)
target_z = sin(psi)


scene_envelope_factor = 2.
object_envelope_factor = 1.

f = scene_envelope_factor
TargetCamera(
    pos    = (0 , 0 , 0),
    target = (target_x,target_y,target_z),
    fstop = 0.3,
    fov = 90.,
)
"""

SCENE_BASE = """
old_parts = []

MODEL_PARAM_LIST = $MODEL_PARAM_STRING
bboxes = []
for params in MODEL_PARAM_LIST:
    
    obj_file = params['obj_file']
    load(obj_file)
    
    max_envelope = -numpy.inf
    min_envelope = numpy.inf
    
    offset = 0.
    scaling = 1.
    
    root = worldObject("")
    
    new_parts = []
    

    for part in root.iterChilds():
        if part not in old_parts and part.geom is not None:
            
            old_parts.append(part)
            new_parts.append(part)
            
            arr = numpy.array(part.geom.verts)
            this_min = arr.min()
            this_max = arr.max()
            
            if this_min < min_envelope:
                min_envelope = this_min
            if this_max > max_envelope:
                max_envelope = this_max
    
    offset = (min_envelope + max_envelope) / 2.
    scaling = object_envelope_factor  / ((max_envelope - min_envelope) / 2.)
    
   
    for part in new_parts:
        if part.geom is not None:        
        
            # rescale the bump map so it isn't crazy        
            print("Rescaling bump map for part %s" % part.name)
            mat = part.getMaterial()
            if mat.map_Bump is not None:
                mat.map_Bump.bumpsize *= scaling
    
    if 'rotations' in params:
        ROTATIONS = params['rotations']
    else:
		ROTATIONS = [{'rxy':params['rxy'],'rxz':params['rxz'],'ryz':params['ryz']}]
    
    TX = params['tx']
    TY = params['ty']
    TZ = params['tz']
    
    SX = params['sx']
    SY = params['sy']
    SZ = params['sz']
    SX = SX*scaling
    SY = SY*scaling
    SZ = SZ*scaling
    
    b1 = map(min,zip(*[part.boundingBox().getBounds()[0] for part in new_parts if part.geom is not None]))
    b2 = map(max,zip(*[part.boundingBox().getBounds()[1] for part in new_parts if part.geom is not None]))
    bbox = [tuple(b1),tuple(b2)]
    bboxes.append(bbox)
    
    DX = (bbox[1][0] + bbox[0][0])/2
    DY = (bbox[1][1] + bbox[0][1])/2
    DZ = (bbox[1][2] + bbox[0][2])/2
    
    for part in new_parts:
        if part.geom is not None: 
            Trans = mat4().translation(vec3(DX,DY,DZ)).scale(vec3(1/SX,1/SY,1/SZ))
            for rot in ROTATIONS:
                Trans.rotate(rot['ryz'],vec3(1,0,0)).rotate(rot['rxz'],vec3(0,1,0)).rotate(rot['rxy'],vec3(0,0,1))
            Trans.translate(vec3(TX,TY,TZ))
            part.setOffsetTransform(Trans)
            part.transform = mat4().rotation(phi,vec3(0,0,1)).rotate(-psi,vec3(0,1,0))
            

"""

SCENE_TEMPLATE = SCENE_SETUP + """
S = RMShader("envlight2",params={"float samples":32,"string envmap":"$ENVMAP","float Kenv":$KENV,"float Kocc":0})
RMLightSource(shader=S)
"""  + SCENE_BASE


SCENE_TEMPLATE_POINT = SCENE_SETUP + """
GLPointLight($POINT_LIGHT_PARAM_STRING)
""" + SCENE_BASE