#!/bin/bash
#$ -N JOB_NAME
#$ -S /bin/bash
#$ -V 
#$ -pe orte 2

python -c "import renderer as R; R.render_single_image_qsub('$1','$2')"