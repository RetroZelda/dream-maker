#!/bin/bash

ROOT_DIR=$(pwd)


cd ./3rd-party/Animating-Landscape/
#export LD_LIBRARY_PATH=/home/retrozelda/Development/3rdparty/ZLUDA/target/release 
python3 test.py -i $ROOT_DIR/temp/test-image.jpg -o $ROOT_DIR/temp