from django.shortcuts import render
from .models import User, Product

def list_users(request):
    users = User.objects.all()
    return render(request, 'list_users.html', {'users': users})

def products_in_stock(request):
    products = Product.objects.filter(stock__gt=0)
    return render(request, 'products.html', {'products': products})
