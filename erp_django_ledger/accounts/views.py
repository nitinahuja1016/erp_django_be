from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .services import *
from .serializers import *

# Create your views here.
class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class StockMovementViewSet(viewsets.ModelViewSet):
    queryset = StockMovement.objects.all()
    serializer_class = StockMovementSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

class StockMovementLineItemViewSet(viewsets.ModelViewSet):
    queryset = StockMovementLineItem.objects.all()
    serializer_class = StockMovementLineItemSerializer

class TransactionLineItemViewSet(viewsets.ModelViewSet):
    queryset = TransactionLineItem.objects.all()
    serializer_class = TransactionLineItemSerializer

class PurchaseCreateView(APIView):
    def post(self, request):
        serializer = PurchaseSerializer(data = request.data)
        if serializer.is_valid():
            vendor = serializer.validated_data['vendor']
            line_items_data = serializer.validated_data['line_items']
            line_items = [(item['product'],item['quantity'],item['price']) for item in line_items_data]
            movement, txn = process_purchase(account = vendor, vendor = vendor, line_items= line_items)

            return Response({
                'message':'Purchase created successfully'
            },status = status.HTTP_201_CREATED ) 
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
