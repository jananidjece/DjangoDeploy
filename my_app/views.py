from django.shortcuts import render, redirect
from .models import *
from rest_framework.views import APIView
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
import requests
from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view



# Create your views here.
def homePage(request):
    return render(request, 'home.html')

def productPage(request):
    productList = ProductInfo.objects.all()
    return render(request, 'product.html',{"product":productList})

def signupPage(request):
    return render(request,"signup.html")
def loginPage(request):
    return render(request,"login.html")

def adminDashboard(request):
    return render(request, "adminPage.html")

def dashboard(request):
    return render(request, "dashboard.html")

class UserSignupAPI(APIView):
    def post(self, request):
        try:
            serializer = UserOtherInfoSerializer(data = request.data)
            if serializer.is_valid():
                user = serializer.save()
                refresh_token = RefreshToken.for_user(user)
                access_token = refresh_token.access_token
                return Response({'refresh':str(refresh_token),'access':str(access_token), 'data':serializer.data}, status=status.HTTP_201_CREATED)
        except Exception:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# SIGNUP_API_URL = "http://127.0.0.1:8000/token/"
def signupPage_view(request):
    if request.method == "POST":
        data = {
            "first_name": request.POST.get("firstname"),
            "last_name": request.POST.get("lastname"),
            "username": request.POST.get("username"),
            "email": request.POST.get("email"),
            "password": request.POST.get("password"),
        }
    
        try:
            serializer = UserOtherInfoSerializer(data = data)
            print("iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")
            if serializer.is_valid():
                user = serializer.save()
                refresh_token = RefreshToken.for_user(user)
                access_token = refresh_token.access_token
                # return Response({'refresh':str(refresh_token),'access':str(access_token), 'data':serializer.data}, status=status.HTTP_201_CREATED)
                print("jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj")
                return redirect('login') 
        except Exception:
            # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            print("gggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggg")
            return redirect('signup') 

    return render(request, "signup.html")

# class UserLoginAPI(TokenObtainPairView):
#     permission_classes = [AllowAny]
#     serializer_class = UserLoginSerializer

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # 🔑 Superuser check
            if user.is_superuser:
             return redirect('adminDashboard')
        else:
            return redirect('productPage')

    return redirect('login')
#----------------------------------------------------------API---------------------------------------------
class ProductDashAPI(APIView):
    def post(self, request):
       
       serializer = ProductInfoSerializer(data=request.data)

       if serializer.is_valid():
        serializer.save()
        return Response(
            {
                "message": "Product created successfully",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        )

       return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

 
    def get(self, request, productId = None):
        try:
            if productId:
                product = ProductInfo.objects.get(id = productId)
                serializer = ProductInfoSerializer(product)
                return Response (serializer.data, status=status.HTTP_200_OK)
            else:
                products = ProductInfo.objects.all()
                serializer = ProductInfoSerializer(products, many = True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception:
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)   


    def put(self, request, productId):
        try:
            if productId:
               product = ProductInfo.objects.get(id = productId)
               serializer = ProductInfoSerializer(product, data = request.data, partial = True)
               if serializer.is_valid():
                   serializer.save()
                   return Response({"Message":"Product Updated Successfully", "data": serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({"message":"Id Must"})
        except Exception:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
               
         
    def delete(self, request, productId):
        try:
            if productId:
               product = ProductInfo.objects.get(id = productId)
               product.delete()
               return Response({"Message" :"Product deteted successfully"}, status=status.HTTP_200_OK)

            else:
                return Response({"Message":"Id Must"})
        except Exception as e:
            return Response(str(e),status=status.HTTP_400_BAD_REQUEST)

API_BASE_URL = "http://127.0.0.1:8000/productAPI/" 
def productDash_view(request):
    get_data = requests.get(API_BASE_URL)
    show_products = get_data.json()
    return render(request, "productDash.html",{"product":show_products})

def addProduct_view(request):
    categories = ProductCategory.objects.all()
    if request.method == "POST":
        data = {
            "product_name": request.POST.get("product_name"),
            "product_description": request.POST.get("product_description"),
            "product_price": request.POST.get("product_price"),
            "product_category": request.POST.get("product_category"),
        }

        files = {
            "product_image": request.FILES.get("product_image")
        }

        requests.post(API_BASE_URL, data=data, files=files)
        return redirect('productDash')

    return render(request, "add.html",{"categories": categories})



def editProduct_view(request, product_id):
    product = requests.get(f"{API_BASE_URL}{product_id}/").json()
    categories = ProductCategory.objects.all()

    if request.method == "POST":
        data = {
            "product_name": request.POST.get("product_name"),
            "product_description": request.POST.get("product_description"),
            "product_price": request.POST.get("product_price"),
            "product_category": request.POST.get("product_category"),
        }

        files = {}
        if request.FILES.get("product_image"):
            files["product_image"] = request.FILES.get("product_image")

        requests.put(
            f"{API_BASE_URL}{product_id}/",
            data=data,
            files=files
        )

        return redirect("productDash")

    return render(request, "edit.html", {"dress": product, "categories": categories})



def deleteProduct_view(request, product_id):
    if request.method == "POST":
        requests.delete(f"{API_BASE_URL}{product_id}/")
        return redirect("productDash")
    product = requests.get(f"{API_BASE_URL}{product_id}/").json()
    return render(request, "delete.html",{"dress": product})



























