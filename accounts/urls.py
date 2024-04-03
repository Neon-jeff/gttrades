from django.urls import path,include
from .views import *

urlpatterns = [
    path('register-success',SignUpSuccessView,name='success'),
    path('activate/',ActivateAccount,name='activate'),
    path('verify-documents/',UploadDocs,name='upload'),
    path('login/',LoginView,name='login'),
    path('sign-up/',SignUpView,name='sign-up'),
    path('dashboard/',Dashboard,name='dashboard'),
    path('assets/',Assets,name='assets'),
    path('trades/',Trades,name='trades'),
    path('markets/',Market,name='markets'),
    path('deposit/',DepositFunds,name='deposits'),
    path('withdraw/',Withdraw,name='withdraws'),
    path('copy/',CopyTrades,name='copy'),
    path('logout/',Logout,name='logout'),
    path('deposit-method/',SelectMethod,name='select'),
    path('bank-deposit',PayWithBank,name="bank"),
    path('card-deposit',PayWithCard,name="card"),
    path('history',History,name='history')

]
