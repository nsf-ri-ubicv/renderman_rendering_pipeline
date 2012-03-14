#!/bin/bash

VENV=~/rendering

. $VENV/bin/activate

cd $VENV/Thorender/tasks

$VENV/bin/celeryd --loglevel=INFO