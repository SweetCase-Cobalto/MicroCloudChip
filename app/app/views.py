from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

import os

# Create your views here.
def login_page(request):
    return render(request, 'app/login.html')
 
def login(request):
    print(request.POST)
    return HttpResponseRedirect(reverse('main-browser'))
    
def main_browser(request):
    context = {"type": "browser"}
    return render(request, 'app/main.html', context)

def main_setting(request):
    context = {"type": "setting"}
    return render(request, 'app/main.html', context)

def main_about(request):
    context = {"type": "about"}
    return render(request, 'app/main.html', context)

def login_failed(request):
    return render(request, 'app/login_failed.html')