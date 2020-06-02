from django.contrib import admin
from .models import Customers,Products,Orders
class customeradmin(admin.ModelAdmin):
    list_display = ['cname','email','mobile','created_date']
class productadmin(admin.ModelAdmin):
    list_display = ['name','price','created_date','description','category']
class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer','status','created_date']


admin.site.register(Customers,customeradmin)
admin.site.register(Products,productadmin)
admin.site.register(Orders,OrderAdmin)
