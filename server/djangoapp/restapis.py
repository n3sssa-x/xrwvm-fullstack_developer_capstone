# Uncomment the imports below before you add the function code
import requests
import os
from dotenv import load_dotenv
from django.conf import settings

load_dotenv()

backend_url = os.getenv('backend_url', default="http://localhost:3030")
sentiment_analyzer_url = os.getenv('sentiment_analyzer_url', default="http://localhost:5050/")

def get_request(endpoint, **kwargs):
    params = ""
    if kwargs:
        for key, value in kwargs.items():
            params = params + key + "=" + value + "&"

    # avoid adding a stray ? when there are no params
    request_url = backend_url + endpoint
    if params:
        request_url = request_url + "?" + params

    print("GET from {} ".format(request_url))
    try:
        response = requests.get(request_url)
        response.raise_for_status()
        return response.json()
    except Exception as err:
        # Log and return None so callers can handle it
        print("Network exception occurred while calling", request_url, ":", err)
        return None

def analyze_review_sentiments(text):
    request_url = sentiment_analyzer_url.rstrip("/") + "/analyze/" + text
    try:
        response = requests.get(request_url)
        response.raise_for_status()
        return response.json()
    except Exception as err:
        print(f"Sentiment analyzer error while calling {request_url}: {err}")
        # Return a neutral sentiment if sentiment microservice is unavailable
        return {"sentiment": "neutral"}

def post_review(data_dict):
    request_url = backend_url.rstrip("/") + "/insert_review"
    try:
        response = requests.post(request_url, json=data_dict)
        response.raise_for_status()
        print(response.json())
        return response.json()
    except Exception as err:
        print("Network exception occurred while posting to", request_url, ":", err)
        return None
