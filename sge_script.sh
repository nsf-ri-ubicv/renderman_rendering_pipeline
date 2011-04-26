#!/bin/bash
#$ -N $1
#$ -S /bin/bash
#$ -pe orte 2

python -c "import renderer as R; R.render_single_image_qsub($2,$3)"