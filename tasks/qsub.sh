#!/bin/bash

VENV=~/rendering

. $VENV/bin/activate

cd $VENV/Thorender/tasks

HOST=honeybadger.rowland.org
PORT=22334
DBNAME=image_generation
COLNAME=test0
FSNAME=test0fs
KEY=test0key

$VENV/bin/fab mongo_worker:$HOST,$PORT,$DBNAME,$COLNAME,$FSNAME,$KEY