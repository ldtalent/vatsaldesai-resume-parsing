#!/usr/bin/env python
"""This file performs basic operation to convert image to text using Google Cloud Vision API
Google Cloud Vision API.
"""

import io
import argparse
import json
import ntpath
import os
from google.cloud import vision
import googleapiclient
import base64
from google.protobuf.json_format import MessageToJson, MessageToDict


def detectTextBase64(uri):
    # Instantiates a client
    service = googleapiclient.discovery.build('vision', 'v1')

    # Image file
    file_name = uri

    # Loads the image into memory
    with open(file_name, 'rb') as image:
        image_content = base64.b64encode(image.read())

        # Creates the request
        service_request = service.images().annotate(body={
            'requests': [{
                'image': {
                    'content': image_content.decode('UTF-8')
                },
                'features': [{
                    'type': 'TEXT_DETECTION',
                }]
            }]
        })

    # Execute the request
    response = service_request.execute()

    # Convert to Json
    res_json = json.dumps(response)

    return res_json


def extractDeveloperName(filename):
    # src = pathlib.Path(filename).resolve()

    fname_w_extn = ntpath.basename(filename)

    fname, fextension = os.path.splitext(fname_w_extn)

    # print(fextension)
    # print(fname)
    return fname


# Pass the image data to an encoding function.
def encode_image(image):
    image_content = image.read()
    return base64.b64encode(image_content)


def detect_text(path):
    """Detects text in the file."""
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)

    response = MessageToDict(response, preserving_proto_field_name=True)
    # desired_res = response["label_annotation"]
    # serialized = MessageToJson(response.text_annotations)
    # texts = response.text_annotations
    texts = response

    print('Texts:')

    for text in texts:
        print(text)
        # print('\n"{}"'.format(text.description))

        # vertices = (['({},{})'.format(vertex.x, vertex.y)
        # for vertex in text.bounding_poly.vertices])

        # print('bounds: {}'.format(','.join(vertices)))
    return texts


def process_directory(path):
    for filename in os.listdir(path):
        if filename.endswith(".jpg") or filename.endswith(".JPG") or filename.endswith(".JPEG") or filename.endswith(
                ".jpeg"):
            print(os.path.join(path, filename))
            print(filename)
            # frameMD5 = md5(os.path.join(args["path"], filename))
            response = detect_text(os.path.join(path, filename))
            # apiResponseJSON = detectTextBase64(uri = os.path.join(args["path"], filename))
            # Convert the response to dictionary
            # apiResponse = MessageToDict(response)
            newFileName = extractDeveloperName(filename) + '.json'
            # Convert to Json
            # apiResponseJSON = json.dumps(response)
            with open(newFileName, "a+") as data_file:
                json.dump(response, data_file, indent=2)


if __name__ == '__main__':
    # construct the argument parse and parse command line arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--path", required=True, help="path to the image files")
    args = vars(ap.parse_args())
    pattern = '[0-9]'
    process_directory(args["path"])
