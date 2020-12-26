from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

import os

from .models import User

#save_session_function
def save_session(request, user_id, user_pswd):
    request.session['user_id'] = user_id

# Create your views here.
def login_page(request):
    # 이미 한번 로그인 해서 쳐 들어간 경우
    if 'user_id' in request.session:
        return HttpResponseRedirect(reverse('main-browser'))
    # 처음이에요
    return render(request, 'app/login.html')

# Login Redirection
def login(request):
    if request.method == "POST":
        login_id    = request.POST['id']
        login_pswd  = request.POST['pswd']

        # 로그인 테스트
        if len(User.objects.filter(userId=login_id).filter(pswd=login_pswd)) == 0:
            return HttpResponseRedirect(reverse('login-failed'))
        else:
            save_session(request, login_id, login_pswd)
            return HttpResponseRedirect(reverse('main-browser'))

# If login Failed
def login_failed(request):
    return render(request, 'app/login_failed.html')

# Logout
def logout(request):
    if 'user_id' in request.session:
        request.session.clear()
    return HttpResponseRedirect(reverse('login_page'))

# In Main Section
def main_browser(request):
    # get id from session
    user_id = request.session['user_id']
    context = {"type": "browser", "user_id": user_id}
    return render(request, 'app/main.html', context)

def main_setting(request):
    user_id = request.session['user_id']

    # Only admin

    # Search Setting ID
    l = User.objects.all()
    user_list = []
    for item in l:
        user_list.append(item.userId)

    context = {"type": "setting", "user_id": user_id, "user_list": user_list}
    return render(request, 'app/main.html', context)

def main_about(request):
    user_id = request.session['user_id']
    context = {"type": "about", "user_id": user_id}
    return render(request, 'app/main.html', context)

# Setting Section
def add_user_page(request):
    user_id = request.session['user_id']
    if user_id == 'admin':
        return render(request, 'app/main/settings_page/adduser.html')
    else:
        return 'error'

def adduser(request):
    # Is request is post ?& have session
    if (request.method == "POST") and ('user_id' in request.session):
        # Check This id is aleady exist
        new_id = request.POST['new_id']
        new_pswd = request.POST['new_pswd']

        # ID is aleady Exist
        if len(User.objects.filter(userId=new_id)) != 0:
            err_msg = 'THIS ID IS ALEADY EXISED'
            context = {"error_message": err_msg, "back_url": "adduser"}
            return render(request, 'app/err_page/incorrect_redirection.html', context)
        
        # Update new user
        new_user = User(userId=new_id, pswd=new_pswd)
        new_user.save()
        return HttpResponseRedirect(reverse('main-setting'))

def modify_user_page(request):
    user_id = request.session['user_id']
    if user_id == 'admin':
        target_id = request.POST['user-id']
        context = {"target_id": target_id}
        return render(request, 'app/main/settings_page/modifyuser.html', context)
    else:
        return 'error'

def modifyuser(request):
    if(request.method == "POST") and ('user_id' in request.session):
        target_id = request.POST['target_id']
        new_pswd = request.POST['new_pswd']
        
        if len(User.objects.filter(userId=target_id)) != 0:
            target_user = User.objects.filter(userId=target_id).first()
            target_user.pswd = new_pswd
            target_user.save()
    return HttpResponseRedirect(reverse('main-setting'))

# Browser Section




# Error