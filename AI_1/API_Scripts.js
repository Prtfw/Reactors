/*
@TODOS:
- json key and base url file for env vars
- add template file for env_var.json
- import to dict and use in code
- add local key file to .gitignore
- move example image urls to top of file for ease of use
*/



// Foundation url for azure account
const azure_base_url = 'https://maddogtest.cognitiveservices.azure.com/'

// Computer Vision API
const analyze_endpoint = azure_base_url + '/vision/v3.0/analyze'

// Object Detection API
const detection_endpoint = 'https://maddogtest.cognitiveservices.azure.com/' + "vision/v3.0/detect"

// OCR API
const text_recognition_url = 'https://maddogtest.cognitiveservices.azure.com/' + '/vision/v3.0/read/analyze'

// Cognitive API for Translator Text
const translator_text_url = 'https://api.cognitive.microsofttranslator.com/' + '/translate?api-version=3.0'

// Translation endpoint
let translation_endpoint = 'https://api.cognitive.microsofttranslator.com/'

// General API key
const api_key = 'insert key'

// Translator key
const translate_key = 'insert key'

// Headers
const headers = {
  'Content-Type': 'application/json',
  'Ocp-Apim-Subscription-Key' : api_key
}

const request = require('request');


//***************************************************************************************************************************** */

// Function POST API
const fetch = require("node-fetch");
const requestp = require("request-promise");
const { uuid } = require('uuidv4');


const post_API = async (endpoint, json, headers, params) => {

  const response = await fetch(endpoint, {
    method: 'POST',
    params: params,
    headers: headers,
    body: JSON.stringify({'url': json})
  })

  const json_dict = await response.json()
  // console.log(json_dict.categories[0].name)
  return json_dict
}

//***************************************************************************************************************************** */

// Computer Vision API

// Image used for computer vision API
let analyze_image = 'https://thumbor.thedailymeal.com/QOuw1z3VzY5p7E4U2vd01ofzLk0=/870x565/https://www.theactivetimes.com/sites/default/files/2020/02/20/00_Hero.jpg'

// Headers
const analyze_headers = {
  'Content-Type': 'application/json',
  'Ocp-Apim-Subscription-Key' : api_key
}

// Params for computer vision API
const analyze_params = {
  'visualFeatures': 'Categories,Description,Color'
}

// Computer VISION API call
post_API(analyze_endpoint, analyze_image, analyze_headers, analyze_params).then(x=>console.log('\n !!!!! Computer Vision API \n ',
JSON.stringify(x.categories[0].name), '\n', x))
              .catch(err => console.log(err))

//***************************************************************************************************************************** */

// Object Detection API

let detection_image =  'https://docs.microsoft.com/en-us/azure/cognitive-services/computer-vision/images/windows-kitchen.jpg'

// Headers
const detection_headers = {
  'Content-Type': 'application/json',
  'Ocp-Apim-Subscription-Key' : api_key
}

const detection_params = {
  'visualFeatures': 'Objects,Description'
}

// Object Dtection API call
post_API(detection_endpoint, detection_image, detection_headers, detection_params).then(x=>console.log('\n!!!!!! Object Detection API\n',
JSON.stringify(x), '\n'))
              .catch(err => console.log(err))


//***************************************************************************************************************************** */
// Text recognition

// Set image_url to the URL of an image that you want to recognize.
// Text recognition

// Set image_url to the URL of an image that you want to recognize.
let text_recognition_image = 'https://images.unsplash.com/photo-1483213097419-365e22f0f258?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1050&q=80'


const process_text_API = async (endpoint, json, headers) => {

  const response = await fetch(endpoint, {
    method: 'POST',
    headers: headers,
    body: JSON.stringify({'url': json})
  }),

  response_headers = response.headers.get(('Operation-Location'), headers)

  result = process_text_final_response(response_headers)

  return result

}

const process_text_final_response = async (response_headers) => {

  result = {}

  while (true){

    const response2 = await fetch(response_headers,{
      method: 'GET',
      headers: headers,
      location: 'Operation-Location'
    })

  result = await response2.json()

  if ('analyzeResult' in result){
    break
    }

  if('status' in result && result.status == 'failed'){

    break
    }
 }

  return result
}


// Text recognition API
process_text_API(text_recognition_url, text_recognition_image, headers).then(x=>console.log('\n!!!!! OCR API results \n',
(JSON.stringify(x.analyzeResult.readResults[0].lines)), '\n'))
              .catch(err => console.log(err))


//***************************************************************************************************************************** */

// Sentiment analysis

// Cognitive API for Text Analytics
const sentiment_url = 'https://maddog-text-analytics.cognitiveservices.azure.com/' + '/text/analytics/v2.1/sentiment'

//Key sentiment
const _sentiment_key = 'insert key'

const process_sentiment= async (text, language) => {

  const response = await fetch(sentiment_url, {
    method: 'POST',
    headers: {
      'Ocp-Apim-Subscription-Key': _sentiment_key,
      'Content-type': 'application/json',
      'Ocp-Apim-Subscription-Region': 'eastus',
      'X-ClientTraceId': uuid().toString()
      },
      body: JSON.stringify
      (
        {"documents": [
        {"id": "1", "language": language,
            "text": text}
                  ]
                }
      )
  })

  const sentiment_result = await response.json()

  return sentiment_result
}

let my_text = 'you are nice'
process_sentiment(my_text, 'en').then(x=>console.log('\n!!!!!! Sentiment analysis results \n ',
JSON.stringify(x), '\n'))
              .catch(err => console.log(err))



//***************************************************************************************************************************** */

// Azure Media Face Detector

//Face API endpoint
const face_api_endpoint = 'https://eastus.api.cognitive.microsoft.com/face/v1.0/detect'

//Primary key
const face_api_key = 'insert key'

//Image to detect
const detect_image_url = 'https://upload.wikimedia.org/wikipedia/commons/3/37/Dagestani_man_and_woman.jpg'


const process_request_face_detect = async () => {
  const _params= {
      'returnFaceId': 'true',
      'returnFaceLandmarks': 'true',
      'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise'
      }


var URL = require('url').URL;
var url = new URL(face_api_endpoint)


const {URLSearchParams} = require('url');
url.search = new URLSearchParams(_params).toString();
  const response = await fetch(url, {
    method: 'POST',
    params: {
      'returnFaceId': 'true',
      'returnFaceLandmarks': 'true',
      'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise'
      },
      headers: {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': face_api_key
      },
        body: JSON.stringify({'url': detect_image_url})
      })


      const json_dict = await response.json()

      return json_dict

}


process_request_face_detect(detect_image_url).then(x=>console.log("\n!!!!! Face Detection API results\n", JSON.stringify(x)))
              .catch(err => console.log(err))


//TRANSLATION API*****************************************************

let translation_image = 'https://s3-ap-southeast-2.amazonaws.com/wc-prod-pim/JPEG_1000x1000/SANMS93_sandleford_open_closed_sign_225_x_300mm.jpg'

function translate(json_text){
  let options = {
    method: 'POST',
    baseUrl: translation_endpoint,
    url: 'translate',
    qs: {
      'api-version': '3.0',
      'to': ['ja']
    },
    headers: {
      'Ocp-Apim-Subscription-Key': translate_key,
      'Ocp-Apim-Subscription-Region': 'eastus',
      'Content-type': 'application/json',
      'X-ClientTraceId': uuid().toString()
    },
    body: [{
          'text': json_text
    }],
    json: true,
  };

  let result = request(options, function(err, res, body){
    return JSON.stringify(body, null, 4)
  });
}




process_text_API(text_recognition_url, translation_image, headers).then( (x)=> {

  result = x.analyzeResult.readResults[0].lines
  word_list = []
  for(let i in result){
    words = result[i].text
    words = words.toLowerCase()
    word_list.push(words)
  }
  word_list = word_list.join(' ')
  word_list = JSON.stringify(word_list)
  translate(word_list)
}).catch(err => console.log(err))


const process_text_API_TEST = async (endpoint, json, headers) => {

  const response = await fetch(endpoint, {
    method: 'POST',
    headers: headers,
    body: JSON.stringify({'url': json})
  }),

  response_headers = response.headers.get(('Operation-Location'), headers)

  result = await process_text_final_response(response_headers)

  bounding_boxes = await result.analyzeResult.readResults[0].lines
  word_list = []
  for(let i in bounding_boxes){
    words = await bounding_boxes[i].text
    words = words.toLowerCase()
    word_list.push(words)
  }
  word_list = word_list.join(' ')
  word_list = JSON.stringify(word_list)
  let options = {
    method: 'POST',
    baseUrl: translation_endpoint,
    url: 'translate',
    qs: {
      'api-version': '3.0',
      'to': ['ja']
    },
    headers: {
      'Ocp-Apim-Subscription-Key': translate_key,
      'Ocp-Apim-Subscription-Region': 'eastus',
      'Content-type': 'application/json',
      'X-ClientTraceId': uuid().toString()
    },
    body: [{
          'text': word_list
    }],
    json: true,
  };

  let translation_results = await requestp(options)

  return translation_results

}
(async () => {

resp = await process_text_API_TEST(text_recognition_url, text_recognition_image, headers)
console.log('\n!!!!!  translation results', resp[0].translations)


})()
