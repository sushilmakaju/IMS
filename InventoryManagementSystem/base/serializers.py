from rest_framework import serializers
from .models import *

class Userserializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class Buyerserializers(serializers.ModelSerializer):
    class Meta:
        model = Buyer
        fields = '__all__'

class Sellerserializers(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = '__all__'

class Productserializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class Orderserializers(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

# class OrderedItemserializers(serializers.ModelSerializer):
#     class Meta:
#         model = OrderItem
#         fields = '__all__'
