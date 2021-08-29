import requests
import argparse
import shutil
import json
import sys
import os

global_endpoint_fast = "https://api.deepai.org/api/fast-style-transfer"
global_endpoint_slow = "https://api.deepai.org/api/CNNMRF"
global_endpoint_neural = "https://api.deepai.org/api/neural-style"
global_apikey = '86e0151a-4419-4919-b4e0-d61b8420063a'
global_output_format = 'https://api.deepai.org/job-view-file/{id}/outputs/output.jpg'
global_output_dir = "{path}/{id}"
global_output_file = "{path}/final.jpg"
global_step_output_file = "{path}/step_{num}.jpg"

def ProcessImage(content_image, style_image, dir_out, desired_endpoint):
   
    # send the image to deepai
    request = requests.post(
        desired_endpoint,
        files = {
            'content': open(content_image, 'rb'),
            'style': open(style_image, 'rb') 
        },
        headers = {'api-key': global_apikey}
    )

    # get our response and get hte url of our completed image
    response = json.loads(request.text)
    output_url = response['output_url']
    
    # download the image
    file_request = requests.get(output_url, stream=True)
    file_request.raw.decode_content = True

    # separate into its own dir
    final_dir = global_output_dir.format(path=dir_out, id=response['id'])
    if not os.path.exists(final_dir):
        os.makedirs(final_dir)

    # save the image
    filename = global_output_file.format(path=final_dir)
    with open(filename, 'wb') as file_out:
            shutil.copyfileobj(file_request.raw, file_out)
            
    print("id:" + response['id'] + " " + "file:" + filename)
    return 0



def main(args):

    endpoint_type = args.endpoint_type.lower()
    desired_endpoint = ""
    if endpoint_type == "fast":
        desired_endpoint = global_endpoint_fast
    elif endpoint_type == "slow":
        desired_endpoint = global_endpoint_slow
    elif endpoint_type == "neural":
        desired_endpoint = global_endpoint_neural
    else:
        print("Invalid endpoint_type: " + args.endpoint_type)
        return 1

    return ProcessImage(args.content_image, args.style_image, args.outdir, desired_endpoint)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='style-transfer')
    parser.add_argument('--content_image', '-i')
    parser.add_argument('--style_image', '-s')
    parser.add_argument('--outdir', '-o', default='./temp')
    parser.add_argument("--endpoint_type", '-t')
    args = parser.parse_args()

    result = main(args)
    sys.exit(result)