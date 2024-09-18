from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm 

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

class Category(models.Model):
    sub_category = models.ForeignKey('self', on_delete=models.CASCADE, related_name='sub_categories', null=True, blank=True)
    is_sub = models.BooleanField(default=False)
    name = models.CharField(max_length=200, null=True)
    slug = models.SlugField(max_length=200, unique=True)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    category = models.ManyToManyField(Category, related_name='product')
    price = models.FloatField()
    digital = models.BooleanField(default=False, null=True, blank=False)
    img = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    @property
    def ImgUrl(self):
        try:
            url = self.img.url
        except:
            url = ''
        return url
    
class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    date_order = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)
    
    def __str__(self):
        return str(self.id)
    
    @property
    def get_num_items(self):
        orderitems = self.order_detail_set.all()
        nums = sum([item.quantity for item in orderitems])
        return nums
    
    @property
    def get_total_amount_items(self):
        orderitems = self.order_detail_set.all()
        total = sum([item.get_total_amount_item for item in orderitems])
        return total
    
class Order_detail(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total_amount_item(self):
        total = self.product.price * self.quantity
        return total

class ShippingAddress(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    phone_number = models.CharField(max_length=10, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
