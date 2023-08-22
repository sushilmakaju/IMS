from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from .serializers import *
from django.contrib.auth.hashers import make_password
from django_filters.rest_framework import DjangoFilterBackend

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
        
class ProductApiView(GenericAPIView):
    filter_backends = [DjangoFilterBackend]
    serializer_class = Productserializers
    filterset_fields = ['product_name', 'stock']
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


      
