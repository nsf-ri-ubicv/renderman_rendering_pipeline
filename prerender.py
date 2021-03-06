#!/usr/bin/env python

"""Render tool."""

import sys, os, os.path, optparse, glob, time
from cgkit.ri import *
from cgkit.riutil import *

from math import *
from cgkit.all import *
from cgkit.Interfaces import *
from cgkit.cmds import *
from cgkit.tool import Tool
from cgkit import stitch


renderers = { "aqsis"    : ("aqsis", "aqsl", "teqser"),
              "3delight" : ("renderdl", "shaderdl", "tdlmake"),
              "pixie"    : ("rndr", "sdrc", "texmake"),
              "bmrt"     : ("rendrib", "slc", "mkmip"),
              "prman"    : ("prman", "shader", "txmake"),
              "rdc"      : ("renderdc", "shaderdc", "texdc"),
              "air"      : ("air", "shaded", "mktex") }


# RenderManager
class RenderManager:
    """Process rendering jobs.
    """
    
    def __init__(self):
        """Constructor.
        """
        pass

    # render
    def render(self, renderer, workingdir, rib, tiles=None, outname=None, callback=None):
        """Queue a render job.
        
        renderer: Rendering tool set
        workingdir: Change into this dir before rendering
        rib: The RIB file (relative to workingdir)
        tiles: Tile specification for rendering in tiles
        outname: Output file name
        callback: Gets called when the job is done

        If an image is rendered in tiles the rib file must not contain
        any RiDisplay() calls (unless they only append to the list of
        devices). This is because the output file name has to be modified
        so that there is no name clash for the individual tiles.

        Return value: Job id
        """
        renderer, slcompiler, textool = renderers[renderer]
        # Store the current directory
        prev_dir = os.getcwd()
        # Change to the working directory
        workingdir = os.path.abspath(workingdir)
        os.chdir(workingdir)

        # Render...
        if tiles==None:
            tiles = ((),())
            
        xsplits = [0.0]+list(tiles[0])+[1.0]
        ysplits = [0.0]+list(tiles[1])+[1.0]
        numtiles = (len(xsplits)-1)*(len(ysplits)-1)
        for j in range(len(ysplits)-1):
            for i in range(len(xsplits)-1):
                options = []
                tileout = None
                RiBegin(renderer)
                # Render in tiles? then add the -crop option
                if numtiles>1:
                    x1,x2 = xsplits[i],xsplits[i+1]
                    y1,y2 = ysplits[j],ysplits[j+1]
                    options += ["-crop %s %s %s %s"%(x1,x2,y1,y2)]
                    RiCropWindow(x1,x2,y1,y2)
                    n,e = os.path.splitext(outname)
                    tileout = "%s_%s_%s_%s_%s%s"%(n,x1,x2,y1,y2,e)
                    mode = getScene().getGlobal("displaymode", RI_RGB)
                    RiDisplay(tileout, RI_FILE, mode)
#                cmd = " ".join(["%s"%renderer]+options+["%s"%rib])
#                print cmd
#                sys.stdout.flush()
                # Invoke the renderer
#                os.system(cmd)
                if numtiles>1:
                    n = j*(len(xsplits)-1)+i+1
                    print "Rendering tile %d/%d..."%(n,numtiles)
                    sys.stdout.flush()
                RiReadArchive("main.rib")
                RiEnd()

        # Stitch the tiles...
        if numtiles>1:
            print "Stitching..."
            try:
                stitch.stitch(outname, removetiles=True, infostream=sys.stdout)
            except IOError, e:
                print "ERROR:",e

        # Restore the current directory...
        os.chdir(prev_dir)

        if callback!=None:
            callback()

        return 1



class RenderException(Exception):
    pass

# Render
class Render(Tool):
    """Render tool."""
    
    def __init__(self):
        Tool.__init__(self, defaultoptionvar="RENDER_DEFAULT_OPTIONS")

    def setOptions(self, optparser):
        """Add options specific to this tool."""
        
        Tool.setOptions(self, optparser)
        optparser.add_option("-r", "--renderer", type="string",
                             default="aqsis",
                             help="Renderer to use")
        optparser.add_option("-I", "--include", action="append", default=[],
                             help="Add include path for shader compilation")
        optparser.add_option("-B", "--bake", action="store_true", default=False,
                             help="Bake a texture map")

    def init(self):
        if self.options.renderer not in renderers:
            raise RenderException("Unknown renderer: %s"%self.options.renderer)

    # setOptionsFromGlobals
    def setOptionsFromGlobals(self):
        Tool.setOptionsFromGlobals(self)

        scene = getScene()
        self.options.bake = scene.getGlobal("bake", self.options.bake)

    def action(self):

        scene = getScene()
        timer = scene.timer()

        renderer, slcompiler, textool = renderers[self.options.renderer]
        ribname = "main.rib"
        origoutput = scene.getGlobal("output", "out.tif")

        while 1:
            print 'Exporting %s...'%ribname
            sys.stdout.flush()
            t1 = time.time()
            framenr = int(round(timer.frame))

            # Determine output name
            if self.time_end!=None:
                output = self.appendFrameNr(origoutput, framenr)
            else:
                output = origoutput

            # Determine the model to bake...
            bakemodel = scene.getGlobal("bakemodel", None)
            bakestvar = scene.getGlobal("bakestvar", "st")
            if self.options.bake:
                if bakemodel==None:
                    # Get a list of all trimeshes/polyhedrons
                    meshes = filter(lambda obj: isinstance(obj.geom, TriMeshGeom) or isinstance(obj.geom, PolyhedronGeom), list(scene.walkWorld()))
                    if len(meshes)==1:
                        bakemodel = meshes[0]
                    else:
                        print "Please specify a bake model using the 'bakemodel' global"
                        sys.exit(1)

            # Render in tiles?
            tiles = scene.getGlobal("tiles", None)
            if tiles==None:
                _output = output
            else:
                _output = None

            # Set the resolution
            w = self.options.width
            h = self.options.height
            a = getattr(self.options, "aspect", 1.0)
            scene.setGlobal("resolution", (w,h,a))

            output_framebuffer = scene.getGlobal("output_framebuffer", self.time_end==None)
                  
            # Create RIB & shaders
            save(ribname,
                 camera = self.cam,
                 output = _output,
                 output_framebuffer = output_framebuffer,
                 bake = self.options.bake,
                 bakemodel = bakemodel,
                 bakestvar = bakestvar
                 )

            # Compile shaders
            if os.path.exists("shaders"):
                print "Compiling shaders..."
                sys.stdout.flush()
                oldpath = os.getcwd()
                os.chdir("shaders")
                self.compileSL(slcompiler)
                os.chdir(oldpath)

            t2 = time.time()
            print "Preprocessing time:",self.time2str(t2-t1)

            # Increase time
            if self.time_end==None:
                break
            timer.step()
            if timer.time>self.time_end:
                break

    # appendFrameNr
    def appendFrameNr(self, output, framenr):
        """Append the frame number to all outputs.

        The return value is the same than output except that the file names
        have an appended frame number.
        """
        # No output?
        if output==None:
            return None
        # Is output a string? (i.e. the output file name)
        elif isinstance(output, types.StringTypes):
            return self._appendFrameNr(output, framenr)
        # User specified output specs? (output must already be a list
        # of specs)
        else:
            res = []
            for name,type,mode,params in output:
                name = self._appendFrameNr(name,framenr)
                res.append((name,type,mode,params))
            return res

    # _appendFrameNr
    def _appendFrameNr(self, filename, framenr):
        """Append the frame number to a file name.

        Returns the new file name.
        """
        name, ext = os.path.splitext(filename)
        return "%s%04d%s"%(name, framenr, ext)
        
    # outputName
    def outputName(self, output):
        """Return the output file name.

        output is the 'output' parameter.
        """
        # No output?
        if output==None:
            return ""
        # Is output a string? (i.e. the output file name)
        elif isinstance(output, types.StringTypes):
            return output
        # User specified output specs? (output must already be a list
        # of specs)
        else:
            if len(output)>0:
                return output[0][0]
            else:
                return ""
        

    # compileSL
    def compileSL(self, slcompiler):
        """Compiles all shaders in the current directory."""

        opts = ""
        for p in self.options.include:
            opts+="-I%s"%p
            
        shaders = glob.glob("*.sl")
        for shader in shaders:
            cmd = "%s %s %s"%(slcompiler, opts, shader)
#            print cmd
            os.system(cmd)

    def time2str(self, t):
        if t<60:
            return "%1.0fs"%t
        else:
            min = int(t/60)
            sec = int(t%60)
            if min<60:
                return "%dmin %ds"%(min,sec)
            else:
                h = int(min/60)
                min = int(min%60)
                return "%dh %dmin %ds"%(h,min,sec)
            
        

######################################################################

if __name__=="__main__":
    render = Render()
    try:
        render.run()
    except RenderException, e:
        print e
