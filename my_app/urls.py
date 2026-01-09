from django.urls import path
from .views import *

urlpatterns = [
    path('', homePage, name = 'homePage'),
    path('productPage/', productPage, name = 'productPage'),
    path('signup/',signupPage, name = "signup" ),
    path('login/',loginPage, name = "login" ),
    path('token/', UserSignupAPI.as_view(), name = 'signupToken'),
    # path('user/token/obtain/', UserLoginAPI.as_view(), name = 'loginToken'),
    path('Signup_view/', signupPage_view, name = 'Signup_view'),
    path('login_view/',login_view, name = 'login_view'),
    path('adminDashboard/', adminDashboard, name = 'adminDashboard'),
    path('productDash/', productDash_view, name = 'productDash'),
    path('add/', addProduct_view, name = 'add'),
    path('edit/<int:product_id>/', editProduct_view, name = 'edit'),
    path('delete/<int:product_id>/', deleteProduct_view, name = 'delete'),
    path('dashborad/', dashboard, name ='dashboard'),
    path('productAPI/', ProductDashAPI.as_view()),
    path('productAPI/<int:productId>/',ProductDashAPI.as_view()),
]
