from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(Profile)
admin.site.register(Trade)
admin.site.register(Deposit)
admin.site.register(Withdrawal)
admin.site.register(Deposit_Wallets)
admin.site.register(CopyTrader)
admin.site.register(CopyExpertRequest)
