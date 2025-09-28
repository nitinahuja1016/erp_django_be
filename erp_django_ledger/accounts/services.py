from django.db import transaction
from .models import *

def process_purchase(account, vendor, line_items, payment_amount=None):
    """
    1. StockMovement created
    2. Transaction create
    3. Loop for line items
        a. Stock Movement line items created
        b. Transaction line items created
    4. Total amount in transaction updated
    """
    with transaction.atomic():
        movement = StockMovement.objects.create(
            transaction_type = 'in'
        )
        txn = Transaction.object.create(
            account = vendor,
            # amount = total_amount,
            transaction_type = 'cr',
            stock_movement = movement
        )
        total_amount = 0
        for product, qty, price in line_items:
            StockMovementLineItem.objects.create(
                stock_movement = movement,
                product = product,
                quantity = qty
            )
            product.current_stock += qty
            #Review: Do we need to fetch product instance from objects.get before updating the current_qty?
            product.save()

            #This is fethcing price of product from product, but rather fetch it from purchase transaction
            total_amount += price * qty
            TransactionLineItem.objects.create(
                transaction = txn,
                product= product,
                quantity= qty,
                price = price,

            )
        #Try if this works or we will have to fetch the transaction instance?
        txn.amount = total_amount
        txn.save()
    

        
    return movement, txn