#!/bin/sh

python api.py &

cd frontend
make serve-source

