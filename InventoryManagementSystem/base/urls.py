from django.urls import path
from .views import *

urlpatterns = [
    path('login/',LoginAPIView.as_view(), name='login_view'),
    path('register/',register_view, name='register_view'),
    path('product/',ProductApiView.as_view(), name="ProductApiView"),
    path('product/<pk>',ProductApiView.as_view(), name="ProductApiView"),
    path('buyer/', BuyerApiView.as_view(), name='BuyerApiView'),
    path('buyer/', BuyerApiView.as_view(), name='BuyerApiView'),
]