from django.urls import path
from .views import *

urlpatterns = [
    path('login/',LoginAPIView.as_view(), name='login_view'),
    path('register/',register_view, name='register_view'),
    path('product/',ProductApiView.as_view(), name="ProductApiView"),
    path('buyerproductview/',BuyerProductApiView.as_view(), name="BuyerProductApiView"),
    path('product/<pk>',ProductApiView.as_view(), name="ProductApiView"),
    path('buyer/', BuyerApiView.as_view(), name='BuyerApiView'),
    path('buyer/<pk>', BuyerApiView.as_view(), name='BuyerApiView'),
    path('seller/', SellerApiView.as_view(), name='SellerApiView'),
    path('seller/<pk>', SellerApiView.as_view(), name='SellerApiView'),
    path('order', OrderApiView.as_view(), name='OrderApiVIew'),
    path('order/<pk>', OrderApiView.as_view(), name='OrderApiVIew'),
    path('sellerorderhistory', SellerOrderHistoryView.as_view(), name="SellerOrderHistoryView"),
    path('sellerorderdashboard/', SellerOrderView.as_view(), name='SellerOrderView'),
    path('sellerorderdashboard/<pk>', SellerOrderView.as_view(), name='SellerOrderView')
]