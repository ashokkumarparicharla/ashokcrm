from django.db import models
from django.contrib.auth.models import User
class Customers(models.Model):
    user = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    cname=models.CharField(max_length=50,null=True)
    email=models.EmailField(max_length=50,null=True)
    mobile=models.BigIntegerField(null=True)
    created_date=models.DateField(auto_now_add=True,null=True)
    def __str__(self):
        return self.cname
class Products(models.Model):
    CATEGORY=(
        ('Indoor','Indoor'),('Outdoor','Outdoor'),('Anywhere','Anywhere')
    )
    name=models.CharField(max_length=50,null=True)
    price=models.IntegerField(null=True)
    created_date=models.DateField(auto_now_add=True,null=True)
    description=models.CharField(max_length=100,blank=True)
    category=models.CharField(max_length=100,choices=CATEGORY,null=True)

    def __str__(self):
        return self.name

class Orders(models.Model):
    STATUS=(('Delivered','Delivered'),('Pending','Pending'),('OutforDelivery','OutforDelivery'))

    customer=models.ForeignKey(Customers,on_delete=models.CASCADE)
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    status=models.CharField(max_length=50,choices=STATUS)
    created_date=models.DateField(auto_now_add=True,null=True)

