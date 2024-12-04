from django.db import models
from django.contrib.auth.models import User #import thêm thư viện lấy User
#auth xác thực
#User dùng tạo csdl thông tin người dùng
from django.contrib.auth.forms import UserCreationForm

class Menu(models.Model):
    sub_menu = models.ForeignKey('self',on_delete=models.CASCADE, related_name='sub_menu_s',null=True,blank=True)
    is_sub=models.BooleanField(default=False)
    name = models.CharField(max_length=200,null=True)
    slug = models.SlugField(max_length=200,unique=True)
    def __str__(self):
        return self.name

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name','password1','password2']
    
class Product(models.Model):
    menu = models.ManyToManyField(Menu, related_name='product')
    hangsx = models.CharField(max_length=200,null=True)
    name = models.CharField(max_length=200,null=True)
    price = models.FloatField() #giá có thể lẻ nên dùng trường số thực
    digital = models.BooleanField(default=False,null=True,blank=False)
    image = models.ImageField(null=True,blank=True)
    chitiet = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.name
    @property
    def ImageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class Order(models.Model):
    customer = models.ForeignKey(User,on_delete=models.SET_NULL, null=True,blank=True)
    date_order = models.DateField(auto_now_add=True)
    complete = models.BooleanField(default=False,null=True,blank=False)
    transaction_id = models.CharField(max_length=200,null=True)
    
    def __str__(self):
        return str(self.id)
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
class OrderItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.SET_NULL, null=True,blank=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL, null=True,blank=True)
    quantity = models.IntegerField(default=0,null=True,blank=True) # trường số nguyên
    date_added = models.DateTimeField(auto_now_add=True)
    # cái này k cần trả về nên k cần return
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class ShippingAddress(models.Model):
    customer = models.ForeignKey(User,on_delete=models.SET_NULL, null=True,blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    mobile = models.CharField(max_length=10,null=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    district = models.CharField(max_length=200, null=True, blank=True)
    ward = models.CharField(max_length=200, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email