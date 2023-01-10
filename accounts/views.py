from django.shortcuts import render,redirect
from django.http import HttpResponse
from django_daraja.mpesa.core import MpesaClient
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.views.generic import ListView
from requests.auth import HTTPBasicAuth
from django.http import HttpResponse, JsonResponse
import requests
import json

from django.views.decorators.csrf import csrf_exempt


import requests

# Create your views here.
from .models import *
from .forms import *
from .decorators import *

@login_required(login_url='login')
def home(request, *args, **kwargs):
    #writer=Writer.objects.get(id=pk)
    user = (kwargs.get('ref_code'))
    writer = Writer.objects.get(user=user)
    request.session['ref_writer'] = writer.id
    orders = writer.order_set.all()
    status=writer.status
    balance=writer.balance
    order_count=orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'orders':orders, 'order_count':order_count, 'writer':writer, 'balance': balance,
    'delivered':delivered, 
    'pending':pending }


    return render(request, 'accounts/dashboard.html', context)
@login_required(login_url='login')
def referrals(request, *args, **kwargs):
    code = str(kwargs.get('ref_code'))
    try:
        writer = Writer.objects.get(code=code)
        request.session['ref_writer'] = writer.id
        print('id', writer.id)
    except:
        pass
    print(request.session.get_expiry_age())
    return render(request, 'accounts/referrals.html', {})
@unauthenticated_user
def loginPage(request):
    
    if request.method == 'POST':
            username = request.POST.get('username')
            password =request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username OR password is incorrect')


    context = {}
    return render(request, 'accounts/login.html', context)
def logoutUser(request):
    logout(request)
    return redirect('login')
def landing(request):
    return render(request,'accounts/landing.html')
@unauthenticated_user
def signup(request):
    
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user=form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            phone_number = form.cleaned_data.get('phone_number')
            get_membership= Membership.objects.get(membership_type='Free')
            instance = UserMembership.objects.create(user=user, membership=get_membership)
            user_subscription = Subscription()
            user_subscription.user_membership = user_membership
            instance = balance(user = request.user, balance = 0)
            instance.save()
            
            return user
            

            group = Group.objects.get(name='writer')
            user.groups.add(group)
            
            Writer.objects.create(
                user=user,
                name=user.username,
                phone_number=user.phone_number,
                email=email,
                balance=balance
                )

            messages.success(request, 'Account was created for ' + username)

            return redirect('login')
        

    context = {'form':form}
    return render(request, 'accounts/signup.html', context)

def forget(request):
    return render(request,'accounts/forget.html')
@login_required(login_url='login')
def gigs(request):
    gigs= Gig.objects.all()
    context={'gigs':gigs}
    return render(request,'accounts/gigs.html',context)
@login_required(login_url='login')
def writers(request,pk):
    writer=Writer.objects.get(id=pk)
    orders=writer.order_set.all()
    order_count=orders.count()
    paid = orders.filter(status='Paid').count()
    context={'writer':writer,'orders':orders,'order_count':order_count,'paid':paid}
    return render(request,'accounts/writers.html',context)
def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'accounts/simple_upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'accounts/simple_upload.html')

class MembershipView(ListView):
    model = Membership
    template_name = 'accounts/plans.html'
    def get_user_membership(self):
        user_membership_qs = UserMembership.objects.filter(user=self.request.user)
        if user_membership_qs.exists():
            return user_membership_qs.first()
        return None
    #def get_context_data(self, *args, **kwargs):
       # context = super().get_context_data(**kwargs)
       # current_membership = self.get_user_membership(self.request)
        #context['current_membership'] = str(current_membership.membership)
        return context
def pay(request):
    if request.method == 'POST':
        # Get the payment details from the form
        form = PaymentForm(request.POST)
        if form.is_valid():
            cl = MpesaClient()
            account_reference = 'reference'
            transaction_desc = 'Description'
            amount = 450
            phone_number = request.POST['phone_number']
            api_URL = 'https://api.safaricom.co.ke/mpesa/stkpush/v1/processrequest' 
            consumer_key = 'AE9TW0DNG7LMmoE1Ddv88gIeUAAgdVwE'
            consumer_secret = 'TEYy9G8ky2Ahkwmg'
            callback_url = 'https://api.safaricom.co.ke/mpesa/stkpush/v1/processrequest';
            response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)

            
            return HttpResponse(response.response_description)

            # Render the payment form template
    form = PaymentForm()
    return render(request, 'accounts/pay.html',{'form': form})
def withdraw(request):
    if request.method == 'POST':
        form = WithdrawForm(request.POST)
        if form.is_valid():
            # Initiate withdrawal using Mpesa Daraja API
            phone_number = str(request.user.phone_number)
            amount = form.cleaned_data['amount']
            #phone_number = request.user.phone_number
            api_url = 'https://api.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
            api_key = 'vHz4VLhPsGNDI4LaCopTn7fli4rSZ0aM'
            api_secret = 'XPB0nMwxYmg5DH5Q'
            headers = {
                'Authorization': 'Bearer {}'.format(api_key),
                'Content-Type': 'application/json'
            }
            data = {
                'BusinessShortCode': '174379',
                'Password': api_secret,
                'Timestamp': 'XPB0nMwxYmg5DH5Q',
                'TransactionType': 'CustomerPayBillOnline',
                'Amount': amount,
                'PartyA': phone_number,
                'PartyB': '174379',
                'PhoneNumber': phone_number,
                'CallBackURL': 'https://your-callback-url.com/withdraw/',
                'AccountReference': 'Withdrawal',
                'TransactionDesc': 'Withdrawal from account'
            }
            response = requests.post(api_url, json=data, headers=headers)
            if response.status_code < 200:
                # Update customer's balance and save changes to database
                try:
                    
                    pk = request.user.id
                    balance_r = Account.objects.get(pk=pk)
                except Account.DoesNotExist:
                        balance_r = Account.objects.create(
                          user=request.user
                        )
                        balance_r.save()
                        
                        balance_r.balance -= amount
                        account.save()
                        return render(request, 'withdraw_success.html', {'amount': amount})
            else:
                        return HttpResponse("Couldn't withdraw funds. Please try again.")
    else:
        form = WithdrawForm()
        form = WithdrawForm()
    return render(request, 'accounts/withdraw.html', {'form': form})
def getAccessToken(request):
    consumer_key = 'vHz4VLhPsGNDI4LaCopTn7fli4rSZ0aM'
    consumer_secret = 'XPB0nMwxYmg5DH5Q'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']

    return HttpResponse(validated_mpesa_access_token)


#def lipa_na_mpesa_online(request):
   # access_token = MpesaAccessToken.validated_mpesa_access_token
    #api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    #headers = {"Authorization": "Bearer %s" % access_token}
    #request = {
        #"BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
        #"Password": LipanaMpesaPpassword.decode_password,
        #"Timestamp": LipanaMpesaPpassword.lipa_time,
        #"TransactionType": "CustomerPayBillOnline",
        #"Amount": 1,
        #"PartyA": 254758578816,  # replace with your phone number to get stk push
        #"PartyB": LipanaMpesaPpassword.Business_short_code,
        #"PhoneNumber": 254758578816,  # replace with your phone number to get stk push
        #"CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
        #"AccountReference": "Daniel Mawioo",
        #"TransactionDesc": "Testing stk push"
    #}

    #response = requests.post(api_url, json=request, headers=headers)
    #return HttpResponse('success')


@csrf_exempt
def register_urls(request):
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    headers = {"Authorization": "Bearer %s" % access_token}
    options = {"ShortCode": LipanaMpesaPpassword.Test_c2b_shortcode,
               "ResponseType": "Completed",
               "ConfirmationURL": "https://8472-197-232-61-238.ngrok.io/api/v1/c2b/confirmation",
               "ValidationURL": "https://8472-197-232-61-238.ngrok.io/api/v1/c2b/validation"}
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
def stk_push_callback(request):
    data =request.body.decode('utf-8')
    #mpesa_payment = json.loads(data)

    #payment = MpesaPayment(
        #first_name=mpesa_payment['FirstName'],
        #last_name=mpesa_payment['LastName'],
        #middle_name=mpesa_payment['MiddleName'],
        #description=mpesa_payment['TransID'],
        #phone_number=mpesa_payment['MSISDN'],
        #amount=mpesa_payment['TransAmount'],
        #reference=mpesa_payment['BillRefNumber'],
        #organization_balance=mpesa_payment['OrgAccountBalance'],
        #type=mpesa_payment['TransactionType'],

    #)
    #payment.save()

    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }
#
    return JsonResponse(dict(context))

