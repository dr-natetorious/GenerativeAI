#!/usr/bin/env python3
from os import environ
import requests
from typing import List
from json import loads
import streamlit as st
import boto3

KENDRA_INDEX = environ.get('KENDRA_INDEX', '85993151-b0a4-49ee-8144-d6d945981c89')
MODEL_API = environ.get('MODEL_URL', 'https://api.ai21.com/studio/v1/j2-jumbo-instruct/complete')

kendra = boto3.client('kendra', region_name='us-east-1')

def get_api_key(file:str):
  with open(file,'rt') as f:
     json = loads(f.read())
     return json['key']

API_KEY = get_api_key('../api_key.json')

def ask_kendra(q:str):
  response = kendra.query(
    IndexId=KENDRA_INDEX,
    QueryText=q)

  answers = []
  for result in response['ResultItems']:
    answers.append('Article: "%s" states: %s\n\n Uri: %s\n\n\#\#\#\n\n'% (
      result['DocumentTitle']['Text'], 
      result['DocumentExcerpt']['Text'].replace('\n',' '),
      result['DocumentURI']))

  st.write('\n'.join(answers))
  return answers

def ask_ai21(q:str, answers:List[str]):
  #st.write('%s' % '\n'.join(answers))
  payload = {
    "numResults": 5,
    "maxTokens": 200,
    "minTokens": 0,
    "temperature": 0.7,
    "topP": 1,
    "topKReturn": 0,
    "frequencyPenalty": {
        "scale": 1,
        "applyToWhitespaces": True,
        "applyToPunctuations": True,
        "applyToNumbers": True,
        "applyToStopwords": True,
        "applyToEmojis": True
    },
    "presencePenalty": {
        "scale": 0,
        "applyToWhitespaces": True,
        "applyToPunctuations": True,
        "applyToNumbers": True,
        "applyToStopwords": True,
        "applyToEmojis": True
    },
    "countPenalty": {
        "scale": 0,
        "applyToWhitespaces": True,
        "applyToPunctuations": True,
        "applyToNumbers": True,
        "applyToStopwords": True,
        "applyToEmojis": True
    }
  }
  headers = {
      "accept": "application/json",
      "content-type": "application/json",
      "Authorization": 'Bearer %s' % API_KEY
  }

  payload['prompt'] = '''
  %s
  Alice wants to "%s" which article should she read?
  Return only the Uri for that article  
  '''

  response = requests.post(MODEL_API, json=payload, headers=headers)  
  response = loads(response.text)

  completions = response['completions']
  st.write(completions)

  for completion in completions:
    result = completion['data']['text']
    st.write(result)


input = st.text_input("Ask Kendra", key='question')
answers = ask_kendra(input)
ask_ai21(input,answers)
