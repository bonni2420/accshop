from django.shortcuts import render
from accounts.models import Category
from customers.models import Customer

def index(request):
    return render(request, "core/index.html")