from django.http import HttpResponse, JsonResponse
import requests
from requests.auth import HTTPBasicAuth
import json
import mpesa_credentials
from django.views.decorators.csrf import csrf_exempt

def transactionStatus():
    access_token = mpesa_credentials.MpesaAccessToken.validated_mpesa_access_token
    headers = {"Authorization": "Bearer %s" % access_token}
    api_url = "https://sandbox.safaricom.co.ke/mpesa/transactionstatus/v1/query"
    request = {
        "Initiator": "testapi",
        "SecurityCredential": "SKXjJo1n7pfrFyr2dCFGSz/YOdpPkPPg87Cp/6kJ68pdjFqGdVJkdpdKVfwV8KBMVjpwAhZepN7X7yKh+EZ+BqIanTJhr4NTrVRxk+K6mNQl2x46UiedKprdoY5nd7yW/xAco4g2qY9TNnob91cLKuNIQTAerfBMwLqiIH0ZH+1Rwq8AOiujqkfcikzTRB/qpzhS/IHZFsAvBtWNg1eu46Jrf2P0WVE//OGDbVPw4NNs5PVFiRzzPTmdOzVCH/phq5GEVfUfvbJ3su0tXH7zetGh4bgG6MPp/P/xvbjScAdsP/WHXPDz7V3QHipEz+rr50cfCX5awiLKB6dUOqwq3w==",
        "CommandID": "TransactionStatusQuery",
        "TransactionID": "OEI2AK4Q16",
        "PartyA": 600980,
        "IdentifierType": "2",
        "ResultURL": "https://mydomain.com/TransactionStatus/result/",
        "QueueTimeOutURL": "https://mydomain.com/TransactionStatus/queue/",
        "Remarks": "here",
        "Occassion": "here",
    }

    response = requests.post(api_url, headers = headers, json=request)
    print(response.text)

transactionStatus()
