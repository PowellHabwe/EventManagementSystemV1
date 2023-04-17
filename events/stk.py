from django.http import HttpResponse, JsonResponse
import requests
from requests.auth import HTTPBasicAuth
import json
import mpesa_credentials

def lipa_na_mpesa_online():
    access_token = mpesa_credentials.MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": "Bearer %s" % access_token}
    request = {
        "BusinessShortCode": mpesa_credentials.LipanaMpesaPpassword.Business_short_code,
        "Password": mpesa_credentials.LipanaMpesaPpassword.decode_password,
        "Timestamp": mpesa_credentials.LipanaMpesaPpassword.lipa_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": 1,
        "PartyA": 254708294284,  # replace with your phone number to get stk push
        "PartyB": mpesa_credentials.LipanaMpesaPpassword.Business_short_code,
        "PhoneNumber": 254708294284,  # replace with your phone number to get stk push
        "CallBackURL": "https://fcc6-41-90-42-204.in.ngrok.io/api/v1/c2b/confirmation",
        "AccountReference": "Powell",
        "TransactionDesc": "Testing stk push"
    }
    response = requests.post(api_url, json=request, headers=headers)
    json_data = response.json()
    print('json_data:', json_data)
    mpesa_response1 = json.loads(response.text)
    print('mpesa_response1:', mpesa_response1)
    return(mpesa_response1)

lipa_na_mpesa_online()
