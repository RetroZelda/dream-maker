#!/bin/bash
root_path=$(pwd)
motion_generating_path=$root_path/3rd-party/Animating-Landscape
motion_generation=$motion_generating_path/test.py
temp_folder="$root_path/temp"
out_folder="$root_path/output"

mkdir -p $temp_folder
mkdir -p $out_folder

# TODO: Take these in as a parameter
source_image="./test-files/test-image.jpg"
dream_depth=5
##########################################################

source_name="$(basename $source_image)"
image_extension="${source_name##*.}"
source_name="$(basename -s .$image_extension $source_image)"

if test $dream_depth -gt 0; then
    echo "generating dream..."
    result_blob=$(python3 ./scripts/deep-dream.py -o $temp_folder -i $source_image -d $dream_depth)
    exit_code=$?

    if test $exit_code -gt 0; then
        echo $result_blob
        exit 1
    fi

    readarray -d ' ' -t result <<< "$result_blob"
    id="${result[0]/"id:"/""}"
    source_image="${result[1]/"file:"/""}"
fi

image_path="$(readlink -f $source_image)"
image_file="$(basename $source_image)"
image_extension="${image_file##*.}"
image_filename="$(basename -s .$image_extension $source_image)"
working_folder=$temp_folder/$id

motion_generation_extension="avi"
motion_desired_extension="mp4"

# generate motion
# TODO: Add some params for direction, speed, etc
python3 $motion_generation --gpu 0 --model_path $motion_generating_path/models -i $source_image -o $working_folder -c MJPG -e $motion_generation_extension

motion_file=$working_folder/$image_filename.$motion_generation_extension
final_motion=$out_folder/${source_name}_dream.$motion_desired_extension

# opencv seems to only like to deal with *.avi(divx/mjpg) so lets just convert it to what we actually want: mp4
ffmpeg -i $motion_file -c:v libx264 -crf 19 -preset slow -c:a aac -b:a 192k -ac 2 $final_motion

echo "created \"$final_motion\""