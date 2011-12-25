import subprocess
import re
import tempfile
import cPickle
import string
import os
import hashlib

def callfunc(fn,argfile):
    args = cPickle.loads(open(argfile).read())
    
    if isinstance(args,list):
        pos_args = args[0]
        kwargs = args[1]
    elif isinstance(args,dict):
        pos_args = ()
        kwargs = args
    else:
        pos_args = args
        kwargs = {}

    os.remove(argfile)    
    fn(*pos_args,**kwargs)
    
SGE_SUBMIT_PATTERN = re.compile("Your job ([\d]+) ")

import random

def get_temp_file():

    random.seed()
    hash = "%016x" % random.getrandbits(128)
    filename = os.path.join(os.environ['HOME'] , 'qsub_tmp',"qsub_" + hash)
    return open(filename,'w')

def qsub(fn,args,opstring='', python_executable='python'):

    module_name = fn.__module__
    fnname = fn.__name__
    
    f = get_temp_file()
    argfile = f.name
    cPickle.dump(args,f)
    f.close()

    f = get_temp_file()
    scriptfile = f.name
    call_script = string.Template(call_script_template).substitute({'MODNAME':module_name,
                                                         'FNNAME':fnname,
                                                         'ARGFILE':argfile,
                                                         'PYEXEC':python_executable})
    f.write(call_script)
    f.close()
    
    p = subprocess.Popen('qsub ' + opstring + ' ' + scriptfile,shell=True,stdout=subprocess.PIPE)
    sts = os.waitpid(p.pid,0)[1]

    if sts == 0:
        output = p.stdout.read()
        jobid = SGE_SUBMIT_PATTERN.search(output).groups()[0]
    else:
        raise 

    os.remove(scriptfile)
    
    return jobid
    
call_script_template = """#!/bin/bash
#$$ -V
#$$ -cwd
#$$ -S /bin/bash

$PYEXEC -c "import $MODNAME, sge_utils; sge_utils.callfunc($MODNAME.$FNNAME,'$ARGFILE')"

"""
