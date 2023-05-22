import requests
from json import dumps, loads
#API_KEY='gVksEoA6mzLbaLzPu7pyNSNQoa4Yr8Hj'

import requests

url = "https://api.ai21.com/studio/v1/j2-jumbo/complete"

def get_api_key(file:str):
  with open(file,'rt') as f:
     json = loads(f.read())
     return json['key']

API_KEY = get_api_key('api_key.json')

payload = {
    "numResults": 5,
    "maxTokens": 16,
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


if __name__ == "__main__":
  payload['prompt'] = 'who is batman'

  response = requests.post(url, json=payload, headers=headers)

  response = loads(response.text)

  prompt_text = response['prompt']['text']
  completions = response['completions']

  for completion in completions:
      result = completion['data']['text']
      print(result)

  print(dumps(loads(response.text), indent=2))
