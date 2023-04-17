# import stripe
# from django.shortcuts import render, get_object_or_404
# from django.conf import settings
# from django.http import JsonResponse, HttpResponse
# from django.template.loader import get_template
# from django.views import View   
# from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
# from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# from django.contrib.auth.models import User
# stripe.api_key = settings.STRIPE_SECRET_KEY
# from django.http import FileResponse
# from .models  import Promise, MpesaPaymentCalls


# def postDetail1(request, pk):
    
#     mpesaresponse2 = {    
#         "Body": {        
#             "stkCallback": {            
#                 "MerchantRequestID": "29115-34620561-1",            
#                 "CheckoutRequestID": "ws_CO_191220191020363925",            
#                 "ResultCode": 0,            
#                 "ResultDesc": "The service request is processed successfully.",            
#                 "CallbackMetadata": {                
#                     "Item": [{                        
#                     "Name": "Amount",                        
#                     "Value": 1.00                    
#                     },                    
#                     {                        
#                     "Name": "MpesaReceiptNumber",                        
#                     "Value": "NLJ7RT61SV"                    
#                     },                    
#                     {                        
#                     "Name": "TransactionDate",                        
#                     "Value": 20191219102115                    
#                     },                    
#                     {                        
#                     "Name": "PhoneNumber",                        
#                     "Value": 254708374149                    
#                     }]            
#                 }        
#             }    
#         }
#     }
#     t = MpesaPaymentCalls.objects.get(id=6)
#     return HttpResponse(t)


#     # mpesaresponse2 = "https://2f10-41-90-42-204.in.ngrok.io/c2b/confirmation"
#     # print("trialresponse :", mpesaresponse2['Body'])
#     trialResponse = mpesaresponse2['Body']
#     stkCallback = trialResponse['stkCallback']
#     CallbackMetadata = stkCallback['CallbackMetadata']
#     Item = CallbackMetadata['Item']
#     AmountDict = Item[0]
#     Amount = AmountDict['Value']
#     MpesaReceiptNumberDict = Item[1]
#     MpesaReceiptNumber = MpesaReceiptNumberDict['Value']
#     TransactionDateDict = Item[2]
#     TransactionDate = TransactionDateDict['Value']
#     PhoneNumberDict = Item[3]
#     PhoneNumber = PhoneNumberDict['Value']
#     # print('Item :', Item)
#     MerchantRequestIDNew = stkCallback['MerchantRequestID']
#     CheckoutRequestIDNew = stkCallback['CheckoutRequestID']
#     ResultCode = stkCallback['ResultCode']
#     ResultDesc = stkCallback['ResultDesc']
#     # print("TransactionDate :", TransactionDate)


    # for merchantid in MpesaPaymentCalls.objects.get('MerchantRequestID'):
    #     if MerchantRequestIDNew == merchantid:
    #         updateLog = MpesaPaymentCalls.objects.get(id=54)
    #         payment_id = request.get('MerchantRequestID')
    #         # print('updateLog',updateLog.MerchantRequestID)
    #         updateLog.MerchantRequestID = MerchantRequestIDNew
    #         updateLog.CheckoutRequestID = CheckoutRequestIDNew
    #         updateLog.TransactionStatus2 = ResultCode
    #         updateLog.TransactionDescription2 = ResultDesc
    #         updateLog.ItemAmountPaid = Amount
    #         updateLog.ItemReceipt = MpesaReceiptNumber
    #         updateLog.PhoneNumber2 = PhoneNumber
    #         updateLog.ItemDate = TransactionDate
    #         updateLog.save()
    # else:
    #     pass






    #     # updateLog = MpesaPaymentCalls.objects.get(id=87)
    # # print('updateLog; ',updateLog)
    # # Data Extraction
    # mpesaresponse1 = request.body.decode('utf-8')
    # print('mpesaresponse1 :', mpesaresponse1)
    # mpesaresponse2 = json.loads(mpesaresponse1)
    # trialResponse = mpesaresponse2['Body']
    # stkCallback = trialResponse['stkCallback']
    # stk = mpesaresponse2['Body']['stkCallback']
    # CallbackMetadata = mpesaresponse2['Body']['stkCallback']['CallbackMetadata']
    # print('CallbackMetadata: ',CallbackMetadata)
    # # CallbackMetadata = stkCallback['CallbackMetadata']
    # # Item = CallbackMetadata['Item']
    # # AmountDict = Item[0]
    # # Amount = AmountDict['Value']
    # # MpesaReceiptNumberDict = Item[1]
    # # MpesaReceiptNumber = MpesaReceiptNumberDict['Value']
    # # TransactionDateDict = Item[2]
    # # # TransactionDate = TransactionDateDict['Value']
    # # PhoneNumberDict = Item[3]
    # # PhoneNumber = PhoneNumberDict['Value']
    # # MerchantRequestIDNew = stkCallback['MerchantRequestID']
    # # CheckoutRequestIDNew = stkCallback['CheckoutRequestID']
    # # ResultCode = stkCallback['ResultCode']
    # # ResultDesc = stkCallback['ResultDesc']
    # # print('CallbackMetadata; ',CallbackMetadata)


# COPY EVERYTHING

@csrf_exempt
def confirmation(request):
    # updateLog = MpesaPaymentCalls.objects.get(id=87)
    # print('updateLog; ',updateLog)
    # Data Extraction
    mpesaresponse1 = request.body.decode('utf-8')
    print('mpesaresponse1 :', mpesaresponse1)
    mpesaresponse2 = json.loads(mpesaresponse1)
    trialResponse = mpesaresponse2['Body']
    stkCallback = trialResponse['stkCallback']
    stk = mpesaresponse2['Body']['stkCallback']
    ResultCode = mpesaresponse2['Body']['stkCallback']['ResultCode']
    MerchantRequestIDNew = mpesaresponse2['Body']['stkCallback']['MerchantRequestID']
    CheckoutRequestIDNew = mpesaresponse2['Body']['stkCallback']['CheckoutRequestID']
    ResultDesc = mpesaresponse2['Body']['stkCallback']['ResultDesc']
    CallbackMetadata = stkCallback['CallbackMetadata']
    Item = CallbackMetadata['Item']
    AmountDict = Item[0]
    Amount = AmountDict['Value']
    MpesaReceiptNumberDict = Item[1]
    MpesaReceiptNumber = MpesaReceiptNumberDict['Value']
    TransactionDateDict = Item[2]
    # TransactionDate = TransactionDateDict['Value']
    PhoneNumberDict = Item[3]
    PhoneNumber = PhoneNumberDict['Value']
    # MerchantRequestIDNew = stkCallback['MerchantRequestID']
    # CheckoutRequestIDNew = stkCallback['CheckoutRequestID']
    # ResultCode = stkCallback['ResultCode']
    # ResultDesc = stkCallback['ResultDesc']
    print('CallbackMetadata; ',CallbackMetadata)

    reqid = MpesaPaymentCalls.objects.all().filter(CheckoutRequestID =  CheckoutRequestIDNew).values()
    print('reqid: ',reqid)
    reqid.update(
    MerchantRequestID = MerchantRequestIDNew,
    CheckoutRequestID = CheckoutRequestIDNew,
    TransactionStatus2 = ResultCode,
    TransactionDescription2 = ResultDesc,
    ItemAmountPaid = Amount,
    ItemReceipt = MpesaReceiptNumber,
    PhoneNumber2 = PhoneNumber,
    # ItemDate = TransactionDate,
    )

    # mpesacalls = MpesaPaymentCalls.objects.all()
    # print(mpesacalls)
    # reqid = MpesaPaymentCalls.objects.all().filter(CheckoutRequestID='ws_CO_26082022210007507708294284').values()
    # print('reqid :', reqid)
    # print('reqidID :', reqid['id'])


@csrf_exempt
def confirmation(request):
    # updateLog = MpesaPaymentCalls.objects.get(id=87)
    # print('updateLog; ',updateLog)
    # Data Extraction
    mpesaresponse1 = request.body.decode('utf-8')
    print('mpesaresponse1 :', mpesaresponse1)
    mpesaresponse2 = json.loads(mpesaresponse1)
    trialResponse = mpesaresponse2['Body']
    stkCallback = trialResponse['stkCallback']
    stk = mpesaresponse2['Body']['stkCallback']
   
    # MerchantRequestIDNew = mpesaresponse2['Body']['stkCallback']['MerchantRequestID']
    # CheckoutRequestIDNew = mpesaresponse2['Body']['stkCallback']['CheckoutRequestID']
    # ResultDesc = mpesaresponse2['Body']['stkCallback']['ResultDesc']
    # ResultCode = mpesaresponse2['Body']['stkCallback']['ResultCode']
    # ItemAmountPaid = mpesaresponse2['Body']['stkCallback']['CallbackMetadata']['Item'][0]['Value']
    # ItemReceipt = mpesaresponse2['Body']['stkCallback']['CallbackMetadata']['Item'][1]['Value']
    # PhoneNumber2 = mpesaresponse2['Body']['stkCallback']['CallbackMetadata']['Item'][3]['Value']
    # CallbackMetadata = stkCallback['CallbackMetadata']
    # Item = CallbackMetadata['Item']
    # AmountDict = Item[0]
    # Amount = AmountDict['Value']
    # MpesaReceiptNumberDict = Item[1]
    # MpesaReceiptNumber = MpesaReceiptNumberDict['Value']
    # TransactionDateDict = Item[2]
    # # TransactionDate = TransactionDateDict['Value']
    # PhoneNumberDict = Item[3]
    # PhoneNumber = PhoneNumberDict['Value']
    # MerchantRequestIDNew = stkCallback['MerchantRequestID']
    # CheckoutRequestIDNew = stkCallback['CheckoutRequestID']
    # ResultCode = stkCallback['ResultCode']
    # ResultDesc = stkCallback['ResultDesc']
    # print('CallbackMetadata; ',CallbackMetadata)

    reqid = MpesaPaymentCalls.objects.all().filter(CheckoutRequestID =  mpesaresponse2['Body']['stkCallback']['CheckoutRequestID']).values()
    print('reqid: ',reqid)
    reqid.update(
    MerchantRequestID = mpesaresponse2['Body']['stkCallback']['MerchantRequestID'],
    CheckoutRequestID = mpesaresponse2['Body']['stkCallback']['CheckoutRequestID'],
    TransactionStatus2 = mpesaresponse2['Body']['stkCallback']['ResultCode'],
    TransactionDescription2 = mpesaresponse2['Body']['stkCallback']['ResultDesc'],
    ItemAmountPaid = mpesaresponse2['Body']['stkCallback']['CallbackMetadata']['Item'][0]['Value'],
    ItemReceipt =  mpesaresponse2['Body']['stkCallback']['CallbackMetadata']['Item'][1]['Value'],
    PhoneNumber2 =  mpesaresponse2['Body']['stkCallback']['CallbackMetadata']['Item'][3]['Value'],
    # ItemDate = TransactionDate,
    )

    # mpesacalls = MpesaPaymentCalls.objects.all()
    # print(mpesacalls)
    # reqid = MpesaPaymentCalls.objects.all().filter(CheckoutRequestID='ws_CO_26082022210007507708294284').values()
    # print('reqid :', reqid)
    # print('reqidID :', reqid['id'])




    # # Data Update
    # for merchant in MpesaPaymentCalls.objects.all():
    #     checkout = merchant.CheckoutRequestID
    #     print(checkout)
    #     if checkout == MerchantRequestIDNew:
    #         updateLog = MpesaPaymentCalls.objects.get(checkout == MerchantRequestIDNew)
    # reqid = MpesaPaymentCalls.objects.all().filter(CheckoutRequestID='ws_CO_26082022210007507708294284')
    # print('reqid :', reqid)
    # print('reqid :', reqid[0])
    # reqid = MpesaPaymentCalls.objects.all().filter(CheckoutRequestID='ws_CO_26082022210007507708294284')
    # print('reqid :', reqid.values_list())
    # print('reqid :', reqid[0])

        # updateLog = MpesaPaymentCalls.objects.get(id=54)
    # payment_id = request.get('MerchantRequestID')
    # qs.update(active=False, is_deleted=True, date_finished=timezone.now())
    # print('updateLog',updateLog.MerchantRequestID)
    # updateLog.MerchantRequestID = MerchantRequestIDNew
    # updateLog.CheckoutRequestID = CheckoutRequestIDNew
    # updateLog.TransactionStatus2 = ResultCode
    # updateLog.TransactionDescription2 = ResultDesc
    # updateLog.ItemAmountPaid = Amount
    # updateLog.ItemReceipt = MpesaReceiptNumber
    # updateLog.PhoneNumber2 = PhoneNumber
    # updateLog.ItemDate = TransactionDate
    # updateLog.save()

    # mpesa_payment = json.loads(mpesaresponse2)
    # print('mpesa_payment:', mpesa_payment)

    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }

    return JsonResponse(dict(context))



IMPORTANT STUFF

def getAccessToken1():
    consumer_key = 'hOUUrGCHFqNkkkAD9rxpY5nvffoj8wXs'
    consumer_secret = 'OA8VGTUikCtOE4yO'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    r = requests.get(api_URL, auth=HTTPBasicAuth(
        consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']
    print(validated_mpesa_access_token)
    return (validated_mpesa_access_token)


# def lipa_na_mpesa_online(request, *args, **kwargs):
def lipa_na_mpesa_online(request):
    # Prepopulate the amount
    access_token = MpesaAccessToken.validated_mpesa_access_token
    print(access_token)
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": "Bearer %s" % access_token}
    request = {
        "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
        "Password": LipanaMpesaPpassword.decode_password,
        "Timestamp": LipanaMpesaPpassword.lipa_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": 1,
        "PartyA": 254708294284,  # replace with your phone number to get stk push
        "PartyB": LipanaMpesaPpassword.Business_short_code,
        "PhoneNumber": 254708294284,  # replace with your phone number to get stk push
        # "CallBackURL": "https://a940-102-167-63-17.eu.ngrok.io/api/v1/c2b/confirmation",
        "CallBackURL": "https://a940-102-167-63-17.eu.ngrok.io/c2b/confirmation",
        # "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
        "AccountReference": "Powell",
        "TransactionDesc": "Testing stk push"
    }
    # BusinessShortCode = request.BusinessShortCode
    BusinessShortCode = request['BusinessShortCode']
    Timestamp = request['Timestamp']
    TransactionType = request['TransactionType']
    Amount = request['Amount']
    PartyA = request['PartyA']
    PartyB = request['PartyB']
    PhoneNumber = request['PhoneNumber']
    AccountReference = request['AccountReference']
    # TransactionDescription = request['TransactionDesc']

    # REALTHING
    response = requests.post(api_url, json=request, headers=headers)
    response = response.json()
    print('Mresponse :', 'Success. Request accepted for processing')
    # REALTHINGEND

    MerchantRequestID = response['MerchantRequestID']
    CheckoutRequestID = response['CheckoutRequestID']
    ResponseCode = response['ResponseCode']
    ResponseDescription = response['ResponseDescription']
    CustomerMessage = response['CustomerMessage']

    # mpesacalls = MpesaPaymentCalls.objects.filter(CheckoutRequestID)
    # print(mpesacalls)


    MpesaPaymentCalls.objects.create(
        BusinessShortCode = BusinessShortCode,
        Timestamp = Timestamp,
        TransactionType = TransactionType,
        Amount = Amount,
        PartyA = PartyA,
        PartyB = PartyB,
        PhoneNumber = PhoneNumber,
        AccountReference = AccountReference,
    
        MerchantRequestID=MerchantRequestID,
        CheckoutRequestID=CheckoutRequestID,
        TransactionStatus1=ResponseCode,
        TransactionDescription1=ResponseDescription,
        CustomerMessage=CustomerMessage,
    )

    # for merchant in MpesaPaymentCalls.objects.all():
    #     checkout = merchant.CheckoutRequestID
    #     print(checkout.id)
    # reqid = MpesaPaymentCalls.objects.all().filter(CheckoutRequestID='ws_CO_26082022210007507708294284')
    # print('reqid :', reqid.values_list())
    # print('reqid :', reqid[0])

    return HttpResponse('success')


@csrf_exempt
def register_urls(request):
    access_token = MpesaAccessToken.validated_mpesa_access_token

    api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    headers = {"Authorization": "Bearer %s" % access_token}
    options = {"ShortCode": LipanaMpesaPpassword.Business_short_code,
               "ResponseType": "Completed",
            #    "ConfirmationURL": "https://a940-102-167-63-17.eu.ngrok.io/api/v1/c2b/confirmation",
               "ConfirmationURL": "https://a940-102-167-63-17.eu.ngrok.io/c2b/confirmation",
               "ValidationURL": "https://a940-102-167-63-17.eu.ngrok.io/api/v1/c2b/validation"}
    response = requests.post(api_url, json=options, headers=headers)
    return HttpResponse(response.text)


@csrf_exempt
def call_back(request):
    pass


@csrf_exempt
def validation(request):
    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }
    return JsonResponse(dict(context))



@csrf_exempt
def confirmation(request):
    # updateLog = MpesaPaymentCalls.objects.get(id=11)
    # print('updateLog; ',updateLog)
    # Data Extraction
    mpesaresponse1 = request.body.decode('utf-8')
    print('mpesaresponse1 :', mpesaresponse1)
    mpesaresponse2 = json.loads(mpesaresponse1)
    print('mpesaresponse2 :', mpesaresponse2)

    trialResponse = mpesaresponse2['Body']
    stkCallback = trialResponse['stkCallback']
    stk = mpesaresponse2['Body']['stkCallback']
    print('stk :', stk)

   
    reqid = MpesaPaymentCalls.objects.all().filter(CheckoutRequestID =  mpesaresponse2['Body']['stkCallback']['CheckoutRequestID']).values()
    print('reqid: ',reqid)
    if mpesaresponse2['Body']['stkCallback']['ResultDesc'] == 'Request cancelled by user':
        reqid.update(
            MerchantRequestID = mpesaresponse2['Body']['stkCallback']['MerchantRequestID'],
            CheckoutRequestID = mpesaresponse2['Body']['stkCallback']['CheckoutRequestID'],
            TransactionStatus2 = mpesaresponse2['Body']['stkCallback']['ResultCode'],
            TransactionDescription2 = mpesaresponse2['Body']['stkCallback']['ResultDesc'],
            ItemAmountPaid = '0',
            ItemReceipt =  'No Receipt due to cancellation',
            PhoneNumber2 =  'Phone Number',
            
        )

            #     reqid.update(
            # MerchantRequestID = mpesaresponse2['Body']['stkCallback']['MerchantRequestID'],
            # CheckoutRequestID = mpesaresponse2['Body']['stkCallback']['CheckoutRequestID'],
            # TransactionStatus2 = mpesaresponse2['Body']['stkCallback']['ResultCode'],
            # TransactionDescription2 = mpesaresponse2['Body']['stkCallback']['ResultDesc'],
            # ItemAmountPaid = mpesaresponse2['Body']['stkCallback']['CallbackMetadata']['Item'][0]['Value'],
            # ItemReceipt =  mpesaresponse2['Body']['stkCallback']['CallbackMetadata']['Item'][1]['Value'],
            # PhoneNumber2 =  mpesaresponse2['Body']['stkCallback']['CallbackMetadata']['Item'][3]['Value'],
            # )


    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }

    return JsonResponse(dict(context))



import requests
​
headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Bearer AKwGE4xAm80AK1pwHwlR6PcrBBe1'
}
​
payload = {
    "BusinessShortCode": 174379,
    "Password": "MTc0Mzc5YmZiMjc5ZjlhYTliZGJjZjE1OGU5N2RkNzFhNDY3Y2QyZTBjODkzMDU5YjEwZjc4ZTZiNzJhZGExZWQyYzkxOTIwMjIwOTIyMDEyNTEz",
    "Timestamp": "20220922012513",
    "TransactionType": "CustomerPayBillOnline",
    "Amount": 1,
    "PartyA": 254708374149,
    "PartyB": 174379,
    "PhoneNumber": 254708374149,
    "CallBackURL": "https://mydomain.com/path",
    "AccountReference": "CompanyXLTD",
    "TransactionDesc": "Payment of X" 
  }
​
response = requests.request("POST", 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest', headers = headers, data = payload)
print(response.text.encode('utf8'))

def b2c(request):
    if request.method == 'POST':

        access_token = MpesaAccessToken.validated_mpesa_access_token
        api_url = 'https://sandbox.safaricom.co.ke/mpesa/b2c/v1/paymentrequest'
        headers = {"Authorization": "Bearer %s" % access_token}
        request = {
            "InitiatorName": "testapi",
            "SecurityCredential": "dcQUsiygneUJFnAU8sRkkKlkBD9YU7x21XAHkLvytcw8ZLsU+5/h2p8+rIqVZHzrXPxvfqyfV3MqvzjxvqiYK9az7lE1rweIbacVWEFQvdi6Ty0UXxyrXajuJi7BcHMMHBz7y6RMfeO51jEGidUAXYoQV+1f1J582JBvBDPykJaj4Iv3/paMxi9lgM4FspeK/sq2JFR9b+Ixhm0EB5CRuZcRgAYEUokaf4hhvIQ5uhZWh9AM0Svqlb3CCvABiEx1stXEdBg/vaIyUWGKQQk2rdg5InL9q8TFxDljQlk+uiNBdonsY9VSiA/+ZpcuunvGE6zPFMAstkMq3mqV8eEcEw==",
            "CommandID": "BusinessPayment",
            "Amount": 1,
            "PartyA": 254708294284,
            "PartyB": 254759727082,
            "Remarks": "Test remarks",
            "QueueTimeOutURL": "https://bbe5-102-167-105-38.in.ngrok.io/c2b/confirmation",
            "ResultURL": "https://bbe5-102-167-105-38.in.ngrok.io/c2b/confirmation",
            "Occassion": "Business",
        }

        response = requests.post(api_url, json=request, headers=headers)
        return HttpResponse('This is a successfull b2c payment')



import requests
​
response = requests.request("GET", 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials', headers = { 'Authorization': 'Bearer cFJZcjZ6anEwaThMMXp6d1FETUxwWkIzeVBDa2hNc2M6UmYyMkJmWm9nMHFRR2xWOQ==' })
print(response.text.encode('utf8'))
# def b2c(request):
#     if request.method == 'POST':
#         access_token = MpesaAccessToken.validated_mpesa_access_token
#         headers = {"Authorization": "Bearer %s" % access_token}

#         form = B2C(request.POST)

#         phone_no = request.POST['phone_no']
#         amount = request.POST['amount']
#         withdrawal_id = request.POST['withdrawal_id']

#         payload = {
#             "InitiatorName": "testapi",
#             "SecurityCredential": "JqXQiIef4VH4dTKoPGUNJ/loiV9zzCAvYXFBGzgsR81URN9dikUD0THOe8mDuRXrvEUh8eqqvpQUsPxSp8bhIxL7W+qSNyK+Spk5JhrKW3AO099nJ513JmiPw5lVtD1C4Pzhqgw98yNlYdr/VvGhz4IdKZMFdL5xp3jzx7kHV6uhZx0Poc4uv8QOZKjlRaz0gzKA5aSqPHMAQsTbEMB03O7yGlFwzRvHNoZyDp3jzO4xKUiQrNQsPuzrw8iemiDVHQgIsgyFv8v5rDxCqi5BsceWtH3JFOIKAdQTRCa06pyKF1layfUuZCZV8CDkQoQuPImfwT68i75FTixDpKi1oA==",
#             "CommandID": "BusinessPayment",
#             "Amount": 1,
#             "PartyA": 600995,
#             "PartyB": 254708294284,
#             "Remarks": "Test remarks",
#             "QueueTimeOutURL": "https://7ae5-105-163-56-216.in.ngrok.io/b2c/queue",
#             "ResultURL": "https://7ae5-105-163-56-216.in.ngrok.io/b2c/result",
#             "Occassion": "",
#         }
        
#         response = requests.request("POST", 'https://sandbox.safaricom.co.ke/mpesa/b2c/v1/paymentrequest', headers = headers, json = payload)
#         print(response.text.encode('utf8'))
#     else:
#         form = B2C()
#     context = {'form' : form}

#     return render(request, 'events/withdraw.html', context)
