from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Writer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True,on_delete=models.CASCADE)
    name=models.CharField(max_length=200, null=True)
    phone=models.CharField(max_length=200, null=True)
    email=models.CharField(max_length=200, null=True)
    active = models.BooleanField(default=False, null=True, blank=True)
    #balance

    def __str__(self):
        return self.name
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

class Order(models.Model):
    STATUS=(
            ('Pending','Pending'),
            ('Rejected','Rejected'),
            ('Paid','Paid'),
        )
    writer=models.ForeignKey(Writer,null=True, on_delete=models.SET_NULL)
    gig=models.ForeignKey(Gig,null=True, on_delete=models.SET_NULL)
    price=models.FloatField(null=True)
    status=models.CharField(max_length=200, null=True,choices=STATUS)
