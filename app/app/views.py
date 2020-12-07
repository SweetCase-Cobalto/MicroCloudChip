from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

import os

# Create your views here.
def login(request):
    return render(request, 'app/login.html')