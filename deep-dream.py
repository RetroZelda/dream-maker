import requests
import shutil
import json
import sys
import os

global_endpoint = "https://api.deepai.org/api/deepdream"
global_apikey = '86e0151a-4419-4919-b4e0-d61b8420063a'
global_output_format = 'https://api.deepai.org/job-view-file/{id}/outputs/output.jpg'
global_output_file = "{path}/{id}.jpg"

def ProcessImage(local_image_in, dir_out):
    
    # send the image to deepai
    request = requests.post(
        global_endpoint,
        files = { 'image': open(local_image_in, 'rb') },
        headers = {'api-key': global_apikey}
    )

    # get our response and get hte url of our completed image
    response = json.loads(request.text)
    output_url = global_output_format.format(id=response['id'])
    
    # download the image
    file_request = requests.get(output_url, stream=True)
    file_request.raw.decode_content = True

    if not os.path.exists(dir_out):
        os.makedirs(dir_out)

    # save the image
    filename = global_output_file.format(path=dir_out, id=response['id'])
    with open(filename, 'wb') as file_out:
            shutil.copyfileobj(file_request.raw, file_out)



def main(argv):
    ProcessImage("./test-files/test-image.jpg", "./temp")

if __name__ == "__main__":
    main(sys.argv)