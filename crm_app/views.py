from django.shortcuts import render, redirect
from .models import Customers, Products, Orders
from .forms import Orderform, Customerform, ProductForm, CreateUserForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users, admin_only


@unauthenticated_user
def registerpage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = request.POST.get('username')
            messages.success(request, 'account created sucessfully for ' + user)
            return redirect(loginpage)
    context = {'form': form}
    return render(request, 'crmaccounts/registration.html', context)


@unauthenticated_user
def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.warning(request, 'username or password is wrong')
    return render(request, 'crmaccounts/loginpage.html')


def logoutpage(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userpage(request):
    customers = Customers.objects.get(user=request.user)
    orders = request.user.customers.orders_set.all()
    total_orders = len(orders)
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    outfordelivery = orders.filter(status='OutforDelivery').count()

    context = {'customers': customers, 'orders': orders,
               'total_orders': total_orders, 'pending': pending, 'delivered': delivered,
               'outfordelivery': outfordelivery}

    return render(request, 'crmaccounts/user.html', context)


@login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
@admin_only
def home(request):
    customers = Customers.objects.all()
    products = Products.objects.all()
    orders = Orders.objects.all()
    total_orders = len(orders)
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    outfordelivery = orders.filter(status='OutforDelivery').count()

    context = {'customers': customers, 'products': products, 'orders': orders,
               'total_orders': total_orders, 'pending': pending, 'delivered': delivered,
               'outfordelivery': outfordelivery}
    return render(request, 'crmaccounts/dashbord.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Products.objects.all()
    context = {'products': products}
    return render(request, 'crmaccounts/products.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customers(request, str_pk):
    customers = Customers.objects.get(id=str_pk)
    orders = customers.orders_set.all()
    total_orders = orders.count()
    context = {'customers': customers, 'orders': orders, 'total_orders': total_orders}
    return render(request, 'crmaccounts/customers.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def create_order(request):
    form = Orderform()
    if request.method == 'POST':
        form = Orderform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'crmaccounts/create_order.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def create_order_by_customer(request):
    form = Orderform()
    if request.method == 'POST':
        form = Orderform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_page')
    context = {'form': form}
    return render(request, 'crmaccounts/create_order.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def update_order(request, pk):
    order = Orders.objects.get(id=pk)
    form = Orderform(instance=order)
    if request.method == 'POST':
        form = Orderform(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'crmaccounts/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_order(request, pk):
    order = Orders.objects.get(id=pk)
    order.delete()
    return redirect('/')


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def update_customer(request, pk):
    customer = Customers.objects.get(id=pk)
    form = Customerform(instance=customer)
    if request.method == 'POST':
        form = Customerform(request.POST, instance=customer)

        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'crmaccounts/update_customer.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_customer(request, pk):
    form = Customers.objects.get(id=pk)
    form.delete()
    return redirect('/')


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def update_product(request, pk):
    product = Products.objects.get(id=pk)
    form = ProductForm(instance=product)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'crmaccounts/product_edit.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_product(request, pk):
    form = Products.objects.get(id=pk)
    form.delete()
    return redirect('/')
