#!/bin/bash

rm -drf ./temp
rm -drf ./output
rm -drf ./3rd-party
mkdir temp
mkdir output
mkdir 3rd-party

OUTDIR="$(pwd)/output"
TMPDIR="$(pwd)/temp"
ROOTDIR="$(pwd)"

# things for animating landscapes
pip3 install torch==1.9.0+cu111 torchvision==0.10.0+cu111 torchaudio==0.9.0 -f https://download.pytorch.org/whl/torch_stable.html
pip3 install opencv-python
pip3 install scikit-learn
pip3 install gdown
pip3 install numpy

git clone https://github.com/RetroZelda/Animating-Landscape.git ./3rd-party/Animating-Landscape

wget 'http://www.cgg.cs.tsukuba.ac.jp/~endo/projects/AnimatingLandscape/models.zip' -O ./temp/models.zip
7z x ./temp/models.zip -o./3rd-party/Animating-Landscape/

# things for CNNMRF
git clone https://github.com/RetroZelda/CNNMRF.git ./3rd-party/CNNMRF

# get the CNNMRF data models
cd ./3rd-party/CNNMRF/data/models
./download_models.sh
cd $ROOTDIR