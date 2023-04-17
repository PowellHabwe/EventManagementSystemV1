from django import forms
from django.forms import ModelForm

from .models import B2CModel, Promise,Ticket_info,Post,MpesaConfirmation, TicketOrder, MpesaPaymentCalls, StkInfo,EventTotals


class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'


class PostForm(ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'content','price', 'header_image']

        # widgets = {
        #     'content': forms.TextInput(attrs={'placeholder': 'Type your phone number in this format: 254712345678'})
            
        # }


class PromiseForm(ModelForm):

    class Meta:
        model = Ticket_info
        fields = ['event_organiser', 'ticket_title', 'ticket_price','city' ,'venue' , 'date', 'time', ]

        widgets = {
            'date': DateInput(),
            'time': TimeInput(),
        }


# class ConfirmForm(ModelForm):

#     class Meta:
#         model = MpesaConfirmation
#         fields = ['receipt_no' ]
class ConfirmForm(ModelForm):

    class Meta:
        model = MpesaPaymentCalls
        fields = ['mpesa_receipt','ticket_no' ]

class StkCall(ModelForm):

    class Meta:
        model = MpesaPaymentCalls
        fields = ['ticket_title','phone_number' ]

        widgets = {
            'phone_number': forms.TextInput(attrs={'placeholder': 'Type your phone number in this format: 254712345678'})
            
        }

 
class TicketOrder(ModelForm):

    class Meta:
        model = TicketOrder
        fields = ['mpesareceipt']

class StkInfo(ModelForm):
    class Meta:
        model = StkInfo
        fields = ['ticket_title']

class B2C(ModelForm):

    class Meta:
        model = B2CModel
        fields = ['phone_no', 'amount', 'withdrawal_id']

        widgets = {
            'phone_no': forms.TextInput(attrs={'placeholder': 'Type your phone number in this format: 254712345678'})
            
        }

class EventTotals(ModelForm):

    class Meta:
        model = EventTotals
        fields = ['Event_title','Withdrawal_code']

