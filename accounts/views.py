from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

# Create your views here.
from .models import *
from .forms import CreateUserForm
from .decorators import *
@login_required(login_url='login')
def home(request):
	orders = Order.objects.all()
	writers = Writer.objects.all()

	

	total_orders = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()

	context = {'orders':orders, 'writers':writers,
	'total_orders':total_orders,'delivered':delivered,
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
			user = form.save()
			username = form.cleaned_data.get('username')

			group = Group.objects.get(name='writer')
			user.groups.add(group)
			
			Writer.objects.create(
				user=user,
				name=user.username,
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

