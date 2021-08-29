import requests
import argparse
import shutil
import json
import sys
import os

global_endpoint = "https://api.deepai.org/api/deepdream"
global_apikey = '86e0151a-4419-4919-b4e0-d61b8420063a'
global_output_format = 'https://api.deepai.org/job-view-file/{id}/outputs/output.jpg'
global_output_dir = "{path}/{id}"
global_output_file = "{path}/final.jpg"
global_step_output_file = "{path}/step_{num}.jpg"

def ProcessImage(local_image_in, dir_out, count):
    step_responses = []

    # send the image to deepai
    request = requests.post(
        global_endpoint,
        files = { 'image': open(local_image_in, 'rb') },
        headers = {'api-key': global_apikey}
    )
    
    count -= 1
    while count > 0:
        response = json.loads(request.text)
        step_responses.append(response)
        request = requests.post(
            global_endpoint,
            data = { 'image': response['output_url'] },
            headers = {'api-key': global_apikey}
        )
        count -= 1

    # get our response and get hte url of our completed image
    response = json.loads(request.text)
    output_url = global_output_format.format(id=response['id'])
    
    # download the image
    file_request = requests.get(output_url, stream=True)
    file_request.raw.decode_content = True

    # separate into its own dir
    final_dir = global_output_dir.format(path=dir_out, id=response['id'])
    if not os.path.exists(final_dir):
        os.makedirs(final_dir)

    #save each step
    step_count = 0
    for response_step in step_responses:
        step_file_request = requests.get(response_step['output_url'], stream=True)
        step_file_request.raw.decode_content = True

        filename = global_step_output_file.format(path=final_dir, num=step_count)
        with open(filename, 'wb') as file_out:
                shutil.copyfileobj(step_file_request.raw, file_out)
        step_count += 1

    # save the image
    filename = global_output_file.format(path=final_dir)
    with open(filename, 'wb') as file_out:
            shutil.copyfileobj(file_request.raw, file_out)
            
    print("id:" + response['id'] + " " + "file:" + filename)
    return 0



def main(args):
    return ProcessImage(args.input, args.outdir, args.depth)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='deep-dream')
    parser.add_argument('--input', '-i')
    parser.add_argument('--outdir', '-o', default='./temp')
    parser.add_argument('--depth', '-d', type=int, default=1)
    args = parser.parse_args()

    result = main(args)
    sys.exit(result)