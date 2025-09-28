from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Product)
admin.site.register(Account)
# admin.site.register(StockMovement)
# admin.site.register(StockMovementLineItem)
# admin.site.register(Transaction)
# admin.site.register(TransactionLineItem)

class VendorAdmin(admin.ModelAdmin):
    list_display = ['id','balance','name']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(account_type='vendor')
# admin.site.register(Account, VendorAdmin)
    

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id','balance','name']
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(account_type='customer')
# admin.site.register(Account, CustomerAdmin)

class Vendor(Account):
    objects = VendorManager()
    list_display = ['id','balance','name']

    class Meta:
        proxy = True
        verbose_name = 'Vendor'
        verbose_name_plural = 'Vendors'
    
class Customer(Account):
    objects = CustomerManager()
    list_display = ['id','balance','name']
    class Meta:
        proxy = True
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'

admin.site.register(Vendor, VendorAdmin)
admin.site.register(Customer, CustomerAdmin)

class StockMovementLineItemInline(admin.TabularInline):
    model = StockMovementLineItem
    #This gives number of blank forms
    extra = 1

class StockMovementAdmin(admin.ModelAdmin):
    list_display = ['id','transaction_type','created_at']
    inlines = [StockMovementLineItemInline]

admin.site.register(StockMovement,StockMovementAdmin)


class TranscactionLineItemInlie(admin.TabularInline):
    model = TransactionLineItem
    extra = 1

class TransactionAdmin(admin.ModelAdmin):
    list_display = ['id','account','amount','transaction_type','created_at']
    inlines = [TranscactionLineItemInlie]

admin.site.register(Transaction, TransactionAdmin)
