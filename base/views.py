from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate,logout,login
from django.contrib.auth.decorators import login_required

def index(request):
    query = request.GET.get('search')
    if query != None:
        products = Product.objects.filter(Q(title__icontains=query))
        context = {'product':products}
        return render(request,'base/all_products.html',context)
    
    products = Product.objects.all().order_by('id')
    context = {'product':products}
    return render(request, 'base/index.html',context)

def all_products(request):
    query = request.GET.get('search')
    print(query)
    if query != None:
        products = Product.objects.filter(Q(title__icontains=query))
    else:
        products = Product.objects.all().order_by('id')

    context = {'product':products}
    return render(request, 'base/all_products.html',context)

def product(request,pk):
    product = Product.objects.get(id = pk)
    review = Review.objects.filter(product=product)
    previous_page = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.save()
            print(previous_page)
            return redirect(previous_page)
    else:
        form = ReviewForm()

    context = {'product':product,'review':review,'form':form}

    return render(request,'base/product.html',context)


def register(request):

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = user.email.lower()
            user.save()
            login(request,user)
            return redirect('index')
        else:
            messages.error(request, 'An error occurred during registration')
    else:
        form = UserForm()
    return render(request,'base/register.html',{'form':form})

def login_page(request):

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = CustomUser.objects.get(email=email)
        except:
            messages.error(request,"User doesn't exist")
        user = authenticate(request,email=email,password=password)

        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            messages.error(request,'Invalid credentials')
    context= {}
    return render(request,'base/login.html',context)


def logout_page(request):
    logout(request)
    return redirect('index')

@login_required(login_url='login_page')
def item_cart(request):
    if request.method == 'POST':
        cart = request.user
    user = request.user
    cart = Cart.objects.get(user=user)
    cart_products = CartItem.objects.filter(cart=cart)
    price_array = [x.product.price for x in cart_products]
    total = sum(price_array)
    context={'cart_products':cart_products,'total':total}
    return render(request,'base/cart.html',context)

def add_to_cart(request,id):

    product = Product.objects.get(id=id)
    cart = Cart.objects.get(user=request.user)
    cart_item = CartItem.objects.create(cart=cart,product=product)
    cart_item.save()
    return redirect('cart')

def remove_from_cart(request,id):
    cart_item = CartItem.objects.get(id=id)
    print(id,cart_item)
    cart_item.delete()
    return redirect('cart')