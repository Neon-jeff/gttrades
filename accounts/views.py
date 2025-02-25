from django.shortcuts import render,redirect,resolve_url
from .handlers import FetchCoinData,Forex_Currencies,StockData
from django.http import JsonResponse
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.core import serializers
from .utils import *
from .locations import CountryData
import uuid
from django.conf import settings
from .wallets import wallet_address
from .otp import CreateOtp
from django.core.exceptions import ObjectDoesNotExist



# Create your views here.

def LoginView(request):
    if request.user.is_authenticated:
        if  request.user.profile.verified==True:
            return redirect('dashboard')
        if not request.user.profile.verified:
            return redirect('upload')
    if request.method=="POST":
        email=request.POST['email']
        password=request.POST['password']
        user=User.objects.filter(email=email).first()
        if user:
            auth_user=authenticate(username=user.username,password=password)
            if auth_user == None:
                messages.error(request,'Invalid Credentials, check password')
                return render(request,'pages/login.html')
            else:
                login(request, auth_user)
                if(auth_user.profile.verified==False):
                    return redirect('pending')
                return redirect('dashboard')
        else:
            messages.error(request,'No existing account')
            return render(request,'pages/login.html')
    return render(request,'pages/login.html',status=200)


def SignUpView(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method=="POST":
        data=request.POST
        email=data['email']
        if User.objects.filter(email=email).first() is not  None:
            return JsonResponse({"status":"failure"},safe=False)
        else:
            user=User.objects.create(
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'],
                username=data['email'],
            )
            user.set_password(data['password'])
            user.save()
            Profile.objects.create(
                user=user,
                country=data['country'],
                address=data['address'],
                phone_code=data['phone_code'],
                phone=f"+{data['phone_code']}{data['phone']}",
                verified=False,
                token=uuid.uuid4()

            )
            login(request,user)
            # Send welcome email to user
            SendEmail(user=user,request=request)
            messages.success(request,"Registration Successful")
            return JsonResponse({"status":"success"},safe=False)
    return render(request,'pages/register.html',{"countries":CountryData()},status=200)




def ActivateAccount(request):
    profile=Profile.objects.filter(token=request.GET['token']).first()
    if profile.verified:
        messages.success(request,'Account already verified')
        return redirect('login')
    profile.verified=True
    profile.save()
    messages.success(request,'Account successfully verified')
    return redirect('login')

@login_required(login_url='login')
def SignUpSuccessView(request):
    return render(request,'pages/register-success.html')

@login_required(login_url='login')
def UploadDocs(request):
    if not request.user.profile.verified and request.user.profile.verification_document != '':
        print(request.user.profile.verification_document)
        messages.success(request,"Verification document uploaded")
        return redirect('pending')    
    if request.user.profile.verified and request.user.profile.verification_document != '':
        messages.success(request,"Verification document uploaded")
        return redirect('dashboard')
    user=request.user
    if request.method=='POST':
        user.profile.verification_document=request.FILES['image']
        user.profile.verification_document2=request.FILES['image2']
        user.profile.document_type=request.POST['type']
        user.profile.save()
        # messages.success(request,"Account Creation Successful")
        return JsonResponse({"data":"success"},safe=False)
    return render(request,'pages/upload-documents.html')

@login_required(login_url='login')
def UploadDocsRedirect(request):
    return redirect('pending')

@login_required(login_url='login')
def Logout(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def Pending(request):
    if request.user.profile.verified:
        return redirect('dashboard')
    return render(request,'pages/verification-pending.html')

@login_required(login_url='login')
def Dashboard(request):
    if request.user.profile.verified==False:
        return redirect('upload')
    user_profile=Profile.objects.filter(user=request.user).first()
    user_json=user_profile.serialize()
    assets={
        "crypto":FetchCoinData(),
        "forex":Forex_Currencies(),
        "stocks":StockData()
        }
    # assets={
    #     "crypto":[],
    #     "forex":[],
    #     "stocks":[]
    # }
    total_deposit=sum([x.amount for x in request.user.user_deposit.filter(status='approved')])
    return render(request,'dashboard/dashboard.html',{"assets":assets,"user":user_json,"deposit":total_deposit})

@login_required(login_url='login')
def Assets(request):
    user_profile=Profile.objects.filter(user=request.user).first()
    user_json=user_profile.serialize()
    assets=FetchCoinData()
    return render(request,'dashboard/assets.html',{"assets":assets,"user":user_json})

login_required(login_url='login')
def Trades(request):
    assets=FetchCoinData()
    user_profile=Profile.objects.filter(user=request.user).first()
    user_json=user_profile.serialize()
    trades=[
        {
            "amount":trade.amount,
            "currency":trade.currency,
            "stop_loss":trade.stop_loss,
            "take_profit":trade.take_profit,
            "closed":trade.closed,
            "created":trade.created.strftime('%m/%d/%Y'),
            "id":trade.id,
            "expert":trade.expert_trade,
            "lost":trade.lost_trade
        } for trade in Trade.objects.filter(user=request.user).order_by('-id')
    ]
    if request.method=='POST':
        data=request.POST
        Trade.objects.create(
            user=request.user,
            amount=int(data['amount']),
            currency=data['currency'],
            take_profit=int(data['take_profit']),
            stop_loss=int(data['stop_loss']),
            # duration=data["duration"]
        )
        request.user.profile.dollar_balance=request.user.profile.dollar_balance-int(data["amount"])
        request.user.profile.save()
        messages.success(request,"Open trade successful")
        return JsonResponse({"status":"success"},safe=False)
    return render(request,'dashboard/trades.html',{"assets":assets,"user":user_json,"trades":trades})

def UserCoinBalance(request):
    pass

@login_required(login_url='login')
def Market(request):
    assets=FetchCoinData()
    return render(request,'dashboard/markets.html',{"assets":assets})

@login_required(login_url='login')
def CoinDetails(request):
    pass

@login_required(login_url='login')
def DepositFunds(request):
    address=[
        {
            "name":x.coin.upper(),
            "address":x.address,
            "image":x.image
        } for x in Deposit_Wallets.objects.all()
    ]
    if request.method=='POST':
        data=request.POST
        # image=request.FILES['image']
        Deposit.objects.create(
            user=request.user,
            amount=data['amount'],
            currency=data['currency'],
            # proof=image
        )
        messages.success(request,"Deposit reqeust added, check transaction historys")
        return JsonResponse({"status":"success"},safe=False,status=200)
    return render(request,'dashboard/deposit.html',{"wallets":address})

@login_required(login_url='login')
def Withdraw(request):
    if request.method=='POST':
        data=request.POST
        Withdrawal.objects.create(
            user=request.user,
            amount=data['amount'],
            currency=data['currency'],
        )
        return JsonResponse({"status":"success"},safe=False,status=200)

    return render(request,'dashboard/withdraw.html',{"wallets":wallet_address,'user':request.user.profile.serialize()})

@login_required(login_url='login')
def CopyTrades(request):
    experts_dict=[
        {
            "name":expert.name,
            "win_rate":expert.win_rate,
            "wins":expert.wins,
            "losses":expert.losses,
            "profit_share":expert.profit_share,
            "image":expert.image.url,
            "copy_amount":expert.copy_amount,
            "id":expert.id,
            "followers":expert.followers
        }
        for expert in CopyTrader.objects.all()
    ]
    if "copy" in request.GET:
        expert_id=request.GET["copy"]
        CopyExpertRequest.objects.create(
            user=request.user,
            expert=CopyTrader.objects.filter(id=expert_id).first()
        )
        return JsonResponse({"status":"success"},safe=False)
    return render(request,"dashboard/copy.html",{"user":request.user.profile.serialize(),"experts":experts_dict})


def SelectMethod(request):
    return render(request,"dashboard/select-method.html",{"user":request.user.profile.serialize()})

def PayWithBank(request):
    return render(request,"dashboard/deposit-bank.html",{"user":request.user.profile.serialize()})

def PayWithCard(request):
    return render(request,"dashboard/deposit-card.html",{"user":request.user.profile.serialize()})

def History(request):
    withdrawals=[
        {
            "amount":w.amount,
            "comfirmed":w.confirmed,
            "currency":w.currency,
            "created":w.created.strftime('%m/%d/%Y'),
            "id":w.id
        }
        for w in Withdrawal.objects.filter(user=request.user).order_by('-id')
    ]

    deposits=[
        {
            "amount":d.amount,
            "status":d.status,
            "currency":d.currency,
            "created":d.created.strftime('%m/%d/%Y'),
            "id":d.id
        }
        for d in Deposit.objects.filter(user=request.user).order_by('-id')
    ]
    history={
        "withdrawals":withdrawals,
        "deposits":deposits
    }
    return render(request,"dashboard/transaction-history.html",{"user":request.user.profile.serialize(),"history":history})


def ForgotPasswordSendOtp(request):
    if request.method == "POST":
        try:
            user = User.objects.get(email=request.POST["email"])
            user.profile.otp = CreateOtp()
            user.profile.save()
            SendResetPasswordEmail(user, user.profile.otp)
            messages.success(request, "Password reset otp sent")
            return redirect(resolve_url("verify-identity") + f"?email={user.email}")
        except ObjectDoesNotExist:
            messages.error(request, "Account with email does not exist")
            return render(request, "pages/forgot-password.html")
    return render(request, "pages/forgot-password.html")


def VerifyIdentity(request):
    email = request.GET["email"]
    user = User.objects.get(email=email)
    if request.method == "POST":
        if request.POST["otp"] == user.profile.otp:
            messages.success(request, "Identity Verified,Update Your Password")
            return redirect(resolve_url("change-password") + f"?email={user.email}")
        else:
            messages.error(request, "Invalid OTP")
            return render(request, "pages/password-otp-confirm.html")
    return render(request, "pages/password-otp-confirm.html")


def ChangePassword(request):
    user = User.objects.get(email=request.GET["email"])
    if request.method == "POST":
        data = request.POST
        if data["password"] != data["confirm"]:
            messages.error(request, "Passwords do not match")
            return render(request, "pages/reset-password.html")
        else:
            user.set_password(request.POST["password"])
            user.save()
            profile = Profile.objects.get(user=user)
            profile.password = request.POST["password"]
            profile.save()
            messages.success(request, "Password Updated")
            return redirect("login")
    return render(request, "pages/reset-password.html")
