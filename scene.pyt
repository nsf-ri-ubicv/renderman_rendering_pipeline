import numpy
import cgkit.ri as ri


Globals(
    resolution = (512, 512),
    pixelsamples = (16,16),
    output = "$OUTFILE",
    displaymode = "rgba",
    output_framebuffer = False,
    rib = 'Imager "background"  "string bgtexture" "$ENVMAP"'
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

S = RMShader("envlight",params={"float samples":32,"string envmap":"$ENVMAP","float Kenv":$KENV,"float Kocc":0})
RMLightSource(shader=S)

load("$OBJ")

max_envelope = -numpy.inf
min_envelope = numpy.inf

offset = 0.
scaling = 1.

root = worldObject("")

for part in root.iterChilds():
    if part.geom is not None:
        
        arr = numpy.array(part.geom.verts)
        this_min = arr.min()
        this_max = arr.max()
        
        if this_min < min_envelope:
            min_envelope = this_min
        if this_max > max_envelope:
            max_envelope = this_max

offset = (min_envelope + max_envelope) / 2.
scaling = object_envelope_factor  / ((max_envelope - min_envelope) / 2.)

for part in root.iterChilds():
    if part.geom is not None:        
        
        # rescale the vertices
        print("Rescaling vertices for part %s" % part.name)
        for i in range(len(part.geom.verts)):
            part.geom.verts[i] = (part.geom.verts[i] - offset) * scaling
    
        # rescale the bump map so it isn't crazy        
        print("Rescaling bump map for part %s" % part.name)
        mat = part.getMaterial()
        if mat.map_Bump is not None:
            mat.map_Bump.bumpsize *= scaling


cogs = []
for part in root.iterChilds():
    if part.geom is not None: 
        cogs.append(part.cog)
cogs_mean = numpy.array(cogs).mean(0)
print(cogs_mean)

for part in root.iterChilds():
    if part.geom is not None: 
        part.setOffsetTransform(mat4().translation(cogs_mean).rotate($RYZ,vec3(1,0,0)).rotate($RXZ,vec3(0,1,0)).rotate($RXY,vec3(0,0,1)).translate(vec3($TX,$TY,$TZ)))
        part.transform = mat4().rotation(phi,vec3(0,0,1)).rotate(-psi,vec3(0,1,0))