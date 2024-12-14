from django.contrib import admin
from django.urls import path
from . import views
from .views import placeorder
# from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name="home"),
    path('register/', views.register, name="register"),
    path('login/', views.loginPage, name="login"),
    path('search/', views.search, name="search"),
    path('menu/', views.menu, name="menu"),
    path('tracuudonhang/', views.tracuudonhang, name="tracuudonhang"),
    path('aboutus/', views.aboutus, name="aboutus"),
    path('chitiet/', views.chitiet, name="chitiet"),
    path('logout/', views.logoutPage, name="logout"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name="update_item"),
    path('placeorder/', views.placeorder, name="placeorder"),
    path('ForgetPassword/', views.ForgetPassword, name="forget_password"),
    path('newpasswordpage/<str:uidb64>/<str:token>/', views.NewPasswordPage, name="new_password"),
    path('doimatkhau/', views.Change_Password, name="doimatkhau"),
    path('suahoso/', views.Sua_Ho_So, name="suahoso"),
]