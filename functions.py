import requests
import os
import urllib
from datetime import datetime
import random

def get_intent(key, url, query):

    params = urllib.parse.urlencode({"query": query})

    response = requests.get(url + params)

    data = response.json()
    intents = data['prediction']['intents']
    score_max = 0
    if 'ville' in data['prediction']['entities'].keys():
        entity = data['prediction']['entities']['ville'][0]
    else:
        entity = "No entity"
    for intent in intents:
        score = intents[intent]['score']
        if score > score_max:
            score_max = score
            most_likely_intent = intent
    return {
        'intent': most_likely_intent,
        'score': score_max,
        'entity': entity,
    }

def get_temp(key, city):

    response = requests.post(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}")
    response = response.json()
    if 'main' in response.keys():
        temp = response["main"]["temp"] - 273.15
    else:
        temp = "Bad request"
    return {
        'city': city,
        'temp': temp,
    }

def get_sunset(key, city):

    response = requests.post(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}")
    data = response.json()
    datetime.fromtimestamp(1172969203.1)
    sunset = datetime.fromtimestamp(data['sys']['sunset'])
    return {
        'city': city,
        'sunset': f"{sunset:%Y-%m-%d %H:%M:%S}",
    }

def select_learner(learners):
    return random.choice(learners)