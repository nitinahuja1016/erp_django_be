from rest_framework import serializers
from .models import *   

class AccountSerializer(serializers.ModelSerializer):
    account_type = serializers.ChoiceField(choices=Account.ACCOUNT_TYPES)

    class Meta:
        model = Account
        # fields = ['id','name', 'account_type','opening_balance', 'balance' ]
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'




class TransactionSerializer(serializers.ModelSerializer):
    transaction_type = serializers.ChoiceField(choices = Transaction.TRANSACTION_TYPE)
    class Meta:
        model = Transaction
        fields = '__all__'

class StockMovementLineItemSerializer(serializers.ModelSerializer):
    # stock_movement = StockMovementSerializer()
    # Product = ProductSerializer()

    class Meta:
        model = StockMovementLineItem
        fields = ['product','quantity']
        # exclude = ['stock_movement'] # not sure why stock movement is this left out,but it says that inner seraizlier should not even know about stock movement and it should be save programatically
        #alternatively, try adding stock movement as serializer by uncommenting 1st line of this serializer

class StockMovementSerializer(serializers.ModelSerializer):
    transaction_type = serializers.ChoiceField(choices = StockMovement.TRANSACTION_STATUS)
    # line_items = StockMovementLineItemSerializer(many=True, read_only=True)  # added line items in stock, this is mapped in reversed! read only true ignores it in save and update and will only fetch in view
    line_items = StockMovementLineItemSerializer(many=True)  # added line items in stock, this is mapped in reversed! read only true ignores it in save and update and will only fetch in view
    class Meta:
        model = StockMovement
        # fields = '__all__'
        fields = ['id', 'transaction_type', 'created_at', 'line_items']
        read_only_fields= ['created_at']
    

    def create(self, validated_data):
        print("inside create method")
        line_items_data = validated_data.pop('line_items')
        print(f"{len(line_items_data)} line items received")
        stock_movement = StockMovement.objects.create(**validated_data)
        print("Stock Movement created: ",stock_movement)
        for line_item in line_items_data:
            StockMovementLineItem.objects.create(stock_movement = stock_movement,**line_item)
        return stock_movement
    
    def update(self, instance, validated_data):
        line_items_data = validated_data.pop('line_items')
        instance.transaction_type  = validated_data.get('transaction_type',instance.transaction_type)
        instance.save()

        instance.line_items.all().delete()

        for line_data in line_items_data:
            StockMovementLineItem.objects.create(stock_movement = instance, **line_data)
        
        return instance

class TransactionLineItemSerializer(serializers.ModelSerializer):
    # transaction = TransactionSerializer()
    # product = ProductSerializer()
    class Meta:
        model = TransactionLineItem
        fields = '__all__'


class PurchaseLineItemSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(queryset = Product.objects.all())
    quantity = serializers.IntegerField()
    price = serializers.DecimalField(max_digits = 12, decimal_places = 2)

class PurchaseSerializer(serializers.Serializer):
    vendor = serializers.PrimaryKeyRelatedField(queryset = Account.objects.filter(account_type = 'vendor'))
    line_items = PurchaseLineItemSerializer(many=True)
    


    # quantity =
    # price = 