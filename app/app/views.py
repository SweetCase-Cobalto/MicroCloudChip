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
    return HttpResponseRedirect(reverse('main'))

def main(request):
    #return render(request, 'app/login_failed.html')
    return render(request, 'app/main.html')

def login_failed(request):
    return render(request, 'app/login_failed.html')