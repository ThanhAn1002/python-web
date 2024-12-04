from django.contrib import admin
from django.urls import path
from . import views
from .views import placeorder

urlpatterns = [
    path('', views.home, name="home"),
    path('register/', views.register, name="register"),
    path('login/', views.loginPage, name="login"),
    path('search/', views.search, name="search"),
    path('menu/', views.menu, name="menu"),
    path('tracuudonhang/', views.tracuudonhang, name="tracuudonhang"),
    path('chitiet/', views.chitiet, name="chitiet"),
    path('logout/', views.logoutPage, name="logout"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name="update_item"),
    path('placeorder/', views.placeorder, name="placeorder"),

]