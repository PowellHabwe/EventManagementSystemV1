from django.http import HttpResponse
import requests
from requests.auth import HTTPBasicAuth
import json


def getAccessToken1():
    consumer_key = 'hOUUrGCHFqNkkkAD9rxpY5nvffoj8wXs'
    consumer_secret = 'OA8VGTUikCtOE4yO'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']
    print(validated_mpesa_access_token)
    return (validated_mpesa_access_token)

getAccessToken1()