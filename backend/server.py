from flask import Flask
import torch
from flask import request
# import flask
from torchvision import transforms
from PIL import Image
import datetime
import json
import base64
import numpy as np
from PIL import Image
x = datetime.datetime.now()
  
# Initializing flask app
app = Flask(__name__)
  
  
# Route for seeing a data
@app.route('/data')
def get_time():
  
    # Returning an api for showing in  reactjs
    return {
        'Name':"david Wang", 
        "Age":"22",
        "Date":x, 
        "programming":"python"
        }

@app.route('/imgResponse', methods=['POST', 'GET'])
def get_food_name():
    if request.method == 'POST':
        print(request.get_json())
        img = request.get_json()
        img = img['img']
        # print(base64.b64decode(img))
        decodedData = base64.b64decode(img)
        imgFile = open('image.png', 'wb')
        imgFile.write(decodedData)
        imgFile.close()
        img = Image.open("image.png")
        convert_tensor = transforms.ToTensor()
        img_tensor = convert_tensor(img)
        print(img_tensor)
        # tensor_image = transforms.ToTensor(base64.b64decode(img))
        # print(tensor_image)
    else:
        return {'yes': 'no'}
    
    # for i in len(tensor_image):
    #     print(tensor_image[i])
    return {'hello': img}
  
@app.route('/')
def hello():
    return {'hey': 'hello'}
# Running app
if __name__ == '__main__':
    app.run(debug=True)


