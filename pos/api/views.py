from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from pos_app.models import (
    User, StatusModel, TableResto, Profile, Category, MenuResto, OrderMenu, OrderMenuDetail
)
from api.serializers import (
    TableRestoSerializer, CategorySerializer, MenuRestoSerializer, RegisterUserSerializer, LoginSerializer
)
from rest_framework import generics
from rest_framework.authtoken.models import Token
from django.contrib.auth import login as django_login, logout as django_logout
from django.http import HttpResponse, JsonResponse
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny

class RegisterUserApiView(APIView):
    serializer_class = RegisterUserSerializer

    def post(self, request, format = None):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                'status' : status.HTTP_201_CREATED,
                'message' : "Selamat Anda Telah Terdaftar",
                'data' : serializer.data,
            }
            return Response(response_data, status = status.HTTP_201_CREATED)
        return Response(
            {
                'status' : status.HTTP_400_BAD_REQUEST,
                'data' : serializer.errors
            }, status = status.HTTP_400_BAD_REQUEST
        )
    
class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        user = serializer.validated_data['user']
        django_login(request, user)
        token, created = Token.objects.get_or_create(user = user)
        return JsonResponse({
            'status' : 200,
            'message' : "Selamat anda berhasil masuk...",
            'data' : {
                'token' : token.key,
                'id' : user.id,
                'first_name' : user.first_name,
                'last_name' : user.last_name,
                'email' : user.email,
                'is_active' : user.is_active,
                'is_waitress' : user.is_waitress,
            }
        })
     

class TableRestoListApiView(APIView):
    def get(self, request, *args, **kwargs):
        table_restos = TableResto.objects.all()
        serializer = TableRestoSerializer(table_restos, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        data = {
            'code' : request.data.get('code'),
            'name' : request.data.get('name'),
            'capacity' : request.data.get('capacity'),
        }
        serializer = TableRestoSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status' : status.HTTP_201_CREATED,
                'message' : "Data Created Successfully...",
                'data' : serializer.data,
            }
            return Response(response, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    
class TableRestoDetailApiView(APIView):
    def get_object(self, id):
        try:
            return TableResto.objects.get(id = id)
        except:
            return None
        
    def get(self, request, id, *args, **kwargs):
        table_resto_instances = self.get_object(id)
        if not table_resto_instances:
            return Response(
                {
                    'status' : status.HTTP_404_NOT_FOUND,
                    'message' : "Data does not exists...",
                    'data' : {}
                }, status = status.HTTP_404_NOT_FOUND
            )
        serializer = TableRestoSerializer(table_resto_instances)
        response = {
            'status' : status.HTTP_200_OK,
            'message' : "Data Retrieved Successfully...",
            'data' : serializer.data
        }
        return Response(response, status = status.HTTP_200_OK)
    
    def put(self, request, id, *args, **kwargs):
        table_resto_instances = self.get_object(id)
        if not table_resto_instances:
            return Response(
                {
                    'status' : status.HTTP_404_NOT_FOUND,
                    'message' : "Data does not exists...",
                    'data' : {}
                }, status = status.HTTP_404_NOT_FOUND
            )
        data = {
            'code' : request.data.get('code'),
            'name' : request.data.get('name'),
            'capacity' : request.data.get('capacity'),
            'table_status' : request.data.get('table_status'),
            'status' : request.data.get('status'),
        }
        serializer = TableRestoSerializer(table_resto_instances, data = data, partial = True)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status' : status.HTTP_200_OK,
                'message' : "Data Updated Successfully...",
                'data' : serializer.data
            }
            return Response(response, status = status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id, *args, **kwargs):
        table_resto_instance = self.get_object(id)
        if not table_resto_instance:
            return Response(
                {
                    'status' : status.HTTP_404_NOT_FOUND,
                    'message' : "Data does not exists...",
                    'data' : {}
                }, status = status.HTTP_404_NOT_FOUND
            )
        table_resto_instance.delete()
        response = {
            'status' : status.HTTP_200_OK,
            'message' : "Data Deleted Successfully...",
        }
        return Response(response, status = status.HTTP_200_OK)
    
class CategoryListApiView(APIView):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        serializers = CategorySerializer(categories, many = True)
        return Response(serializers.data, status = status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        data = {
            'name' : request.data.get('name'),
        }
        serializer = CategorySerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status' : status.HTTP_201_CREATED,
                'message' : "Data Created Successfully...",
                'data' : serializer.data,
            }
            return Response(response, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    
class CategoryDetailApiView(APIView):
    def get_object(self, id):
        try:
            return Category.objects.get(id = id)
        except:
            return None
        
    def get(self, request, id, *args, **kwargs):
        category_instances = self.get_object(id)
        if not category_instances:
            return Response(
                {
                    'status' : status.HTTP_404_NOT_FOUND,
                    'message' : "Data does not exists...",
                    'data' : {}
                }, status = status.HTTP_404_NOT_FOUND
            )
        serializer = CategorySerializer(category_instances)
        response = {
            'status' : status.HTTP_200_OK,
            'message' : "Data Retrieved Successfully...",
            'data' : serializer.data
        }
        return Response(response, status = status.HTTP_200_OK)
    
    def put(self, request, id, *args, **kwargs):
        category_instances = self.get_object(id)
        if not category_instances:
            return Response(
                {
                    'status' : status.HTTP_404_NOT_FOUND,
                    'message' : "Data does not exists...",
                    'data' : {}
                }, status = status.HTTP_404_NOT_FOUND
            )
        data = {
            'name' : request.data.get('name'),
            'status' : request.data.get('status'),
        }
        serializer = CategorySerializer(category_instances, data = data, partial = True)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status' : status.HTTP_200_OK,
                'message' : "Data Updated Successfully...",
                'data' : serializer.data
            }
            return Response(response, status = status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id, *args, **kwargs):
        category_instance = self.get_object(id)
        if not category_instance:
            return Response(
                {
                    'status' : status.HTTP_404_NOT_FOUND,
                    'message' : "Data does not exists...",
                    'data' : {}
                }, status = status.HTTP_404_NOT_FOUND
            )
        category_instance.delete()
        response = {
            'status' : status.HTTP_200_OK,
            'message' : "Data Deleted Successfully...",
        }
        return Response(response, status = status.HTTP_200_OK)
    
class MenuRestoListApiView(APIView):
    def get(self, request, *args, **kwargs):
        menu_restos = MenuResto.objects.all()
        serializer = MenuRestoSerializer(menu_restos, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        data = {
            'name' : request.data.get('name'),
            'price' : request.data.get('price'),
            'image_menu' : request.data.get('image_menu'),
            'category' : request.data.get('category'),
        }
        serializer = MenuRestoSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status' : status.HTTP_201_CREATED,
                'message' : "Data Created Successfully...",
                'data' : serializer.data,
            }
            return Response(response, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    
class MenuRestoDetailApiView(APIView):
    def get_object(self, id):
        try:
            return MenuResto.objects.get(id = id)
        except:
            return None
        
    def get(self, request, id, *args, **kwargs):
        menu_instances = self.get_object(id)
        if not menu_instances:
            return Response(
                {
                    'status' : status.HTTP_404_NOT_FOUND,
                    'message' : "Data does not exists...",
                    'data' : {}
                }, status = status.HTTP_404_NOT_FOUND
            )
        serializer = MenuRestoSerializer(menu_instances)
        response = {
            'status' : status.HTTP_200_OK,
            'message' : "Data Retrieved Successfully...",
            'data' : serializer.data
        }
        return Response(response, status = status.HTTP_200_OK)
    
    def put(self, request, id, *args, **kwargs):
        menu_instances = self.get_object(id)
        if not menu_instances:
            return Response(
                {
                    'status' : status.HTTP_404_NOT_FOUND,
                    'message' : "Data does not exists...",
                    'data' : {}
                }, status = status.HTTP_404_NOT_FOUND
            )
        data = {
            'name' : request.data.get('name'),
            'price' : request.data.get('price'),
            'image_menu' : request.FILES.get('image_menu'),
            'category' : request.data.get('category'),
            'menu_status' : request.data.get('menu_status'),
            'status' : request.data.get('status'),
        }
        serializer = MenuRestoSerializer(menu_instances, data = data, partial = True)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status' : status.HTTP_200_OK,
                'message' : "Data Updated Successfully...",
                'data' : serializer.data
            }
            return Response(response, status = status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id, *args, **kwargs):
        table_resto_instance = self.get_object(id)
        if not table_resto_instance:
            return Response(
                {
                    'status' : status.HTTP_404_NOT_FOUND,
                    'message' : "Data does not exists...",
                    'data' : {}
                }, status = status.HTTP_404_NOT_FOUND
            )
        table_resto_instance.delete()
        response = {
            'status' : status.HTTP_200_OK,
            'message' : "Data Deleted Successfully...",
        }
        return Response(response, status = status.HTTP_200_OK)
    
class MenuRestoView(APIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        menu_restos = MenuResto.objects.filter(status = 'Aktif')
        serializer = MenuRestoSerializer(menu_restos, many = True)
        response = {
            'status' : status.HTTP_200_OK,
            'message' : "Pembacaan seluruh data berhasil...",
            'user' : str(request.user),
            'auth' : str(request.auth),
            'data' : serializer.data
        }
        return Response(response, status = status.HTTP_200_OK)