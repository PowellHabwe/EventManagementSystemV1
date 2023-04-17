from . mpesa_credentials import MpesaAccessToken, LipanaMpesaPpassword
import json
from django.db.models import Sum
from django.http import HttpRequest
from requests.auth import HTTPBasicAuth
import requests
from django.http import HttpResponse, JsonResponse
from .models import MpesaPayment
from django.views.decorators.csrf import csrf_exempt

from .forms import PromiseForm, ConfirmForm, TicketOrder, StkInfo, StkCall,B2C,EventTotals

from .models import EventTotals2, B2CModel, ExistingReceipt, TicketOrder,Promise, MpesaPaymentCalls, MpesaConfirmation, OrganiserCut, CompanyCut
from django.http import FileResponse
import stripe
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Ticket_info
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.template.loader import get_template
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
stripe.api_key = settings.STRIPE_SECRET_KEY

# mpesa
# customise input


class PromiseCreateView(CreateView):
    model = Promise
    form_class = PromiseForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# Create your views here.


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'events/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'events/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'events/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


def PostDetailView(request, pk):
    post = Post.objects.get(id = pk)
    context = {
        'post':post, 

    }
    return render(request, 'events/post_detail.html', context)


def TicketConfirmation(request, *args, **kwargs):

    if request.method == 'POST':
        # pk = self.kwargs.get('pk')
        form = ConfirmForm(request.POST)
        mpesa_receipt = request.POST['mpesa_receipt']
        ticket_no = request.POST['ticket_no']
        if form.is_valid():
            exists = ExistingReceipt.objects.filter(receipt = mpesa_receipt).exists()
            
            check_existing = MpesaPaymentCalls.objects.filter(ItemReceipt= mpesa_receipt).exists()
            pk = get_object_or_404(Ticket_info, pk=ticket_no)
            if check_existing and not exists:
                ExistingReceipt.objects.create(
                    receipt = mpesa_receipt
                )
                return redirect("ticket_detail", pk=request.POST['ticket_no'])
            else:
                return HttpResponse("Not Found / You have already used that receipt")
    else:
        form = ConfirmForm()
    context = {'form' : form}

    return render(request, 'events/mpesaconf.html', context)


class MpesaCreateView(LoginRequiredMixin, CreateView,):
    # model = MpesaConfirmation
    template_name = 'events/mpesaconf.html'
    form_class = ConfirmForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'price', 'header_image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TicketCreateView(LoginRequiredMixin, CreateView,):
    model = Ticket_info
    form_class = PromiseForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'events/about.html', {'title': 'About'})

def detailtry(request):
    return render(request, 'events/post_detail3.html', {'title': 'About'})


def cancel(request):
    return render(request, 'events/cancel.html', {'title': 'Cancel'})


def success(request):
    return render(request, 'events/about.html', {'title': 'Success'})


def TicketDetailView(request, pk):
    ticket = Ticket_info.objects.get(pk=pk)
    context = {
        'ticket': ticket
    }

    return render(request, 'events/ticket.html', context)


def TicketDetailView1(request, pk):
    ticket = Ticket_info.objects.get(pk=pk)
    context = {
        'ticket': ticket
    }

    return render(request, 'events/ticket1.html', context)

def TicketOrder(request):
    form = TicketOrder
    if request.POST:
        mpesareceipt = request.POST['mpesareceipt']
        ticketname = request.POST['ticketname']
        form = TicketOrder(request.POST)
        if form.is_valid():
            check_existing = MpesaPaymentCalls.objects.filter(ItemReceipt= request.POST['mpesareceipt'])
            if check_existing:
                return redirect(home)
            else:
                form.save()
                return HttpResponse("Not Found")

    # else:
    #     form = TicketOrder()
    return render(request, 'events/order.html', {'form':form})

# MPESA PAYMENT LOGIC


def getAccessToken(request):
    consumer_key = 'SWuCQTpBbVNDjLHiEGd3RvAJ89GPtsWa'
    consumer_secret = 'Ffc2GGWRrwBXCi6S'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']
    print(validated_mpesa_access_token)
    return HttpResponse(validated_mpesa_access_token)


def postDetail(request, pk):
    post = Post.objects.get(id=pk)
    context = {
        'post':post, 

        }
    return render(request, 'events/home.html', context)

def StkInfo(request):

    if request.method == 'POST':
        
        form = StkCall(request.POST)
        ticket_title = request.POST['ticket_title']
        number_receiving = request.POST['phone_number']
        access_token = MpesaAccessToken.validated_mpesa_access_token
        # print(access_token)
        # prepopulate = Post.objects.all()
        prepopulate = Post.objects.all().filter(title = ticket_title).values()
        # print(prepopulate)
        # print("prepopulate: ",prepopulate[0]['author_id'])
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}
        payload = {
            "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
            "Password": LipanaMpesaPpassword.decode_password,
            "Timestamp": LipanaMpesaPpassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            # "Amount": 1,
            "Amount": prepopulate[0]['price'],
            "PartyA": number_receiving,  # replace with your phone number to get stk push
            "PartyB": LipanaMpesaPpassword.Business_short_code,
            "PhoneNumber": 254708294284,  # replace with your phone number to get stk push
            # "CallBackURL": "https://www.linkedin.com/in/powell-habwe-558b36230/",
            "CallBackURL": "https://b73c-41-90-62-196.in.ngrok.io/c2b/callback",
            # "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
            "AccountReference": "Powell",
            "TransactionDesc": "Testing stk push"
        }
        BusinessShortCode = payload['BusinessShortCode']
        Timestamp = payload['Timestamp']
        TransactionType = payload['TransactionType']
        Amount = payload['Amount']
        PartyA = payload['PartyA']
        PartyB = payload['PartyB']
        PhoneNumber = payload['PhoneNumber']
        AccountReference = payload['AccountReference']
        # TransactionDescription = request['TransactionDesc']

        response = requests.post(api_url, json=payload, headers=headers)
        response = response.json()
        print('Mpesaresponse :', response)

        MerchantRequestID = response['MerchantRequestID']
        CheckoutRequestID = response['CheckoutRequestID']
        ResponseCode = response['ResponseCode']
        ResponseDescription = response['ResponseDescription']
        CustomerMessage = response['CustomerMessage']


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
            
            Event_title = prepopulate[0]['title'],
            Event_price = prepopulate[0]['price'],
            Withdrawal_code = prepopulate[0]['uuid']
        )
        EventTotals2.objects.create (
            owner = prepopulate[0]['author_id'],
            checkoutRequestID = CheckoutRequestID
        )

        # for merchant in MpesaPaymentCalls.objects.all():
        #     checkout = merchant.CheckoutRequestID
        #     print(checkout.id)
        # reqid = MpesaPaymentCalls.objects.all().filter(CheckoutRequestID='ws_CO_26082022210007507708294284')
        # print('reqid :', reqid.values_list())
        # print('reqid :', reqid[0])

    else:
        form = StkCall()
    context = {'form' : form}

    return render(request, 'events/stkinfo.html', context)


@csrf_exempt
def register_urls(request):
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    headers = {"Authorization": "Bearer %s" % access_token}
    options = {"ShortCode": LipanaMpesaPpassword.Business_short_code,
               "ResponseType": "Completed",
               "ConfirmationURL": "https://b73c-41-90-62-196.in.ngrok.io/c2b/confirmation",
               "ValidationURL": "https://b73c-41-90-62-196.in.ngrok.io/c2b/validation"}
    response = requests.post(api_url, json=options, headers=headers)
    return HttpResponse(response.text)



# @csrf_exempt
# def call_back(request):
#     pass



@csrf_exempt
def call_back(request):
    mpesaresponse1 = request.body.decode('utf-8')
    mpesaresponse2 = json.loads(mpesaresponse1)
    print('mpesaresponse2 :', mpesaresponse2)

    result = mpesaresponse2['Result']
    reqid = B2CModel.objects.all().filter(ConversationID =  mpesaresponse2['Result']['ConversationID']).values()

    if mpesaresponse2['Result']['ResultDesc'] == "The initiator information is invalid.":
        reqid.update(
            ResultType = mpesaresponse2['Result']['ResultType'],
            ResultCode = mpesaresponse2['Result']['ResultCode'],
            ResultDesc = mpesaresponse2['Result']['ResultDesc'],
            OriginatorConversationID2 = mpesaresponse2['Result']['OriginatorConversationID'],
            ConversationID2 = mpesaresponse2['Result']['ConversationID'],
            TransactionID =  mpesaresponse2['Result']['TransactionID'],
        )

    elif mpesaresponse2['Result']['ResultDesc'] == "The service request is processed successfully.":
        reqid.update(
            ResultType = mpesaresponse2['Result']['ResultType'],
            ResultCode = mpesaresponse2['Result']['ResultCode'],
            ResultDesc = mpesaresponse2['Result']['ResultDesc'],
            OriginatorConversationID2 = mpesaresponse2['Result']['OriginatorConversationID'],
            ConversationID2 = mpesaresponse2['Result']['ConversationID'],
            TransactionID =  mpesaresponse2['Result']['TransactionID'],
            TransactionAmount =  mpesaresponse2['Result']['ResultParameters']['ResultParameter'][0]['Value'],
            TransactionReceipt =  mpesaresponse2['Result']['ResultParameters']['ResultParameter'][1]['Value'],
            B2CRecipientIsRegisteredCustomer =  mpesaresponse2['Result']['ResultParameters']['ResultParameter'][2]['Value'],
            B2CChargesPaidAccountAvailableFunds =  mpesaresponse2['Result']['ResultParameters']['ResultParameter'][3]['Value'],
            ReceiverPartyPublicName =  mpesaresponse2['Result']['ResultParameters']['ResultParameter'][4]['Value'],
            TransactionCompletedDateTime =  mpesaresponse2['Result']['ResultParameters']['ResultParameter'][5]['Value'],
            B2CUtilityAccountAvailableFunds =  mpesaresponse2['Result']['ResultParameters']['ResultParameter'][6]['Value'],
            B2CWorkingAccountAvailableFunds =  mpesaresponse2['Result']['ResultParameters']['ResultParameter'][7]['Value'],
        )

    return HttpResponse("Payment Initiated")



@csrf_exempt
def validation(request):
    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }
    return JsonResponse(dict(context))


@csrf_exempt
def confirmation(request):
    mpesaresponse1 = request.body.decode('utf-8')
    mpesaresponse2 = json.loads(mpesaresponse1)
    print('mpesaresponse2 :', mpesaresponse2)

    trialResponse = mpesaresponse2['Body']
    stkCallback = trialResponse['stkCallback']
    stk = mpesaresponse2['Body']['stkCallback']

    # reqid2 = EventTotals2.objects.filter(checkoutRequestID =  mpesaresponse2['Body']['stkCallback']['CheckoutRequestID']).values()
   
    reqid2 = EventTotals2.objects.all().filter(checkoutRequestID =  mpesaresponse2['Body']['stkCallback']['CheckoutRequestID']).values()
    # print(reqid2)
    reqid = MpesaPaymentCalls.objects.all().filter(CheckoutRequestID =  mpesaresponse2['Body']['stkCallback']['CheckoutRequestID']).values()
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

        reqid2.update (
            receipts2 = 'hbvawub1',
            proceeding = '56',
        )
        print('failed')
    elif mpesaresponse2['Body']['stkCallback']['ResultDesc'] == "The service request is processed successfully.":

        reqid.update(
            MerchantRequestID = mpesaresponse2['Body']['stkCallback']['MerchantRequestID'],
            CheckoutRequestID = mpesaresponse2['Body']['stkCallback']['CheckoutRequestID'],
            TransactionStatus2 = mpesaresponse2['Body']['stkCallback']['ResultCode'],
            TransactionDescription2 = mpesaresponse2['Body']['stkCallback']['ResultDesc'],
            ItemAmountPaid = mpesaresponse2['Body']['stkCallback']['CallbackMetadata']['Item'][0]['Value'],
            ItemReceipt =  mpesaresponse2['Body']['stkCallback']['CallbackMetadata']['Item'][1]['Value'],
            PhoneNumber2 =  mpesaresponse2['Body']['stkCallback']['CallbackMetadata']['Item'][3]['Value'],
            CompanyAmount = (0.1 * (mpesaresponse2['Body']['stkCallback']['CallbackMetadata']['Item'][0]['Value'])),
            OrganisersAmount = (0.9 * (mpesaresponse2['Body']['stkCallback']['CallbackMetadata']['Item'][0]['Value'])),
        ) 
        # reqid2 = EventTotals2.all().filter(checkoutRequestID =  mpesaresponse2['Body']['stkCallback']['CheckoutRequestID']).values()
        # reqid2.objects.create (
        #     receipts2 = mpesaresponse2['Body']['stkCallback']['CallbackMetadata']['Item'][1]['Value'],
        #     proceeding = (0.9 * (mpesaresponse2['Body']['stkCallback']['CallbackMetadata']['Item'][0]['Value'])),
        # )
        print('success')
    else:
        reqid.update(
            MerchantRequestID = mpesaresponse2['Body']['stkCallback']['MerchantRequestID'],
            CheckoutRequestID = mpesaresponse2['Body']['stkCallback']['CheckoutRequestID'],
            TransactionStatus2 = mpesaresponse2['Body']['stkCallback']['ResultCode'],
            TransactionDescription2 = mpesaresponse2['Body']['stkCallback']['ResultDesc'],
            ItemAmountPaid = "0",
            ItemReceipt = "No receipt due to late response",
            PhoneNumber2 =  "No number due to late response",
        ) 


        print('No success')

    return HttpResponse('payment successful')

def b2c(request):
    if request.method == 'POST':

        form = B2C(request.POST)
        phone_no = request.POST['phone_no']
        amount = request.POST['amount']
        withdrawal_id = request.POST['withdrawal_id']
        if form.is_valid():
            exists = EventTotals2.objects.filter(owner = withdrawal_id).exists()
            # exists = EventTotals2.objects.filter(uuid = withdrawal_id).exists()
            for_totals = EventTotals2.objects.all().filter(owner = request.POST['withdrawal_id']).values('proceeding')
            total = for_totals.aggregate(TOTAL = Sum('proceeding'))['TOTAL']
            # return HttpResponse(total)
            print('total ',total)
            EventTotals2.objects.all().filter(owner = request.POST['withdrawal_id']).delete()


            if exists:
                access_token = MpesaAccessToken.validated_mpesa_access_token
                headers = {"Authorization": "Bearer %s" % access_token}
                api_url = 'https://sandbox.safaricom.co.ke/mpesa/b2c/v1/paymentrequest'

                payload = {
                    "InitiatorName": "testapi",
                    "SecurityCredential": "Vy14Bmfv4Mz/ANaL8tUCq3jaAifo4wQHOoADoMPj9XUPs5zgek4DVWpTGFFTgIiLiBmeRBrL60cIA5YiA9mYc98qm4cmx/XrbQxqir5H3R7MXkNlKGKOphFNy+sz6I82ZKuYFXqUJW9Visa1Eh7YNIXKo7MwbXodKztoxkXxgnXvjFfIbv22ZH18NKY1+U6pcuIqD2Zs5zNvmrA/oVsqos0P5iU+EnYZGpFOzAIIPoGuSsbqJMyp126VclgAZYxjPi8UmkZm862TkvgPy/2l/0PBfUHQ089A7u3NK8dzHsLcSFeAEA++Pe9W5atk3bYFKFKrmz/XDjoqHOGDi8h6nQ==",
                    # "SecurityCredential": "EUcQ7s8TpoMWaiQDwQQdfAnKoLyXsc0+51b9oue7RaPNKl46EI6PFxuqcJLd7dYryVL3ZPLDLqKltxo6TeIcF3aDmhXlpdjjZ6YHzeTJK1s1yyVOUhVMM+Nouus5Hc3D22k3A3PSy67R/6fmYouNigyAK4qF3VirFurrNTr6erWxPBIuR/z8YRbaA0BRRkBB/fAam3z+ia0p2sv6cugfY+ONl+zsxsIIopRb9c4DZXzyw9TC0bfN4TYPxcglQgbnoyXYn4M4vLVtmD1Q5RRGuBjH+FcVFn0ROXqAU24PbOM9MkLqgr1DkrBoCU5BwdMiGlY2jbaVBWuIwYZp6uUQgg==",
                    "CommandID": "BusinessPayment",
                    "Amount": total,
                    # "PartyA": LipanaMpesaPpassword.Business_short_code,
                    "PartyA": 600584,
                    "PartyB": 254708374149,
                    "Remarks": "Test remarks",
                    "QueueTimeOutURL": "https://be0c-197-136-64-179.eu.ngrok.io/b2c/queue",
                    # "QueueTimeOutURL": "https://c2b2-41-90-57-232.in.ngrok.io/c2b/confirmation",
                    # "ResultURL":  "https://c2b2-41-90-57-232.in.ngrok.io/c2b/confirmation",
                    "ResultURL": "https://be0c-197-136-64-179.eu.ngrok.io/b2c/result",
                    "Occassion": "Trial",
                }
                # response = requests.request("POST", 'https://sandbox.safaricom.co.ke/mpesa/b2c/v1/paymentrequest', headers = headers, json = payload)
                response = requests.post(api_url, json=payload, headers=headers)
                
                print(response.text.encode('utf8'))
                response = response.json()

                phone_no = payload['PartyB']
                amount = payload['Amount']
                withdrawal_id = request.POST['withdrawal_id']

                ConversationID = response['ConversationID']
                OriginatorConversationID = response['OriginatorConversationID']
                ResponseCode = response['ResponseCode']
                ResponseDescription = response['ResponseDescription']
                print(ResponseCode)

                B2CModel.objects.create (
                    ConversationID = ConversationID,
                    OriginatorConversationID = OriginatorConversationID,
                    ResponseCode = ResponseCode,
                    ResponseDescription = ResponseDescription,

                    phone_no = phone_no,
                    withdrawal_id = withdrawal_id,
                    amount = amount,

                )
                return HttpResponse('This is a successfull b2c payment')
    else:
        form = B2C()

    context = {'form' : form}

    return render(request, 'events/withdraw.html', context)


# def b2c(request):
#     if request.method == 'POST':

#         form = B2C(request.POST)
#         phone_no = request.POST['phone_no']
#         amount = request.POST['amount']
#         withdrawal_id = request.POST['withdrawal_id']
#         if form.is_valid():
#             exists = Post.objects.filter(uuid = withdrawal_id).exists()
#             For_Totals = EventTotals2.objects.all().filter(owner = request.POST['withdrawal_id']).values('proceeding')
#             print(For_Totals)

#             if exists:
#                 access_token = MpesaAccessToken.validated_mpesa_access_token
#                 headers = {"Authorization": "Bearer %s" % access_token}
#                 api_url = 'https://sandbox.safaricom.co.ke/mpesa/b2c/v1/paymentrequest'

#                 payload = {
#                     "InitiatorName": "testapi",
#                     "SecurityCredential": "Vy14Bmfv4Mz/ANaL8tUCq3jaAifo4wQHOoADoMPj9XUPs5zgek4DVWpTGFFTgIiLiBmeRBrL60cIA5YiA9mYc98qm4cmx/XrbQxqir5H3R7MXkNlKGKOphFNy+sz6I82ZKuYFXqUJW9Visa1Eh7YNIXKo7MwbXodKztoxkXxgnXvjFfIbv22ZH18NKY1+U6pcuIqD2Zs5zNvmrA/oVsqos0P5iU+EnYZGpFOzAIIPoGuSsbqJMyp126VclgAZYxjPi8UmkZm862TkvgPy/2l/0PBfUHQ089A7u3NK8dzHsLcSFeAEA++Pe9W5atk3bYFKFKrmz/XDjoqHOGDi8h6nQ==",
#                     # "SecurityCredential": "EUcQ7s8TpoMWaiQDwQQdfAnKoLyXsc0+51b9oue7RaPNKl46EI6PFxuqcJLd7dYryVL3ZPLDLqKltxo6TeIcF3aDmhXlpdjjZ6YHzeTJK1s1yyVOUhVMM+Nouus5Hc3D22k3A3PSy67R/6fmYouNigyAK4qF3VirFurrNTr6erWxPBIuR/z8YRbaA0BRRkBB/fAam3z+ia0p2sv6cugfY+ONl+zsxsIIopRb9c4DZXzyw9TC0bfN4TYPxcglQgbnoyXYn4M4vLVtmD1Q5RRGuBjH+FcVFn0ROXqAU24PbOM9MkLqgr1DkrBoCU5BwdMiGlY2jbaVBWuIwYZp6uUQgg==",
#                     "CommandID": "BusinessPayment",
#                     "Amount": 1000,
#                     # "PartyA": LipanaMpesaPpassword.Business_short_code,
#                     "PartyA": 600584,
#                     "PartyB": 254708374149,
#                     "Remarks": "Test remarks",
#                     "QueueTimeOutURL": "https://8105-105-163-51-4.in.ngrok.io/b2c/queue",
#                     # "QueueTimeOutURL": "https://c2b2-41-90-57-232.in.ngrok.io/c2b/confirmation",
#                     # "ResultURL":  "https://c2b2-41-90-57-232.in.ngrok.io/c2b/confirmation",
#                     "ResultURL": "https://8105-105-163-51-4.in.ngrok.io/b2c/result",
#                     "Occassion": "Trial",
#                 }
#                 # response = requests.request("POST", 'https://sandbox.safaricom.co.ke/mpesa/b2c/v1/paymentrequest', headers = headers, json = payload)
#                 response = requests.post(api_url, json=payload, headers=headers)
                
#                 print(response.text.encode('utf8'))
#                 response = response.json()

#                 phone_no = payload['PartyB']
#                 amount = payload['Amount']
#                 withdrawal_id = request.POST['withdrawal_id']

#                 ConversationID = response['ConversationID']
#                 OriginatorConversationID = response['OriginatorConversationID']
#                 ResponseCode = response['ResponseCode']
#                 ResponseDescription = response['ResponseDescription']
#                 print(ResponseCode)

#                 B2CModel.objects.create (
#                     ConversationID = ConversationID,
#                     OriginatorConversationID = OriginatorConversationID,
#                     ResponseCode = ResponseCode,
#                     ResponseDescription = ResponseDescription,

#                     phone_no = phone_no,
#                     withdrawal_id = withdrawal_id,
#                     amount = amount,

#                 )
#                 return HttpResponse('This is a successfull b2c payment')
#     else:
#         form = B2C()

#     context = {'form' : form}

#     return render(request, 'events/withdraw.html', context)



def b2c2(request):
    access_token = MpesaAccessToken.validated_mpesa_access_token
    headers = {"Authorization": "Bearer %s" % access_token}
    apiurl = 'https://sandbox.safaricom.co.ke/mpesa/b2c/v1/paymentrequest'

    payload = {
        "InitiatorName": "testapi",
        # "SecurityCredential": "Safaricom123!",
        "SecurityCredential": "Vy14Bmfv4Mz/ANaL8tUCq3jaAifo4wQHOoADoMPj9XUPs5zgek4DVWpTGFFTgIiLiBmeRBrL60cIA5YiA9mYc98qm4cmx/XrbQxqir5H3R7MXkNlKGKOphFNy+sz6I82ZKuYFXqUJW9Visa1Eh7YNIXKo7MwbXodKztoxkXxgnXvjFfIbv22ZH18NKY1+U6pcuIqD2Zs5zNvmrA/oVsqos0P5iU+EnYZGpFOzAIIPoGuSsbqJMyp126VclgAZYxjPi8UmkZm862TkvgPy/2l/0PBfUHQ089A7u3NK8dzHsLcSFeAEA++Pe9W5atk3bYFKFKrmz/XDjoqHOGDi8h6nQ==",
        "CommandID": "BusinessPayment",
        "Amount": 1000,
        "PartyA": 600584,
        # "PartyB": 254708294284,
        "PartyB": 254708374149,
        "Remarks": "Test remarks",
        # "QueueTimeOutURL": "https://c2b2-41-90-57-232.in.ngrok.io/c2b/confirmation",
        "QueueTimeOutURL": "https://8105-105-163-51-4.in.ngrok.io/b2c/queue",
        "ResultURL": "https://8105-105-163-51-4.in.ngrok.io/b2c/queue",
        "Occassion": "Trial",
    }
    response = requests.post(apiurl, headers = headers, json = payload)
    print(response.text.encode('utf8'))
    return HttpResponse('This is a successfull b2c2 payment')


def event_totals(request):
    if request.method == 'POST':
        form = EventTotals(request.POST)
        Event_title = request.POST['Event_title']
        Withdrawal_code = request.POST['Withdrawal_code']
        E_title = MpesaPaymentCalls.objects.all().filter(Event_title = Event_title).values()
        E_title_exists = MpesaPaymentCalls.objects.all().filter(Event_title = Event_title).exists()
        W_code = MpesaPaymentCalls.objects.all().filter(Withdrawal_code = Withdrawal_code).values('Amount')
        W_code_exists = MpesaPaymentCalls.objects.all().filter(Withdrawal_code = Withdrawal_code).exists()
        length = len(W_code) - 1
        if E_title_exists and W_code_exists:
            # print(W_code)
            total = W_code.aggregate(TOTAL = Sum('Amount'))['TOTAL']
            return HttpResponse(total)
            # print(sum(W_code.values_list( flat=True)))
            # for num in W_code:
            #     print(num)
            # print(W_code[:length]['id'])
    else:
        form = EventTotals()
    context = {'form' : form}

    return render(request, 'events/event_totals.html', context)
    



def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
