from django.http import HttpResponse, JsonResponse
import requests
from requests.auth import HTTPBasicAuth
import json
import mpesa_credentials

def account_balance():
    access_token = mpesa_credentials.MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/accountbalance/v1/query"
    headers = {"Authorization": "Bearer %s" % access_token}
    request = {
    "Initiator": "testapi",
    "SecurityCredential": "Uz7qxC/6ARolcxufaFsD6U6Cp91TV4QVcrw5C0z8KrlD2/5P2RK8aLzJD/PPAQzWQ3p6aSXuCpTIhBiZlxxz75WpJropHUfKbIsNO/yB+BACte9P+4w5dGZC2F+rZNsG/xapeNfCQnbWKQCIOjM3OGqQrgRIa4jXq7dQD94GA2u8d5ClbCPmGII0KZfUKaYAYrdSHLTDd/e59JBYThOvXLzCsYnUHYGJPxPtwJtl52zQWGVNVFRgiNVEkxVd1XOnH116kwpbm7ewTWUtJWFOl7MpK+EJdC6Sa6cRGFDOR5EV+A3CUiWVc3L3ukZwLu5ilDIyGBNJpDZsSlvITkG0nQ==",
    "CommandID": "AccountBalance",
    "PartyA": 600977,
    "IdentifierType": "4",
    "Remarks": "Test",
    "QueueTimeOutURL": "https://mydomain.com/AccountBalance/queue/",
    "ResultURL": "https://mydomain.com/AccountBalance/result/",
    }
    response = requests.post(api_url, headers = headers, json=request)
    print(response.text)
account_balance()