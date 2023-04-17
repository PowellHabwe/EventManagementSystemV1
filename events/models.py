import uuid
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib import messages
from django.shortcuts import HttpResponse
from django.core.validators import MinLengthValidator


import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image,ImageDraw

# from 
# Create your models here.

class IpModel(models.Model):
    ip = models.CharField( max_length=100)

    def __str__(self):
        return self.ip

        
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(validators=[MinLengthValidator(50)])
    price = models.PositiveIntegerField(default=0)
    header_image = models.ImageField(null=True, blank=True, upload_to='images')
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    # uuid= models.CharField(default=uuid.uuid4,max_length=50)
    uuid= models.CharField(default=uuid.uuid4,max_length=50)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})#'uuid':self.uuid
   
    # def get_absolute_url(self):
    #     return reverse('post_detail2', kwargs={'pk': self.pk, 'uuid':self.uuid})    

    # def get_absolute_url(self):
    #     return reverse('pay_confirm', kwargs={'pk': self.pk, 'uuid':self.uuid})    

    def get_display_price(self):
        return "{0:.2f}".format(self.price / 100)   

    
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)  # cents

    def __str__(self):
        return self.name
    
    def get_display_price(self):
        return "{0:.2f}".format(self.price / 100)        


class Ticket_info(models.Model):
    event_organiser = models.CharField(max_length=100)
    ticket_title = models.CharField(max_length=100)
    ticket_price = models.PositiveIntegerField(default=0)# cents
    city = models.CharField(max_length=100)
    venue =  models.CharField(max_length=100)
    date = models.DateField(null=True)
    time = models.TimeField(null=True)
    event_start_time =  models.CharField(max_length=100)
    event_end_time =  models.CharField(max_length=100)
    first_act_time =  models.CharField(max_length=100)
    uuid = models.CharField(default=uuid.uuid4,max_length=50)
    qr_code = models.ImageField( upload_to='qr_codes', blank=True)

    def __str__(self):
        return self.ticket_title

    def get_absolute_url(self):
        return reverse('ticket_detail', kwargs={'pk': self.pk}) 

    def save(self, *args, **kwargs):
        qrcode_img = qrcode.make(self.event_organiser)
        canvas = Image.new('RGB', (200,200), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname =f'qr_code-{self.event_organiser}.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.qr_code.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)   


class Promise(models.Model):
    ticket_title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    made_on = models.DateField()


    def __str__(self):
        return self.ticket_title

    def get_absolute_url(self):
        return reverse('ticket_detail1', kwargs={'pk': self.pk}) 

# MPESA API MODELS

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# M-pesa Payment models

class MpesaPaymentCalls(models.Model):
    Event_title = models.TextField()
    Event_price = models.TextField()
    Withdrawal_code = models.TextField()

    Title = Post.title
    BusinessShortCode = models.TextField()
    Timestamp = models.TextField()
    TransactionType = models.TextField()
    Amount = models.TextField()
    PartyA = models.TextField()
    PartyB = models.TextField()
    PhoneNumber = models.TextField()
    PhoneNumber2 = models.TextField()
    AccountReference = models.TextField()

    MerchantRequestID = models.TextField()
    CheckoutRequestID = models.TextField()
    TransactionStatus1 = models.IntegerField() #TRANSACTION STATUS1
    TransactionDescription1 = models.TextField() #TRANSACTION Description1
    CustomerMessage = models.TextField()

    TransactionStatus2 = models.TextField() #TRANSACTION STATUS2
    TransactionDescription2 = models.TextField() #TRANSACTION Description2
    ItemAmountPaid = models.TextField()
    ItemReceipt = models.TextField()
    PhoneNumber2 = models.TextField()
    ItemDate = models.TextField()

    CompanyAmount = models.TextField()
    OrganisersAmount = models.TextField()

    mpesa_receipt = models.CharField(max_length = 10000000)
    ticket_no = models.IntegerField(null=True)

    ticket_title = models.CharField(max_length = 10000000)
    phone_number = models.CharField(max_length = 10000000)

    # Eventowner = models.ForeignKey(Reporter, on_delete=models.CASCADE)


    def __str__(self):
        return self.ItemReceipt


class MpesaPayment(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    type = models.TextField()
    reference = models.TextField()
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.TextField()
    organization_balance = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Mpesa Payment'
        verbose_name_plural = 'Mpesa Payments'

    def __str__(self):
        return self.first_name

class MpesaConfirmation(models.Model):
    receipt_no = models.CharField(max_length=50)

    # def get_absolute_url(self):
    #     return reverse('post_detail', kwargs={'pk': self.pk, 'uuid':self.uuid}) 

class CompanyCut(models.Model):
    amount = models.IntegerField()

    def __str__(self):
        return self.amount


class OrganiserCut(models.Model):
    amount = models.IntegerField()

    def __str__(self):
        return self.amount


class TicketOrder(models.Model):
    # mpesareceipt = models.IntegerField()
    mpesareceipt = models.TextField()

    def __str__(self):
        return self.mpesareceipt

class StkInfo(models.Model):
    ticket_title = models.TextField()

    def __str__(self):
        return self.ticket_title

class B2CModel(models.Model):
    phone_no = models.CharField(max_length = 10000000)
    amount = models.CharField(max_length = 10000000)
    withdrawal_id = models.CharField(max_length = 10000000)
    ConversationID = models.TextField()
    OriginatorConversationID = models.TextField()
    ResponseCode = models.TextField()
    ResponseDescription = models.TextField()
    ResultType = models.TextField()
    ResultCode = models.TextField()
    ResultDesc = models.TextField()
    OriginatorConversationID2 = models.TextField()
    ConversationID2 = models.TextField()
    ConversationID = models.TextField()
    TransactionAmount = models.TextField()
    TransactionReceipt = models.TextField()
    TransactionID = models.TextField()
    B2CRecipientIsRegisteredCustomer = models.TextField()
    B2CChargesPaidAccountAvailableFunds = models.TextField()
    ReceiverPartyPublicName = models.TextField()
    B2CUtilityAccountAvailableFunds = models.TextField()
    B2CWorkingAccountAvailableFunds = models.TextField()
    TransactionCompletedDateTime = models.TextField()


    def __str__(self):
        return self.ResponseDescription

class ExistingReceipt(models.Model):
    receipt = models.TextField()

    def __str__(self):
        return self.receipt

class EventTotals(models.Model):
    Event_title =  models.CharField(max_length = 10000000)
    Withdrawal_code =  models.CharField(max_length = 10000000)
    
    def __str__(self):
        return self.Event_title

class EventTotals2(models.Model):
    receipts2 = models.TextField()
    proceeding = models.TextField()
    owner = models.TextField()
    checkoutRequestID = models.TextField()
