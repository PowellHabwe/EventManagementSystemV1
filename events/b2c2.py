from django.http import HttpResponse, JsonResponse
import requests
from requests.auth import HTTPBasicAuth
import json
import mpesa_credentials


# def b2c2():
#     access_token = mpesa_credentials.MpesaAccessToken.validated_mpesa_access_token
#     print(access_token)

#     headers = {"Authorization": "Bearer %s" % access_token}

#     payload = {
#         "InitiatorName": "testapi",
#         "SecurityCredential": "fEx8UNd5KeUEWwVS+h3gn5V2tI8YgiH81xDDBgJOgwpjZVj5LXQH5WjY+pzpHo+LHQNcoG+ACI3UH20fcpTvzvLDmY2N3I4E6XAUyJia6UCCFu52GUKw8+8XYZ5pR85r7F4SgwMDTDCmWWg42K/8fPCOy9uEpVnqBuQimikyEO1iijcg7R/i3t1PP9DTz0fr4tpnZxXG6NWxN3MALv07zEMYob1hk0PXi/0fGf0/VcE5+zZsz8Agkw9jLKtiqo46r75i9Bzfczi0LKp/vJaRyydg/ZCbXESpVSC+Ejm7l+E4oJRfNZlzsddEArzgrINDdZdTAh0AL9iH1hkxdzZzDQ==",
#         "CommandID": "BusinessPayment",
#         "Amount": 1,
#         "PartyA": 254708294284,
#         "PartyB": 254708294284,
#         "Remarks": "Test remarks",
#         "QueueTimeOutURL": "https://mydomain.com/b2c/queue",
#         "ResultURL": "https://mydomain.com/b2c/result",
#         "Occassion": "",
#     }
#     response = requests.request("POST", 'https://sandbox.safaricom.co.ke/mpesa/b2c/v1/paymentrequest', headers = headers, data = payload)
#     print(response)
# b2c2()

# create a post method whereby total money data is calculated for the organiser and he places in a special code,a uuid which when correct 
# calculates the total money he has and how much he can withdraw

def b2c():
    access_token = mpesa_credentials.MpesaAccessToken.validated_mpesa_access_token
    headers = {"Authorization": "Bearer %s" % access_token}

    payload = {
        "InitiatorName": "174379",
        "SecurityCredential": "EUcQ7s8TpoMWaiQDwQQdfAnKoLyXsc0+51b9oue7RaPNKl46EI6PFxuqcJLd7dYryVL3ZPLDLqKltxo6TeIcF3aDmhXlpdjjZ6YHzeTJK1s1yyVOUhVMM+Nouus5Hc3D22k3A3PSy67R/6fmYouNigyAK4qF3VirFurrNTr6erWxPBIuR/z8YRbaA0BRRkBB/fAam3z+ia0p2sv6cugfY+ONl+zsxsIIopRb9c4DZXzyw9TC0bfN4TYPxcglQgbnoyXYn4M4vLVtmD1Q5RRGuBjH+FcVFn0ROXqAU24PbOM9MkLqgr1DkrBoCU5BwdMiGlY2jbaVBWuIwYZp6uUQgg==",
        "CommandID": "BusinessPayment",
        "Amount": 1,
        "PartyA": 600989,
        "PartyB": 254708294284,
        "Remarks": "Test remarks",
        "QueueTimeOutURL": "https://7ae5-105-163-56-216.in.ngrok.io/b2c/queue",
        "ResultURL": "https://7ae5-105-163-56-216.in.ngrok.io/b2c/result",
        "Occassion": "",
    }
    response = requests.request("POST", 'https://sandbox.safaricom.co.ke/mpesa/b2c/v1/paymentrequest', headers = headers, json = payload)
    print(response.text.encode('utf8'))
b2c()