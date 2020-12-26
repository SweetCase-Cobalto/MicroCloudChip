from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse\

import os

from .models import User

#save_session_function
def save_session(request, user_id, user_pswd):
    request.session['user_id'] = user_id
    request.session['user_pswd'] = user_pswd

# Create your views here.
def login_page(request):
    return render(request, 'app/login.html')
 
def login(request):
    if request.method == "POST":
        login_id = request.POST['id']
        login_pswd = request.POST['pswd']
        if len(User.objects.filter(userId=login_id).filter(pswd=login_pswd)) == 0:
            return HttpResponseRedirect(reverse('login-failed'))
        else:
            save_session(request, login_id, login_pswd)
            return HttpResponseRedirect(reverse('main-browser'))
    
def main_browser(request):

    # get id from session
    user_id = request.session['user_id']
    
    context = {"type": "browser", "user_id": user_id}
    return render(request, 'app/main.html', context)

def main_setting(request):
    context = {"type": "setting"}
    return render(request, 'app/main.html', context)

def main_about(request):
    context = {"type": "about"}
    return render(request, 'app/main.html', context)

def login_failed(request):
    return render(request, 'app/login_failed.html')