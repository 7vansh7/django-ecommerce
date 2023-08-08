from django.shortcuts import render
from .models import Product

# Create your views here.

def index(request):
    product = Product.objects.all()
    context = {'product':product}
    return render(request, 'base/index.html',context)

def product(request,pk):
    product = Product.objects.get(id=pk)
    context = {'product':product}
    return render(request, 'base/product.html',context)