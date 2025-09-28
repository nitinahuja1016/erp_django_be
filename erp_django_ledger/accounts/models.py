from django.db import models

# Create your models here.

class VendorManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(account_type = 'vendor')

class CustomerManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(account_type = 'customer')


class Account(models.Model):
    ACCOUNT_TYPES = [
        ('customer' , 'Customer'),
        ('vendor', 'Vendor'),
        ('employee', 'Employee'),
        ('bank', 'Bank'),

    ]
    name = models.CharField(max_length=100)
    account_type = models.CharField(max_length=20,choices=ACCOUNT_TYPES)
    opening_balance = models.DecimalField(max_digits=12,decimal_places=2,default=0)
    balance= models.DecimalField(max_digits=12, decimal_places=2)
    contact_info = models.JSONField(null=True, blank=True,default=dict)

    objects = models.Manager()
    #custom manager
    vendor = VendorManager() #Account.vendor.all() will give all the vendors
    customer = CustomerManager()

    #default manager to be still available

    def __str__(self):
        return f"{self.account_type}: {self.name} : {self.balance}"


class Product(models.Model):
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=20,null=True,blank=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(max_length=20,null=True,blank=True)
    opening_stock = models.PositiveIntegerField(default=0)
    current_stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}: {self.current_stock} {self.sku}"


class StockMovement(models.Model):
    TRANSACTION_STATUS = [
        ('in','Inward'),
        ('out','Outward')
    ]

    # product= models.ForeignKey(Product,on_delete=models.CASCADE)
    # quantity= models.IntegerField()
    transaction_type= models.CharField(max_length=10,choices=TRANSACTION_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.transaction_type} on {self.created_at}"




class Transaction(models.Model):
    TRANSACTION_TYPE = [
        ('dr','Debit'),
        ('cr','Credit')
    ]
    account = models.ForeignKey(Account,on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12,decimal_places=2)
    transaction_type = models.CharField(max_length=20,choices=TRANSACTION_TYPE)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    stock_movement = models.ForeignKey(StockMovement,on_delete=models.SET_NULL,null=True, blank=True, related_name='transactions_stock_movement')

    def __str__(self):
        return f"{self.transaction_type} - {self.amount} on {self.created_at}"

class StockMovementLineItem(models.Model):
    stock_movement = models.ForeignKey(StockMovement,on_delete=models.CASCADE,related_name='stock_line_items')
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity= models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"
    
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self._old_quanity = getattr(self, 'quantity',None)
    #     self._product_id = getattr(self,'product_id',None)
    #     # self._old_quanity = self.quantity
    #     # self._product_id = self._product_id
   

class TransactionLineItem(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=12,decimal_places=2)

    