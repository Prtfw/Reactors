

# run the following commands to install packages in python venv
#pip install opencv-python
#pip install matplotlib
#pip install pprint
#pip install uuid

import uuid
import time 
import requests
import cv2
import operator
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from PIL import Image
from io import BytesIO
# %matplotlib inline

import pprint 
from pprint import pprint

# global vars
_maxNumRetries = 10

# General headers
headers = {
    'Content-Type': 'application/json', 
    'Ocp-Apim-Subscription-Key': _key
    }

# Primary keys

# Primary key
_key = 'you_key' # Here, paste your primary key

#Translator key
translate_key = 'you_key'

# Key sentiment
_sentiment_key = 'you_key'

# Face API key
face_api_key = 'you_key'

# Endpoint dictionaries

base_url = 'https://maddogtest.cognitiveservices.azure.com/'

# Cognitive API for Computer Vision
analyze_dict = {'computer_vision_API': 
                 [{'url': base_url + '/vision/v3.0/analyze',
                  '_key': _key,
                  'headers': headers,
                  'params': {'visualFeatures': 'Categories,Description,Color'}}]}


# Custom Vision API - Object Detection
detect_dict = {'object_detection_API': 
                 [{'url': base_url + 'vision/v3.0/detect' ,
                  '_key': _key,
                  'headers': headers,
                  'params': {'visualFeatures': 'Objects,Description'}}]}

                 
# OCR API 
text_recognition_dict = {'text_recognition_API': 
                 [{'url': base_url + '/vision/v3.0/read/analyze',
                  '_key': _key,
                  'headers': headers}]}


# Cognitive API for Translator Text 
translator_dict = {'translator_text_API': 
                 [{'url': 'https://api.cognitive.microsofttranslator.com/' + '/translate?api-version=3.0', 
                  '_key': translate_key,
                  'headers': {
                      'Content-Type': 'application/json', 
                      'Ocp-Apim-Subscription-Key': translate_key,
                      'Ocp-Apim-Subscription-Region': 'eastus',
                      'X-ClientTraceId': str(uuid.uuid4())
                      }}]}


# Cognitive API for Text Analytics
# @learner: replace this url with your endpoint
sentiment_dict = {'sentiment_analytics_API': 
                 [{'url': 'https://maddog-text-analytics.cognitiveservices.azure.com/' + '/text/analytics/v2.1/sentiment', 
                  '_key': _sentiment_key,
                   'headers': {
                      'Content-Type': 'application/json', 
                      'Ocp-Apim-Subscription-Key': _sentiment_key,
                      'Ocp-Apim-Subscription-Region': 'eastus',
                      'X-ClientTraceId': str(uuid.uuid4())
                      }}]}


# Face Detector API
face_detector_dict = {'face_detector_API': 
                 [{'url': 'https://eastus.api.cognitive.microsoft.com/face/v1.0/detect', 
                  '_key': face_api_key,
                   'headers': {'Ocp-Apim-Subscription-Key': face_api_key},
                   'params': {
                        'returnFaceId':
                        'true',
                        'returnFaceLandmarks':
                        'false',
                        'returnFaceAttributes':
                        'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise'}}]}



''' analyze image api '''

def processRequest(_url, json, data, headers, params ):

    """
    Helper function to process the request to Project Oxford

    Parameters:
    json: Used when processing images from its URL. See API Documentation
    data: Used when processing image read from disk. See API Documentation
    headers: Used to pass the key information and the data type request
    """

    retries = 0
    result = None

    while True:
        response = requests.request( 'post', _url, json = json, data = data, headers = headers, params = params )

        if response.status_code == 429: 

            print( "Message: %s" % ( response.json() ) )

            if retries <= _maxNumRetries: 
                time.sleep(1) 
                retries += 1
                continue
            else: 
                print( 'Error: failed after retrying!' )
                break

        elif response.status_code == 200 or response.status_code == 201:
            # print(response.json())
            if 'content-length' in response.headers and int(response.headers['content-length']) == 0: 
                result = None 
            elif 'content-type' in response.headers and isinstance(response.headers['content-type'], str): 
                if 'application/json' in response.headers['content-type'].lower(): 
                    result = response.json() if response.content else None 
                elif 'image' in response.headers['content-type'].lower(): 
                    result = response.content
        else:
            print( "Error code: %d" % ( response.status_code ) )
            print( "Message: %s" % ( response.json() ) )

        break
        
    return result

# Render result on image
def render_image(result_title, image_url):

  """Display the obtained results onto the input image"""
    
  image = Image.open(BytesIO(requests.get(image_url).content))

  fig, ax = plt.subplots(figsize=(10, 15))
  ax.imshow( image )

  plt.title(result_title, fontsize=30, va="center", color='r', weight='heavy')

# Cognitive API for Computer Vision

''' test code: analyze image api '''

analyze_image = 'https://thumbor.thedailymeal.com/QOuw1z3VzY5p7E4U2vd01ofzLk0=/870x565/https://www.theactivetimes.com/sites/default/files/2020/02/20/00_Hero.jpg'

analyze_json = {'url': analyze_image}
data = None

analyze_result = processRequest(analyze_dict['computer_vision_API'][0]['url'], 
                        analyze_json, 
                        data, 
                        analyze_dict['computer_vision_API'][0]['headers'], 
                        analyze_dict['computer_vision_API'][0]['params'] )

pprint(analyze_result['categories'][0]["detail"])

result_text = analyze_result['categories'][0]["detail"]['landmarks'][0]['name']

render_image(result_text, analyze_image)

# Custom Vision API - Object Detection
''' object detection api '''


def render_object_detection(image_url, detection_result):
  
  image = Image.open(BytesIO(requests.get(image_url).content))
  fig, ax = plt.subplots(figsize=(10,10))

  ax.imshow(image, alpha=0.6)

  for i in detection_result['objects']:
    fr = i["rectangle"]
    fa = i["object"]
    origin = (fr["x"], fr["y"])

    rectangle = patches.Rectangle(origin, fr["w"],
                            fr["h"], fill=False, linewidth=2, color='b')
    
    ax.axes.add_patch(rectangle)
    ax.text(origin[0], origin[1], "%s"%(fa),
                fontsize=10, weight="bold", va="bottom")

    ax.axis("off")

''' test code: object detection api '''

detection_image = 'https://docs.microsoft.com/en-us/azure/cognitive-services/computer-vision/images/windows-kitchen.jpg'

detect_json = { 'url': detection_image } 
data = None

detection_result = processRequest(detect_dict['object_detection_API'][0]['url'], 
                        detect_json, 
                        data, 
                        detect_dict['object_detection_API'][0]['headers'], 
                        detect_dict['object_detection_API'][0]['params'] )


detection_text_list = []
for i in detection_result['objects']:
  detection_text_list.append(i['object'])
listToStr = ' '.join([str(elem) for elem in detection_text_list]) 

#render_image(listToStr, detection_image)
detection_result['objects']

object_names = []
for i in detection_result['objects']:
  object_names.append(i['object'])
text_to_image = str(object_names)

render_object_detection(detection_image, detection_result)

"""OCR Problem
Finding Text in Signboards
"""

# Text recognition function

def text_recognition(_url, headers, json, data):

  response = requests.request( 'post', _url, headers = headers, json = json, data = data)
  response.raise_for_status()

  # Holds the URI used to retrieve the recognized text.
  operation_url = response.headers["Operation-Location"]

  result = {}
  while (True):

    response_final = requests.get(
        response.headers["Operation-Location"], headers=headers)
    
    result = response_final.json()

    time.sleep(1)

    if ("analyzeResult" in result):
      break
    if ("status" in result and result['status'] == 'failed'):
      break

  return result

# Render image
def render_text_recognition_image(result, image):
  
  polygons = []

  if ("analyzeResult" in result):
    
    # Extract the recognized text, with bounding boxes.
    polygons = [(line["boundingBox"], line["text"])
    for line in result["analyzeResult"]["readResults"][0]["lines"]]
    
  image = Image.open(BytesIO(requests.get(image_url).content))

  fig, ax = plt.subplots(figsize=(15, 20))
  ax.imshow( image )
  

  for polygon in polygons:
      vertices = [(polygon[0][i], polygon[0][i+1])
                  for i in range(0, len(polygon[0]), 2)]

      text = polygon[1]
      patch = Polygon(vertices, closed=True, fill=False, linewidth=2, color='y')
      ax.axes.add_patch(patch)
      plt.text(vertices[0][0], vertices[0][1], text, fontsize=24, va="center", color='r', weight='heavy', 
               family='monospace', rotation=25)

"""test code: OCR Problem
Finding Text in Signboards
"""

image_url = "https://images.unsplash.com/photo-1483213097419-365e22f0f258?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1050&q=80"

json = { 'url': image_url } 
data = None

# Result of text recognitioning
ocr_result = text_recognition(text_recognition_dict['text_recognition_API'][0]['url'],
                          text_recognition_dict['text_recognition_API'][0]['headers'],
                          json, 
                          data)

pprint( ["AI description of image: ", ocr_result['analyzeResult']['readResults'][0]['lines'] ])

# Render image with predictions / bounding boxes
render_text_recognition_image(ocr_result, image_url)

""" Translator API"""

# Helper function to translate text 
def translate_text(translate_urltranslate_key, params, data, json):

  constructed_url = translator_dict['translator_text_API'][0]['url'] + params

  response = requests.request('post', constructed_url, data = data, json=json, headers = translator_dict['translator_text_API'][0]['headers'])
  response.raise_for_status()
  result = response.json()

  return result

""" test code: tex rec API"""

# Set image_url to the URL of an image that you want to recognize.
image_url = "https://s3-ap-southeast-2.amazonaws.com/wc-prod-pim/JPEG_1000x1000/SANMS93_sandleford_open_closed_sign_225_x_300mm.jpg"

json = { 'url': image_url } 
data = None

# Result of text recognitioning
translate_result = text_recognition(text_recognition_dict['text_recognition_API'][0]['url'], 
                                    text_recognition_dict['text_recognition_API'][0]['headers'], 
                                    json, 
                                    data)

# Print to see results in terminal
pprint(translate_result)

import json as j

# Convert translation to json
def translation_to_json(result):
  text_to_translate = []

  for i in result['analyzeResult']['readResults'][0]['lines']:
    text_to_translate.append(i['text'])

  convert_to_json = j.dumps(text_to_translate)

  return convert_to_json
""" test code: translator API"""
# Translate to spanish
params = '&to=es'

data = None

# Translate extracted result
body = [{'text': translation_to_json(translate_result)}]

spanish_result = translate_text(translator_dict['translator_text_API'][0]['_key'], params, data, body)

spanish_result

# Extract translated text from result
translation = ''
for i in spanish_result[0]['translations']:
  translation = i['text']
  translation = str(translation).strip('[]')
print(translation)

# Render translation on image
render_image(translation, image_url);

"""Sentiment Analysis
Cognitive API for Text Analytics
"""

# # Cognitive API for Text Analytics
def sentiment_analysis(text, language):

  documents = {"documents": [
    {"id": "1", "language": language,
        "text": text}
              ]}
  
  response = requests.post(sentiment_dict['sentiment_analytics_API'][0]['url'], 
                           headers=sentiment_dict['sentiment_analytics_API'][0]['headers'], 
                           json=documents)
  
  sentiment_result = response.json()

  return sentiment_result

def count_score(sentiment_result):
  # The sentiment score for a document is between 0.0 and 1.0, with a higher score indicating a more positive sentiment.
  positive = 0
  negative = 0
  for i in sentiment_result['documents']:
    score = i['score']
    if(score > 0.50):
      positive+=1
    else:
      negative+=1

  print('Positive score: ', positive)
  print('Negative score: ', negative)

# Write an input text and analyze 
text = input('Write you sentence here: ')

""" test code: Sentiment API"""
# Save result as a variabel
sentiment_result_english = sentiment_analysis(text, 'en')

# See score for positive/negative
print(count_score(sentiment_result_english))

# In Spanish
text = "Los caminos que llevan hasta Monte Rainier son espectaculares y hermosos."
# Save result as a variabel
sentiment_result_spanish = sentiment_analysis(text, 'es')

# See output
pprint(sentiment_result_spanish)

"""Azure Media Face Detector"""

# Face Detect API 

# Image to detect
face_detect_image = 'https://upload.wikimedia.org/wikipedia/commons/3/37/Dagestani_man_and_woman.jpg'

json = { 'url': face_detect_image } 
data = None

face_result = processRequest(face_detector_dict['face_detector_API'][0]['url'],
               json,
               data,
               face_detector_dict['face_detector_API'][0]['headers'],
               face_detector_dict['face_detector_API'][0]['params'])

pprint(face_result)

"""test code: Azure Media Face Detector"""


# Save emotion for sentiment analysis
emotion = ''
for i in face_result:
  emotion = i['faceAttributes']['emotion']

# Save results in new list
result_list = []

# Loop through emotion items and append to list
for key, value in emotion.items():
  if(value > 0):
    result = sentiment_analysis(key, 'en')
    result_list.append(result)
    pprint(key)

# Plot sentiment analysis on image

def render_face_sentiment_image(image_url, result):
  
  image = Image.open(BytesIO(requests.get(image_url).content))
  fig, ax = plt.subplots(figsize=(10,10))

  ax.imshow(image, alpha=0.6)

  for face in result:
    fr = face["faceRectangle"]
    fa = face["faceAttributes"]
    origin = (fr["left"], fr["top"])

    rectangle = patches.Rectangle(origin, fr["width"],
                            fr["height"], fill=False, linewidth=2, color='b')
    
    ax.axes.add_patch(rectangle)
    ax.text(origin[0], origin[1], "%s"%(fa["emotion"]),
                fontsize=10, weight="bold", va="bottom")

    ax.axis("off")

render_face_sentiment_image(face_detect_image, face_result)

