#!/bin/bash
root_path=$(pwd)
temp_folder="$root_path/temp"
out_folder="$root_path/output"

mkdir -p $temp_folder
mkdir -p $out_folder

# TODO: Get from input params
# TODO: Get more parameters
source_image="./test-files/test-image.jpg"
source_style="./test-files/test-style.jpg"
######################################################

image_name="$(basename $source_image)"
image_extension="${image_name##*.}"
image_name="$(basename -s .$image_extension $source_image)"

style_name="$(basename $source_style)"
style_extension="${style_name##*.}"
style_name="$(basename -s .$style_extension $source_style)"

out_dir="$out_folder/${image_name}_to_${style_name}"
rm -drf $out_dir
mkdir -p $out_dir

echo "applying style to image..."
python3 ./scripts/cnnmrf.py -i $source_image -s $source_style -o $out_dir

echo "check $out_dir for your results"