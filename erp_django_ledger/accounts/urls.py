from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'accounts',AccountViewSet)
router.register(r'product',ProductViewSet)
router.register(r'stock-movement',StockMovementViewSet)
router.register(r'transaction',TransactionViewSet)
router.register(r'stock-movement-line-item',StockMovementLineItemViewSet)
router.register(r'transaction-line-item',TransactionLineItemViewSet)

urlpatterns = [
    path('',include(router.urls)),
    path('purchase/',PurchaseCreateView.as_view(),name = 'purchase-create')
]
