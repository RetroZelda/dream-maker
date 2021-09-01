import subprocess
import argparse
import shutil
import fcntl
import sys
import os

from fcntl import fcntl, F_GETFL, F_SETFL
from os import O_NONBLOCK

global_content_dir = "./3rd-party/CNNMRF/data/content"
global_style_dir = "./3rd-party/CNNMRF/data/style"
global_result_dir = "./3rd-party/CNNMRF/data/result"
global_cnnmrf_dir = "./3rd-party/CNNMRF"
global_cnnmrf = "./cnnmrf.lua"
global_cnnmrf_args = " -style_name {style} -content_name {content} -output_folder {output} -max_size 512 -ini_method image -type transfer -num_res 1 -num_iter 100"

def ProcessImage(content_image, style_image, out_dir):

    # extract the source and style image name
    image_name = os.path.basename(content_image)
    image_dest = global_content_dir + "/" + image_name
    image_name = os.path.splitext(image_name)[0]

    style_name = os.path.basename(style_image)
    style_dest = global_style_dir + "/" + style_name
    style_name = os.path.splitext(style_name)[0]

    # copy the source and style images to the required CNNMRF folders 
    shutil.copyfile(content_image, image_dest);
    shutil.copyfile(style_image, style_dest);

    # build args
    cnnmrf_args = global_cnnmrf_args.format(style = style_name, content = image_name, output = out_dir) # TODO: Add any other args

    # run CNNMRF
    activate_torch = ". ./3rd-party/torch/install/bin/torch-activate\n"
    initialize_lua = "luarocks install loadcaffe\n"
    switch_dir = 'cd ' + global_cnnmrf_dir + "\n"
    run_cnnmrf = "qlua " + global_cnnmrf + cnnmrf_args + "\n" 
    return_dir = "cd ../../\n"

    # run commands
    os.system(activate_torch + initialize_lua + switch_dir + run_cnnmrf + return_dir);
    
    # clean up the source and style image from CNNMRF
    os.remove(image_dest)
    os.remove(style_dest)

    return 0



def main(args):
    return ProcessImage(args.content_image, args.style_image, args.out_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='cnnmrf')
    parser.add_argument('--content_image', '-i')
    parser.add_argument('--style_image', '-s')
    parser.add_argument('--out_dir', '-o')
    args = parser.parse_args()

    result = main(args)
    sys.exit(result)