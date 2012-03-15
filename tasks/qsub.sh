#!/bin/bash

VENV=~/rendering

. $VENV/bin/activate

cd $VENV/Thorender/tasks

HOST=honeybadger.rowland.org
PORT=22334
DBNAME=new_images
COLNAME=image_set_1
FSNAME=image_set_1_fs
KEY=image_set_1

$VENV/bin/fab mongo_worker:$HOST,$PORT,$DBNAME,$COLNAME,$FSNAME,$KEY