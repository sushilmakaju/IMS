from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from .serializers import *
from django.contrib.auth.hashers import make_password
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import *
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters

#Login 
class LoginAPIView(GenericAPIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        # if not email or not password:
        #     return Response({'error': 'email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=email, password=password)
        
        if user:
            token,_ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

#Register 
@api_view(['POST'])

def register_view(request):

    if request.method == 'POST':
        request.data['username'] = 'user'
        
        password = request.data.get("password")
        hash_password = make_password(password)
        request.data['password'] = hash_password
        serializer = Userserializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('user created')
        else:
            return Response(serializer.errors)
        
#product view for seller and CRUD 
class ProductApiView(GenericAPIView):
    filter_backends = [filters.SearchFilter]
    serializer_class = Productserializers
    search_fields =  ['product_name', 'stock']
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, SellerUserPermission]
    
    
    def get (self, request) :
        product_obj = Product.objects.all()
        product_filter = self.filter_queryset(product_obj)
        serializer = self.serializer_class(product_filter, many=True)
        return Response(serializer.data)
    
    def post (self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                'message': 'Product added successfully',
                'data': serializer.data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)
    
    def put (self, request, pk):
        try:
            product_obj = Product.objects.get(id = pk)
        except:
            return Response('Data Not Found!')
        serializer = self.serializer_class(product_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    
    def delete(self, request, pk):
        try:
            product_obj = Product.objects.filter(id = pk)
        except:
            return Response('Data Not Found!')
        product_obj.delete()
        return Response('Data Deleted!')

#Product view for buyer 
class BuyerProductApiView(GenericAPIView):
    filter_backends = [filters.SearchFilter]
    serializer_class = Productserializers
    search_fields = ['product_name', 'stock']
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, BuyerUserPermission]
    
    def get (self, request) :
        product_obj = Product.objects.all()
        product_filter = self.filter_queryset(product_obj)
        serializer = self.serializer_class(product_filter, many=True)
        return Response(serializer.data)
   
#view for buyer details and crud 
class BuyerApiView(GenericAPIView):
    filter_backends = [filters.SearchFilter]
    serializer_class = Buyerserializers
    search_fields = ['name', 'phone_number']
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, BuyerUserPermission]

    def get(self, request):
        buyer_obj = Buyer.objects.all()
        buyer_filter = self.filter_queryset(buyer_obj)
        serializer = self.serializer_class(buyer_filter, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                'message': 'Buyer added successfully',
                'data': serializer.data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)
        
    def put(self, request, pk):
        try:
            buyer_obj = Buyer.objects.get(id = pk)
        except:
            return Response('Data Not Found!')
        serializer = self.serializer_class(buyer_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    
    def delete(self, request, pk):
        try:
            buyer_obj = Buyer.objects.filter(id = pk)
        except:
            return Response('Data Not Found!')
        buyer_obj.delete()
        return Response('Data Deleted!')

#view for seller details and crud
class SellerApiView(GenericAPIView):
    filter_backends = [DjangoFilterBackend]
    serializer_class = Sellerserializers
    filterset_fields = ['name', 'phone_number']
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, SellerUserPermission]

    def get(self, request):
        seller_obj = Buyer.objects.all()
        seller_filter = self.filter_queryset(seller_obj)
        serializer = self.serializer_class(seller_filter, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                'message': 'seller added successfully',
                'data': serializer.data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)
        
    def put(self, request, pk):
        try:
            seller_obj = Seller.objects.get(id = pk)
        except:
            return Response('Data Not Found!')
        serializer = self.serializer_class(seller_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    
    def delete(self, request, pk):
        try:
            seller_obj = Seller.objects.filter(id = pk)
        except:
            return Response('Data Not Found!')
        seller_obj.delete()
        return Response('seller Data Deleted!')
    
#view for placing order for buyer
class OrderApiView(GenericAPIView):
    filter_backends = [filters.SearchFilter]
    serializer_class = Orderserializers
    search_fields = ['order_date']
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, BuyerUserPermission]

    def get(self, request):
        order_obj = Order.objects.all()
        order_filter = self.filter_queryset(order_obj)
        serializer = self.serializer_class(order_filter, many = True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                'message': 'Order Placed successfully',
                'data': serializer.data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)
    
    def put(self, request, pk):
        try:
            order_obj = Order.objects.get(id = pk)
        except:
            return Response('Data Not Found!')
        serializer = self.serializer_class(order_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

#view for ordering item for buyer     
class OrderedItemApi(GenericAPIView):
    filter_backends = [filters.SearchFilter]
    serializer_class = Orderserializers
    search_fields = ['product']
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, BuyerUserPermission]

    def get(self, request):
        orderitemobject = Order.objects.all()
        orderitem_filter = self.filter_queryset(orderitemobject)
        orderitemserilizer = self.serializer_class(orderitem_filter, many = True)
        return Response(orderitemserilizer.data)
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                'message': 'Orderitem Placed successfully',
                'data': serializer.data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)
    
    def put(self, request, pk):
        try:
            order_obj = Order.objects.get(id = pk)
        except:
            return Response('Data Not Found!')
        serializer = self.serializer_class(order_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
# view for accepting order for seller 
class SellerOrderView(GenericAPIView):
    filter_backends = [filters.SearchFilter]
    serializer_class = Orderserializers
    search_fields = ['status']
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, SellerUserPermission]
    def get(self, request):
        # Fetch pending orders for the authenticated seller
        orders = Order.objects.filter(status='Pending')
        serializer = Orderserializers(orders, many=True)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            order = Order.objects.get(id=pk)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Process the order and update status
        order.status = 'accepted'
        order.save()

        # Update product quantities
        for order_item in order.orderitem_set.all():
            product = order_item.product
            print(f"Product: {product}, Initial Stock: {product.stock}, Quantity: {order_item.quantity}")
            product.stock -= order_item.quantity
            print(f"Updated Stock: {product.stock}")
            product.save()

        return Response({'message': 'Order accepted'})

        

        








      
