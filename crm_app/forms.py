from django import forms
from .models import Orders, Customers, Products
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class Orderform(forms.ModelForm):
    class Meta:
        model = Orders
        fields = ['customer', 'product', 'status']


class Customerform(forms.ModelForm):
    class Meta:
        model = Customers
        fields = ['cname', 'email', 'mobile']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['name', 'price', 'description', 'category']


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
