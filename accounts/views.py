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


import requests

# Create your views here.
from .models import *
from .forms import *
from .decorators import *

@login_required(login_url='login')
def home(request, *args, **kwargs):
    try:
        #balance = Account.balance
        # = Balance.objects.get(id=id)
        #user=User.objects.get(pk=pk)
        #writers = Writer.objects.filter(id=writer.id)
        pk = request.user.id
       
        
        #balance=writer.balance
        
        balance_r = Account.objects.get(pk=pk)
    except Account.DoesNotExist:
            balance_r = Account.objects.create(
              user=request.user
            )
            balance_r.save()

   
    orders = Order.objects.all()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'orders':orders, 
    'total_orders':total_orders,'delivered':delivered, 'balance_r':balance_r,  
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
                return redirect('home user.id')
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
def stk_push_callback(request):
        data = request.body
        
        return HttpResponse("STK Push in Django👋")
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
        form = WithdrawForm(request.POST)
        if form.is_valid():
            cl = MpesaClient()
            account_reference = 'reference'
            transaction_desc = 'Description'
            amount = 350
            phone_number = request.POST['phone_number']
            api_URL = 'https://api.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
            consumer_key = 'vHz4VLhPsGNDI4LaCopTn7fli4rSZ0aM'
            consumer_secret = 'XPB0nMwxYmg5DH5Q'
            callback_url = 'https://darajambili.herokuapp.com/express-payment';
            response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)

            # Set up the Mpesa API endpoint and headers
            #api_endpoint = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
            headers = {
                "Authorization": "Bearer YOUR_ACCESS_TOKEN",
                "Content-Type": "application/json"
            }

            # Set up the payload for the Mpesa API request
            payload = {
                "BusinessShortCode": '174379',
                "Password": "YOUR_ENCRYPTED_PASSWORD",
                "Timestamp": "YYYYMMDDHHMMSS",
                "TransactionType": "CustomerPayBillOnline",
                "Amount": amount,
                "PartyA": phone_number,
                "PartyB": '174379',
                "PhoneNumber": phone_number,
                "CallBackURL": "YOUR_CALLBACK_URL",
                "AccountReference": "Payment for product XYZ",
                "TransactionDesc": "Payment for product XYZ"
            }

        # Make the API request to initiate the payment
        response = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))

        # Check the response status code
        if response.status_code == 0:
            # Payment request was successful, parse the response to get the checkout request ID
            response_json = response.json()
            checkout_request_id = '<Checkout request ID>'

            # Store the transaction details in the database
            Transaction.objects.create(
                phone_number=phone_number,
                amount=amount,
                checkout_request_id=checkout_request_id
            )
            try:
                    
                    pk = request.user.id
                    balance_r = Account.objects.get(pk=pk)
            except Account.DoesNotExist:
                        balance_r = Account.objects.create(
                          user=request.user
                        )
                        balance_r.save()
                        
                        balance_r.balance += amount
                        account.save()

            # Redirect the user to the Mpesa Daraja API payment page
            return HttpResponse("success")
        else:
            # Payment request failed, return an error message
            return HttpResponse("Error making payment. Please try again.")

    # Render the payment form template
    form = WithdrawForm()
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

