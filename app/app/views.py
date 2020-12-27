from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

import os
import json

from .models import User
from .engine.browser.browser_module import *

SESSION_ID = "user_id"
SESSION_CURRENT_PATH = "current_path"

ABSOLUTE_ROOT = get_main_root("app/config.json")

#save_session_function
def save_session(request, user_id, user_pswd):
    request.session[SESSION_ID] = user_id
    request.session[SESSION_CURRENT_PATH] = '/'

# Create your views here.
def login_page(request):
    # 이미 한번 로그인 해서 쳐 들어간 경우
    if SESSION_ID in request.session:
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
    if SESSION_ID in request.session:
        request.session.clear()
    return HttpResponseRedirect(reverse('login_page'))

# In Main Section
def main_browser(request):
    # get id from session
    user_id = request.session[SESSION_ID]
    current_path = request.session[SESSION_CURRENT_PATH]

    # New List
    if request.method == "POST":
        new_root = request.POST['selected-item']
        is_back = int(request.POST['isback'])

        print(is_back)
        
        if is_back == 0:
            current_path = current_path + new_root + '/'
        elif is_back == 1:
            path_tokens = current_path.split('/')
            # is not super root
            if len(path_tokens) > 2:
                del path_tokens[-2]
                
                # is super root after remove path
                if len(path_tokens) == 2:
                    current_path = "/"
                else:
                    current_path = "/"
                    for path in path_tokens:
                        if path != '':
                            current_path += path
                            current_path += "/"

    # get list
    print(current_path)
    request.session[SESSION_CURRENT_PATH] = current_path
    root = f'{ABSOLUTE_ROOT}/{current_path}'
    file_list = get_list(root)

    for file_data in file_list:
        if file_data[DATA_TYPE] == CATEGORY_FILE:
            if file_data[DATA_SIZE_TYPE] == SIZE_TYPE_KB:
                file_data[DATA_SIZE] = round(file_data[DATA_SIZE]/1000, 3)
            elif file_data[DATA_SIZE_TYPE] == SIZE_TYPE_MB:
                file_data[DATA_SIZE] = round(file_data[DATA_SIZE]/(1000**2), 3)
            elif file_data[DATA_SIZE_TYPE] == SIZE_TYPE_GB:
                file_data[DATA_SIZE] = round(file_data[DATA_SIZE]/(1000**3), 3) 
    context = {
        "type": "browser", 
        "user_id": user_id, 
        "file_list": file_list,
        "root": current_path
    }
    
    return render(request, 'app/main.html', context)

def main_setting(request):
    user_id = request.session[SESSION_ID]

    # Only admin

    # Search Setting ID
    l = User.objects.all()
    user_list = []
    for item in l:
        user_list.append(item.userId)

    context = {"type": "setting", "user_id": user_id, "user_list": user_list}
    return render(request, 'app/main.html', context)

def main_about(request):
    user_id = request.session[SESSION_ID]
    context = {"type": "about", "user_id": user_id}
    return render(request, 'app/main.html', context)

# Setting Section
def add_user_page(request):
    user_id = request.session[SESSION_ID]
    if user_id == 'admin':
        return render(request, 'app/main/settings_page/adduser.html')
    else:
        return 'error'

def adduser(request):
    # Is request is post ?& have session
    if (request.method == "POST") and (SESSION_ID in request.session):
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
    user_id = request.session[SESSION_ID]
    if user_id == 'admin':
        target_id = request.POST['user-id']
        context = {"target_id": target_id}
        return render(request, 'app/main/settings_page/modifyuser.html', context)
    else:
        return 'error'

def modifyuser(request):
    if(request.method == "POST") and (SESSION_ID in request.session):
        target_id = request.POST['target_id']
        new_pswd = request.POST['new_pswd']
        
        if len(User.objects.filter(userId=target_id)) != 0:
            target_user = User.objects.filter(userId=target_id).first()
            target_user.pswd = new_pswd
            target_user.save()
    return HttpResponseRedirect(reverse('main-setting'))

def deleteuser(request):
    if(request.method == "POST") and (SESSION_ID in request.session):
        target_id = request.POST['user-id']

        if len(User.objects.filter(userId=target_id)) != 0:
            target_user = User.objects.filter(userId=target_id).first()
            target_user.delete()
    return HttpResponseRedirect(reverse('main-setting'))

# Browser Section

# Error