from django.contrib import admin
from .models import Post
# Register your models here.
from .models import Product
from .models import Ticket_info
from .models import Promise
from .models import MpesaPayment
from .models import MpesaPaymentCalls
from .models import MpesaConfirmation
from .models import ExistingReceipt
from .models import EventTotals
from .models import B2CModel
from .models import EventTotals2

admin.site.register(Product)
admin.site.register(Post)   
admin.site.register(Ticket_info)   
admin.site.register(MpesaPayment)   
admin.site.register(Promise)   
admin.site.register(MpesaPaymentCalls)   
admin.site.register(MpesaConfirmation)   
admin.site.register(ExistingReceipt)   
admin.site.register(EventTotals)   
admin.site.register(B2CModel)   
admin.site.register(EventTotals2)   
