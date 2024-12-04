from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from .models import *
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import ShippingAddress, Order

def placeorder(request):
    if request.method == "POST":
        customer = request.user if request.user.is_authenticated else None
        name = request.POST.get('name')
        mobile = request.POST.get('phone')
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get('city')
        district = request.POST.get('district')
        ward = request.POST.get('ward')
        
        shipping_address = ShippingAddress.objects.create(
            customer=customer,
            name = name,
            mobile=mobile,
            email=email,
            address=address,
            city=city,
            district=district,
            ward=ward
        )
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        items =[]
        order = {'get_cart_items':0,'get_cart_total':0}
        cartItems = order['get_cart_items']
        user_not_login = "show"
        user_login = "hidden"
    menus = Menu.objects.filter(is_sub=False)
    context={'menus':menus,'items':items,'order':order,'cartItems': cartItems,'user_not_login':user_not_login,'user_login':user_login}
    return render(request,'app/placeorder.html',context)

def tracuudonhang(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        items =[]
        order = {'get_cart_items':0,'get_cart_total':0}
        cartItems = order['get_cart_items']
        user_not_login = "show"
        user_login = "hidden"
    menus = Menu.objects.filter(is_sub=False)
    context={'menus':menus,'items':items,'order':order,'cartItems': cartItems,'user_not_login':user_not_login,'user_login':user_login}
    return render(request,'app/tracuudonhang.html',context)

def chitiet(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        items =[]
        order = {'get_cart_items':0,'get_cart_total':0}
        cartItems = order['get_cart_items']
        user_not_login = "show"   
        user_login = "hidden"
    id = request.GET.get('id','')
    products = Product.objects.filter(id=id)
    menus = Menu.objects.filter(is_sub=False)
    context={'products':products, 'menus':menus,'items':items,'order':order,'cartItems': cartItems,'user_not_login':user_not_login,'user_login':user_login}
    return render(request,'app/chitiet.html',context)

def menu(request):
    menus = Menu.objects.filter(is_sub=False)
    active_menu = request.GET.get('menu','')
    if active_menu:
        products = Product.objects.filter(menu__slug = active_menu)
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        items =[]
        order = {'get_cart_items':0,'get_cart_total':0}
        cartItems = order['get_cart_items']
        user_not_login = "show"
        user_login = "hidden"
    context = {'cartItems': cartItems,'menus':menus,'products':products,'active_menu':active_menu,'user_not_login':user_not_login,'user_login':user_login} 
    return render(request,'app/menu.html',context)

def search(request):
    if request.method == "POST":
        searched=request.POST["searched"]
        keys=Product.objects.filter(name__contains = searched)
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        items =[]
        order = {'get_cart_items':0,'get_cart_total':0}
        cartItems = order['get_cart_items']
        user_not_login = "show"
        user_login = "hidden"
    menus = Menu.objects.filter(is_sub=False)
    active_menu = request.GET.get('menu','')
    products = Product.objects.all()
    return render(request,'app/search.html',{"menus":menus,"searched":searched,"keys":keys,'products': products,'cartItems': cartItems,'user_not_login':user_not_login,'user_login':user_login})

def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else: 
        items =[]
        order = {'get_cart_items':0,'get_cart_total':0}
        cartItems = order['get_cart_items']
        user_not_login = "show"
        user_login = "hidden"
    menus = Menu.objects.filter(is_sub=False)
    context = {'menus':menus,'cartItems': cartItems,'form':form,'user_not_login':user_not_login,'user_login':user_login} 
    return render(request,'app/register.html',context,)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else: messages.info(request, 'Tên đăng nhập và mật khẩu không đúng!')
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else: 
        items =[]
        order = {'get_cart_items':0,'get_cart_total':0}
        cartItems = order['get_cart_items']
        user_not_login = "show"
        user_login = "hidden"
    menus = Menu.objects.filter(is_sub=False)
    context = {'menus':menus,'cartItems': cartItems,'user_not_login':user_not_login,'user_login':user_login}
    return render(request,'app/login.html',context)

def logoutPage(request):
    logout(request)
    return redirect('login')

def home(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden" # và ẩn dk dn
        user_login = "show" #nếu đăng nhập thì hiện chào
    else:
        items =[]
        order = {'get_cart_items':0,'get_cart_total':0}
        cartItems = order['get_cart_items']
        user_not_login = "show" # ch đăng nhập thì hiện dk dn
        user_login = "hidden" # và ẩn chào 
    menus = Menu.objects.filter(is_sub=False)
    products = Product.objects.all()
    context={'menus':menus,'products': products,'cartItems': cartItems,'user_not_login':user_not_login,'user_login':user_login}
    return render(request,'app/home.html',context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        items =[]
        order = {'get_cart_items':0,'get_cart_total':0}
        cartItems = order['get_cart_items']
        user_not_login = "show"
        user_login = "hidden"
    menus = Menu.objects.filter(is_sub=False)
    context={'menus':menus,'items':items,'order':order,'cartItems': cartItems,'user_not_login':user_not_login,'user_login':user_login}
    return render(request,'app/cart.html',context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        items =[]
        order = {'get_cart_items':0,'get_cart_total':0}
        cartItems = order['get_cart_items']
        user_not_login = "show"
        user_login = "hidden"
    menus = Menu.objects.filter(is_sub=False)
    context={'menus':menus,'items':items,'order':order,'cartItems': cartItems,'user_not_login':user_not_login,'user_login':user_login}
    return render(request,'app/checkout.html',context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user
    product = Product.objects.get(id = productId)
    order, created = Order.objects.get_or_create(customer = customer, complete = False)
    orderItem, created = OrderItem.objects.get_or_create(order = order, product = product)
    if action == 'add':
        orderItem.quantity +=1
    elif action == 'remove':
        orderItem.quantity -=1
    orderItem.save()
    if orderItem.quantity<=0:
        orderItem.delete()
    return JsonResponse('added', safe=False)