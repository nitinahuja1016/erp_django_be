from django.db.models.signals import pre_save,post_save, post_delete
from django.dispatch import receiver
from .models import *


@receiver(pre_save, sender = StockMovementLineItem)
def cache_old_stock_line_item(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_isntance = StockMovementLineItem.objects.get(pk = instance.pk)
            instance._old_quantity = old_isntance.quantity
            instance._old_product_id = old_isntance.product_id
        except StockMovementLineItem.DoesNotExist:
            instance._old_quantity = None
            instance._old_product_id = None
    else:
        instance._old_quantity = None
        instance._old_product_id = None


@receiver(post_save, sender = StockMovementLineItem)
def update_product_stock_on_save(sender, instance, created, **kwargs):
    new_product = instance.product
    new_qty = instance.quantity 
    movement_type = instance.stock_movement.transaction_type  #will be in or out
    if created:
        if movement_type == "in":
            new_product.current_stock += new_qty
        else:
            new_product.current_stock -= new_qty
        new_product.save()
    else:
        old_qty = getattr(instance, '_old_quantity',None)
        old_product_id = getattr(instance, '_old_product_id',None)

        if old_qty is None or old_product_id is None:
            return
        # try:
        #     old_instance = StockMovementLineItem.objects.get(pk=instance.pk)
        #     old_qty = old_instance.quantity
        #     old_product_id = old_instance.product_id
        # except StockMovementLineItem.DoesNotExist:
        #     old_qty= None
        #     old_product_id=None

        # old_qty = instance._old_quantity
        # old_product_id = instance._old_product_id
        if old_product_id != new_product.id:
            old_product = Product.objects.get(id = old_product_id)
            if movement_type == "in":
                old_product.current_stock  -= old_qty
                new_product.current_stock += new_qty
            else:
                old_product.current_stock += old_qty
                new_product.current_stock -= new_qty
            old_product.save()
            new_product.save()
        else:
            



            diff = new_qty - old_qty
            if movement_type == 'in':
                new_product.current_stock += diff
            else: 
                new_product.current_stock -= diff
            new_product.save()



@receiver(post_delete, sender=StockMovementLineItem)
def update_product_stock_on_delete(sender, instance, **kwargs):
    product = instance.product
    qty = instance.quantity
    movement_type = instance.stock_movement.transaction_type
    if movement_type == "in":
        product.current_stock -= qty
    else:
        product.current_stock += qty
    product.save()


@receiver(pre_save, sender = Transaction)
def cache_old_transaction(sender, instance, **kwards):
    if instance.pk:
        try:
            old_instance = Transaction.objects.get(pk = instance.pk)
            instance._old_amount = old_instance.amount
            instance._old_type = old_instance.transaction_type
            instance._old_accont_id = old_instance.account_id
        except Transaction.DoesNotExist:
            instance._old_amount = None
            instance._old_type = None
            instance._old_accont_id = None
    else:
        instance._old_amount = None
        instance._old_type = None
        instance._old_accont_id = None

    
@receiver(post_save, sender = Transaction)
def update_account_balance_on_save(sender, instance, created, **kwargs):
    account = instance.account
    amount= instance.amount
    transaction_type = instance.transaction_type

    if created:
        if transaction_type == 'dr':
            account.balance -= amount
        else: 
            account.balance += amount
        account.save()
    else:
        #reverse old transaction, apply new one
        old_amount = getattr(instance, '_old_amount',None)
        old_type = getattr(instance, '_old_type',None)
        old_account_id = getattr(instance, '_old_account_id',None)

        if old_account_id and old_account_id != account.id:
            #Transaciton moved to another accouct: revert old,
            old_account = Account.objects.get(id = old_account_id)
            if old_type == 'dr':
                old_account.balance += old_amount
            else: 
                old_account.balance -+ old_amount
            old_account.save()

            #giving effect to new account
            if transaction_type == 'dr':
                account.balance -= amount
            else:
                account.balacne += amount
            account.save()
        else:
            #same account, reverse and apply, alternatively, take difference but that will be complex if it changes type.

            #Reverse
            if old_type == 'dr':
                account.balance += old_amount
            else:
                account.balance -= old_amount
            
            #new effect
            if transaction_type == 'dr':
                account.balance -= amount
            else:
                account.balance += amount

            account.save()


@receiver(post_delete,sender = Transaction)
def update_account_balance_on_delete(sender, instance, **kwargs):
    account = instance.account
    amount = instance.amount
    transaction_type = instance.transaction_type

    if transaction_type == 'dr':
        account.balance += amount
    else:
        account.balance -= amount
    account.save()










    


