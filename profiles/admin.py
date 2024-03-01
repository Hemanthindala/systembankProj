from django.contrib import admin
from .models import *


from django.contrib import admin
from .models import BasicDetails, PresentLocation, Status, MoneyTransfer, Transaction

# Register your models here.


admin.site.register(Request)
admin.site.register(Transaction)
admin.site.register(BasicDetails)
admin.site.register(PresentLocation)
admin.site.register(Status)
admin.site.register(MoneyTransfer)



