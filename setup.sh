#!/bin/bash

rm -drf ./temp
rm -drf ./3rd-party
mkdir temp
mkdir 3rd-party

export TMPDIR=$(pwd)/temp

# pip install torch torchvision torchaudio
pip3 install torch==1.9.0+cu111 torchvision==0.10.0+cu111 torchaudio==0.9.0 -f https://download.pytorch.org/whl/torch_stable.html
# pip install torch==1.9.0+cpu torchvision==0.10.0+cpu torchaudio==0.9.0 -f https://download.pytorch.org/whl/torch_stable.html
pip3 install opencv-python
pip3 install scikit-learn
pip3 install gdown
pip3 install numpy

git clone https://github.com/RetroZelda/Animating-Landscape.git ./3rd-party/Animating-Landscape

wget 'http://www.cgg.cs.tsukuba.ac.jp/~endo/projects/AnimatingLandscape/models.zip' -O ./temp/models.zip
7z x ./temp/models.zip -o./3rd-party/Animating-Landscape/
