from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from . models import *
from django import forms

User = get_user_model()




class CreateUserForm(UserCreationForm):
	free_membership = Membership.objects.get(membership_type='Free')
	class Meta:
		model=User
		fields=['username','email','phone_number','first_name','last_name','password1','password2']
class WithdrawForm(forms.Form):
    phone_number = forms.CharField(label='Phone number')
    amount = forms.FloatField(label='Amount')
class PaymentForm(forms.Form):
    phone_number = forms.CharField(label='Phone number')
    amount = forms.FloatField(label='Amount')
    
 
		
