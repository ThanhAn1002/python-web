from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from .models import *
import json
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import ShippingAddress, Order
from django.core.mail import send_mail
from webbanhang.settings import EMAIL_HOST_USER
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

def Sua_Ho_So(request):
    user = request.user
    if request.method == "POST":
        new_username = request.POST.get("new_username")
        new_firstname = request.POST.get("new_firstname")
        new_email = request.POST.get("new_email")

        # Kiểm tra các thông tin đã tồn tại chưa
        if User.objects.filter(username=new_username).exists() and new_username != user.username:
            messages.error(request, "Tên đăng nhập đã tồn tại !")
            return redirect('suahoso')
        if User.objects.filter(email=new_email).exists() and new_email != user.email:
            messages.error(request, "Email đã tồn tại!")
            return redirect('suahoso')
        # Cập nhật thông tin người dùng
        user.username = new_username
        user.first_name = new_firstname
        user.email = new_email
        user.save()
        messages.success(request, "Cập nhật hồ sơ thành công !")
        return redirect('suahoso')
    
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
        return redirect('home')
    menus = Menu.objects.filter(is_sub=False)
    context={'menus':menus,'items':items,'order':order,'cartItems': cartItems,'user_not_login':user_not_login,'user_login':user_login}
    return render(request,'app/suahoso.html',context)

def Change_Password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        old_password = request.POST.get('old_password')
        if not request.user.check_password(old_password):
            messages.error(request, 'Mật khẩu cũ không đúng !')
            return redirect('doimatkhau')
        else:
            new_password1 = request.POST.get('new_password1')
            new_password2 = request.POST.get('new_password2')
            if new_password1 != new_password2:
                messages.error(request, 'Mật khẩu mới không khớp !')
                return redirect('doimatkhau')
            elif new_password1 == request.user.username:
                messages.error(request, 'Mật khẩu không được giống với tên đăng nhập !')
                return redirect('doimatkhau')
            elif new_password1 == old_password:
                messages.error(request, 'Mật khẩu mới trùng với mật khẩu cũ !')
                return redirect('doimatkhau')
            elif form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # không bị đăng xuất
                messages.success(request,'Mật khẩu đã được thay đổi thành công !')
                return redirect('doimatkhau')
    else:
        form = PasswordChangeForm(request.user)

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
        return redirect('home')
    menus = Menu.objects.filter(is_sub=False)
    context={'form': form,'menus':menus,'items':items,'order':order,'cartItems': cartItems,'user_not_login':user_not_login,'user_login':user_login}
    return render(request,'app/doimatkhau.html',context)

def ForgetPassword(request):
    if request.method == "POST":
        email = request.POST.get("email")
        print("Email:", email)
        
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            print("Người dùng tồn tại")

            # Tạo mã thông báo và mã hóa ID người dùng
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            reset_link = f"http://127.0.0.1:8000/newpasswordpage/{uid}/{token}/"
            send_mail(
                "Đặt lại mật khẩu trên AN_HOANG STORE",
                f"\nXin chào {user.username},\n\nChúng tôi đã nhận được yêu cầu đặt lại mật khẩu của bạn. Để đặt lại mật khẩu hãy bấm vào liên kết dưới đây:\n\n{reset_link}\n\nCảm ơn,\nAN_HOANG STORE",
                EMAIL_HOST_USER,
                [email],
                fail_silently=True
            )
            messages.info(request,'Mã xác minh đã gửi về email của bạn !')
            return redirect('forget_password')
        else:
            print("Người dùng không tồn tại")
            messages.error(request,'Email sai hoặc không tồn tại !')
            return redirect('forget_password')

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
    return render(request,'app/forget_password.html',context)

def NewPasswordPage(request, uidb64, token):
    # if request.user.is_authenticated:
    #     return redirect('home')
    try:
        # Giải mã uidb64 để lấy ID người dùng
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == "POST":
            pass1 = request.POST.get("password1")
            pass2 = request.POST.get("password2")
            # print("Pass1 and Pass2: ", pass1, pass2)
            if pass1 == pass2:
                user.set_password(pass1)
                user.save()
                messages.success(request,"Mật khẩu đã được đặt lại thành công !")
                return redirect('login')
            else:
                messages.error(request, "Mật khẩu mới không khớp !")
    else:
        messages.error(request, "Mã xác thực hết hiệu lực hoặc không tồn tại !")
        return redirect('forget_password')

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
    return render(request,'app/new_password.html',context)

def aboutus(request):
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
    return render(request,'app/aboutus.html',context)

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
    if request.user.is_authenticated:
        return redirect('home')
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            if User.objects.filter(email=email).exists():
                messages.error(request, "Email đã tồn tại !")
                return redirect('register')
            else:
                form.save()
                messages.success(request, "Tạo tài khoản thành công!")
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
        else: messages.error(request, 'Tên đăng nhập và mật khẩu không đúng!')
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
        messages.error(request, "Bạn cần đăng nhập để mua hàng !")
        return redirect('cart')
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