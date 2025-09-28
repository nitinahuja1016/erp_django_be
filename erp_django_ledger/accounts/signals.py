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


