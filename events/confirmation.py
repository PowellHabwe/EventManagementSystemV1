# @csrf_exempt
# def confirmation(request):
#     mpesa_body =request.body.decode('utf-8')
#     print('mpesa_body:', mpesa_body)
#     mpesa_payment = json.loads(mpesa_body)
#     print('mpesa_payment:', mpesa_payment)
#     payment = MpesaPaymentCalls(
#         first_name=mpesa_payment['FirstName'],
#         last_name=mpesa_payment['LastName'],
#         middle_name=mpesa_payment['MiddleName'],
#         description=mpesa_payment['TransID'],
#         phone_number=mpesa_payment['MSISDN'],
#         amount=mpesa_payment['TransAmount'],
#         reference=mpesa_payment['BillRefNumber'],
#         organization_balance=mpesa_payment['OrgAccountBalance'],
#         type=mpesa_payment['TransactionType'],
#     )
#     payment.save()
#     context = {
#         "ResultCode": 0,
#         "ResultDesc": "Accepted"
#     }

#     return JsonResponse(dict(context))

import requests
​
headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Bearer MeSU9F7yFUA5qvAab4UmrEIPtBmH'
}
​
payload = {
    "InitiatorName": "testapi",
    "SecurityCredential": "o89xaaanosDgIVVd90ioBN5Ku3DS6QWWZc3ZrVz/ibC8N1vq0KTxZeowYxmO8lzmUyKfq/Yo+CHTjsbRxGPssGBPpcodlZkaqgL3n2BgLWLYRyL/FTSDVq1MDe++0mfjp9N1DqGTjRGZS6+Kn0Whk0+BMaqYRCXos8FrWjC+C2jBI2sK5DyN1OYZz9wSPZWGBLivfxTtR+qzl8unoeO1GEeaBCKNtrzYIH9O4yiV+1nl8M/8SCcYLa6wuFxn3EWRHMFcd3Ilo54YBYA172Nu2nT4x+Hr9x3DWyYJJqERUDHl7gePutuypIJpRrrXyVBMb3/2edSLNsTdoEvlfbI7iQ==",
    "CommandID": "BusinessPayment",
    "Amount": 1,
    "PartyA": 600995,
    "PartyB": 254708374149,
    "Remarks": "Test remarks",
    "QueueTimeOutURL": "https://mydomain.com/b2c/queue",
    "ResultURL": "https://mydomain.com/b2c/result",
    "Occassion": "",
  }
​
response = requests.request("POST", 'https://sandbox.safaricom.co.ke/mpesa/b2c/v1/paymentrequest', headers = headers, data = payload)
print(response.text.encode('utf8'))