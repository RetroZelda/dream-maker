# dream-maker

requirements: 
	p7zip-full
	ffmpeg
	libprotobuf-dev
	protobuf-compiler
	luarocks
	Torch - https://github.com/RetroZelda/distro
	Cuda 10.2 - https://developer.nvidia.com/cuda-10.2-download-archive
	CUDNN 7.6.5 - https://developer.nvidia.com/rdp/cudnn-archive

NOTE:

To get torch installed you should only need do the following once:
	git clone https://github.com/RetroZelda/distro ./torch --recursive
	cd ./torch
	./install-deps
	./clean.sh
	./update.sh

	. ./torch/install/bin/torch-activate
	sudo apt-get install libprotobuf-dev protobuf-compiler
	luarocks install loadcaffe

setup.sh should install the rest
