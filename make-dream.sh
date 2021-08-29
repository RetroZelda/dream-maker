#!/bin/bash
root_path=$(pwd)
motion_generating_path=$root_path/3rd-party/Animating-Landscape
motion_generation=$motion_generating_path/test.py
temp_folder="$root_path/temp"

source_image="./test-files/test-image.jpg"

echo "generating image..."
result_blob=$(python3 ./scripts/deep-dream.py -o $temp_folder -i $source_image -d 5)
exit_code=$?

if test $exit_code -gt 0; then
    echo $result_blob
    exit 1
fi

readarray -d ' ' -t result <<< "$result_blob"
id="${result[0]/"id:"/""}"
image="${result[1]/"file:"/""}"
image_path="$(readlink -f $image)"
image_file="$(basename $image)"
image_extension="${image_file##*.}"
image_filename="$(basename -s .$image_extension $image)"
working_folder=$temp_folder/$id

motion_generation_extension="avi"
motion_desired_extension="mp4"

python3 $motion_generation --gpu 0 --model_path $motion_generating_path/models -i $image -o $working_folder -c MJPG -e $motion_generation_extension

motion_file=$working_folder/$image_filename.$motion_generation_extension
final_motion=$working_folder/$image_filename.$motion_desired_extension

# opencv seems to only like to deal with mjpg so lets just convert it to what we actually want: mp4
ffmpeg -i $motion_file -c:v libx264 -crf 19 -preset slow -c:a aac -b:a 192k -ac 2 $final_motion
