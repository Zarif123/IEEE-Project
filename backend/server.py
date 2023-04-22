from flask import Flask
import torch
from flask import request
from flask import jsonify
# import flask
from torchvision import transforms
from PIL import Image
import datetime
import json
import base64
import numpy as np
from PIL import Image

import torch.nn as nn
import torch.nn.functional as F

import pandas as pd

date = datetime.datetime.now()

# Model
class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 6, 5) # convolutional layers
        self.pool = nn.MaxPool2d(2, 2) # size of pool for image
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16 * 53 * 53, 120) # this down is all the hidden layrs
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 101)

    def forward(self, x):
        # print(x.size())
        x = self.pool(F.relu(self.conv1(x)))
        # print(x.size())
        x = self.pool(F.relu(self.conv2(x)))
        # print(x.size())
        x = torch.flatten(x, 1) # flatten all dimensions except batch
        x = F.relu(self.fc1(x)) # activation functions
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x
    
def transform_image(img):
    imagenet_stats = [(0.485, 0.456, 0.406), (0.229, 0.224, 0.225)]
    imgenet_mean = imagenet_stats[0]
    imgenet_std = imagenet_stats[1]
    valid_tfms = transforms.Compose([
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(imgenet_mean, imgenet_std)]) 
    return valid_tfms(Image.open((img))).unsqueeze(0)

def get_name_ing(food_class):
    df = pd.read_json('ingredients.json')
    food_name = df.iloc[food_class].FoodName
    ingredients = df.iloc[food_class].CleanIngredients
    return jsonify(foodName=food_name,
                   ingredients=ingredients)

# Initializing flask app
app = Flask(__name__)
  
  
# Route for seeing a data
@app.route('/data')
def get_time():
  
    # Returning an api for showing in  reactjs
    return {
        'Name':"david Wang", 
        "Age":"22",
        "Date":date, 
        "programming":"python"
        }

@app.route('/imgResponse', methods=['POST', 'GET'])
def get_food_name():
    if request.method == 'POST':
        #print(request.get_json())
        img = request.get_json()
        img = img['img']
        # print(base64.b64decode(img))
        decodedData = base64.b64decode(img)
        imgFile = open('image.png', 'wb')
        imgFile.write(decodedData)
        imgFile.close()
        img_tensor = transform_image('image.png')

        model = Net()
        model.load_state_dict(torch.load('model.pth', map_location='cpu'))
        pred = model(img_tensor)
        food_class = torch.argmax(pred, dim=1)
        return get_name_ing(food_class.item())

    else:
        return {'yes': 'no'}
    
    # for i in len(tensor_image):
    #     print(tensor_image[i])
    return {'ingredients': ['eggs', 'steak', 'bread'], 'food name': 'tartare'}
  
@app.route('/')
def hello():
    return {'hey': 'hello'}
# Running app
if __name__ == '__main__':
    app.run(debug=True)


