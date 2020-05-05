import ipfs
from flask import Flask, jsonify,request
from flask_cors import CORS
import os
import json
from tempfile import NamedTemporaryFile
import tempfile
from sms import send_sms

app = Flask(__name__)
CORS(app)

PORT = '5000'

THREAD_RUN = False # keep false for model

DEBUG_RUN = True

HOST = '0.0.0.0'

MYIP = ''

_current_imagepath = ''
_current_datapath = ''


@app.route('/image', methods=['POST'])
def receive_image():
    try: 
        # Get request file and save to server
        image = request.files['file']
        filename = image.filename

        _current_imagepath = os.path.join(tempfile.gettempdir(), filename)
        image.save(_current_imagepath)

        # Upload to blockchain, save current data and return link to client
        response = ipfs.upload_ipfs(_current_imagepath, 'IMG', _current_imagepath)
        message = clean_response(response)

        # define if request was successful
        message["success"] = True

        # send back the name
        message["filename"] = filename

        sms = "Hash: %s \n \
File: %s \n \
Type: %s \n \
Link: %s \n" % (message['Hash'], message['filename'], message['type'], message['link'])
        send_sms(sms)

        #with open ('current_data.json', 'w') as cd:
        #    json.dump(message, cd)
        return jsonify(message)
    except Exception as e:        
        message = 'Error receiving message: % s' % e
        #with open ('error.json', 'w') as err:
        #    json.dump(message, err)
        return jsonify({'status' : message, 'success': False})


def clean_response(response):
    response.pop('Name')
    response['id'] = response['id'].replace('downloads/', '').split('.')[0]
    link = dict(link = ipfs.READ_URL + response['Hash'])
    response.update(link)
    return response

@app.route('/json', methods=['POST'])
def process_json():
    input_json = request.get_json()
    with open ('current_data.json', 'r') as cd:
        img_data = json.load(cd)
    input_json.update(img_data)
    return jsonify(input_json)


if __name__ == '__main__':
    app.run(debug=DEBUG_RUN)


# .json input example input - use for debugging
'''
{
   "scan_hash" : "6c8whrnwr8w9eb6wb8erw",
   "user_name": "Lon",
   "is_immune": true,
   "timestamp": 1586042898041
}
'''
