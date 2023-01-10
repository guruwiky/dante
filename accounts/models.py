from django.db import models
from .utils import *
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth import get_user_model
class User(AbstractUser):
	phone_number= PhoneNumberField()


# Create your models here.
STATUS = ((1, "Pending"), (0, "Complete"))

class Transaction(models.Model):
	"""This model records all the mpesa payment transactions"""
	transaction_no = models.CharField(default=uuid.uuid4, max_length=50, unique=True)
	phone_number = PhoneNumberField(null=False, blank=False)
	checkout_request_id = models.CharField(max_length=200)
	reference = models.CharField(max_length=40, blank=True)
	description = models.TextField(null=True, blank=True)
	amount = models.CharField(max_length=10)
	status = models.CharField(max_length=15, choices=STATUS, default=1)
	receipt_no = models.CharField(max_length=200, blank=True, null=True)
	created = models.DateTimeField(auto_now_add=True)
	ip = models.CharField(max_length=200, blank=True, null=True)

	def __str__(self):
		return f"{self.transaction_no}"
STATUS=(
			('Inactive','Inactive'),
			('Active','Active'),
		)
class Writer(models.Model):
	user = models.OneToOneField(User, null=True, blank=True,on_delete=models.CASCADE)
	name=models.CharField(max_length=200, null=True)
	code=models.CharField(max_length=12, blank=True)
	phone_number=models.CharField(max_length=200, null=True, blank=True)
	email=models.CharField(max_length=200, null=True)
	status = models.CharField(choices=STATUS, max_length=15, default='Inactive', null=True, blank=True)
	recommended_by=models.ForeignKey(User, null=True, blank=True,on_delete=models.CASCADE, related_name='ref_by')
	balance= models.FloatField(null=True, blank=True ,default=0.00)
	def __str__(self):
		if self.user:
			return self.user.username

	def deposit(self, amount):
		self.balance += amount
		self.save()
	def payment(self, amount):
		self.balance += amount
		self.save()


	def withdraw(self, amount):
		if amount > self.balance:
			raise ValueError("Insufficient funds")
		self.balance -= amount
		self.save()
	
	def __str__(self):
		if self.user:
			return f"{self.user.username}-{self.code}"
	
	def get_recommened_profiles(self):
	   pass
	def save(self, *args, **kwargs):
		if self.code == "":
			code = generate_ref_code()
			self.code = code
		super().save(*args, **kwargs)
	
	
class Account(models.Model):
	balance = models.DecimalField(max_digits=10, decimal_places=2 ,null=True, default=0)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	


	def __str__(self):
		return self.user.username

	def deposit(self, amount):
		self.balance += amount
		self.save()
	def payment(self, amount):
		self.balance += amount
		self.save()


	def withdraw(self, amount):
		if amount > self.balance:
			raise ValueError("Insufficient funds")
		self.balance -= amount
		self.save()
	



class Gig(models.Model):


	STATUS=(
			('Available','Available'),
			('Assigned','Assigned'),
		)

	title=models.CharField(max_length=200, null=True)
	subject=models.CharField(max_length=200, null=True)
	price=models.FloatField(null=True)
	description=models.TextField(null=True)
	deadline=models.DateTimeField( null=True)
	status=models.CharField(max_length=200, null=True,choices=STATUS)

	def __str__(self):
		return self.title
MEMBERSHIP_CHOICES = (
('Premium', 'premium'),
('Free', 'free'),
)
class Membership(models.Model):
	slug = models.SlugField(null=True, blank=True)
	membership_type = models.CharField(
	choices=MEMBERSHIP_CHOICES, default='Free',
	max_length=30
	  )
	price = models.FloatField(null=True)
	def __str__(self):
	   return self.membership_type
class UserMembership(models.Model):
	user = models.OneToOneField(User, null=True, blank=True ,   related_name='user_membership', on_delete=models.CASCADE)
	membership = models.ForeignKey(Membership, related_name='user_membership', on_delete=models.SET_NULL, null=True)
	def __str__(self):
	   return self.user.username
class Subscription(models.Model):
	user_membership = models.ForeignKey(UserMembership, related_name='subscription', on_delete=models.CASCADE)
	active = models.BooleanField(default=True)
	def __str__(self):
	  return self.user_membership.user.username
class Order(models.Model):
	STATUS=(
			('Pending','Pending'),
			('Rejected','Rejected'),
			('Paid','Paid'),
		)


	writer=models.ForeignKey(Writer,null=True, on_delete=models.SET_NULL)
	orderid=models.CharField(max_length=200, null=True)
	gig=models.ForeignKey(Gig,null=True, on_delete=models.SET_NULL)
	price=models.FloatField(null=True)
	status=models.CharField(max_length=200, null=True,choices=STATUS)
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# M-pesa Payment models

class MpesaCalls(BaseModel):
    ip_address = models.TextField()
    caller = models.TextField()
    conversation_id = models.TextField()
    content = models.TextField()

    class Meta:
        verbose_name = 'Mpesa Call'
        verbose_name_plural = 'Mpesa Calls'


class MpesaCallBacks(BaseModel):
    ip_address = models.TextField()
    caller = models.TextField()
    conversation_id = models.TextField()
    content = models.TextField()

    class Meta:
        verbose_name = 'Mpesa Call Back'
        verbose_name_plural = 'Mpesa Call Backs'


class MpesaPayment(BaseModel):
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