from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def base(request):
    return render(request, 'leidos_app/base.html')

def login(request):
    return render(request, 'leidos_app/login.html')

def register(request):
    return render(request, 'leidos_app/register.html')

def create_menu(request):
    return render(request, 'leidos_app/create_menu.html')  

def menu(request):
    return render(request, 'leidos_app/menu.html')  