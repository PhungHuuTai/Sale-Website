from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import *
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        items = order.order_detail_set.all()
        cartItem = order.get_num_items
    else:
        items = []
        order = {'get_num_items': 0,
                 'get_total_amount_items': 0}
        cartItem = order['get_num_items']
    
    categories = Category.objects.filter(is_sub=False)
    products = Product.objects.all()
    context = {'products': products,
               'cartItem': cartItem,
               'categories': categories}
    return render(request, 'app/home.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        items = order.order_detail_set.all()
        cartItem = order.get_num_items
    else:
        items = []
        order = {'get_num_items': 0,
                 'get_total_amount_items': 0}
        cartItem = order['get_num_items']

    categories = Category.objects.filter(is_sub=False)
    context = {'items': items,
               'order': order,
               'cartItem': cartItem,
               'categories': categories}
    return render(request, 'app/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        items = order.order_detail_set.all()
        cartItem = order.get_num_items
    else:
        items = []
        order = {'get_num_items': 0,
                 'get_total_amount_items': 0}
        cartItem = order['get_num_items']

    categories = Category.objects.filter(is_sub=False)
    context = {'items': items,
               'order': order,
               'cartItem': cartItem,
               'categories': categories}
    return render(request, 'app/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, completed=False)
    orderItem, created = Order_detail.objects.get_or_create(order=order, product=product)
    
    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('added', safe=False)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, "User or password isn't correct!")
            
    context = {}
    return render(request, 'app/login.html', context)

def logoutPage(request):
    logout(request)
    return redirect('login')

def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    context = {'form': form}
    return render(request, 'app/register.html', context)

def search(request):
    if request.method == 'POST':
        searched = request.POST["search"]
        keys = Product.objects.filter(name__contains=searched)
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        items = order.order_detail_set.all()
        cartItem = order.get_num_items
    else:
        items = []
        order = {'get_num_items': 0,
                 'get_total_amount_items': 0}
        cartItem = order['get_num_items']
        
    products = Product.objects.all()
    
    context = {"searched": searched,
                "keys": keys,
                'products': products,
                'cartItem': cartItem}
    return render(request, 'app/search.html', context)

def category(request):
    categories = Category.objects.filter(is_sub=False)
    active_category = request.GET.get('category', '')
    if active_category:
        products = Product.objects.filter(category__slug=active_category)
        context = {'categories': categories,
                   'active_category': active_category,
                   'products': products,}
        
    return render(request, 'app/category.html', context)
