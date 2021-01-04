from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage

import os
import json
import mimetypes
import shutil
import zipfile

from .models import User
from .engine.browser.browser_module import *

SESSION_ID = "user_id"                  # 세션-아이디 키
SESSION_CURRENT_PATH = "current_path"   # 세션-현재 경로

ABSOLUTE_ROOT = get_main_root("app/config.json")

#save_session_function
def save_session(request, user_id, user_pswd):
    request.session[SESSION_ID] = user_id
    request.session[SESSION_CURRENT_PATH] = '/'

# Create your views here.
def login_page(request):
    # 이미 한번 로그인 해서 들어간 경우
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
    try:
        user_id = request.session[SESSION_ID]
        current_path = request.session[SESSION_CURRENT_PATH]
    except Exception as e:
        # Key가 없는 경우 이는 불법으로 접근한 경우
        return HttpResponseRedirect(reverse('access-denied'))

    # 리스트 이동 알고리즘
    if request.method == "POST":
        root_buffer = current_path

        new_root = request.POST['selected-item']
        is_back = int(request.POST['isback'])
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

    # Session에 갱신
    request.session[SESSION_CURRENT_PATH] = current_path
    root = f'{ABSOLUTE_ROOT}{current_path}'
    try:
        file_list = get_list(root)
    except FileNotFoundError: # Refresh
        current_path = request.session[SESSION_CURRENT_PATH] = root_buffer
        root = f'{ABSOLUTE_ROOT}{current_path}'
        file_list = get_list(root)
    
    # 파일 크기 단위 에 따른 수치 변환
    for file_data in file_list:
        if file_data[DATA_TYPE] == CATEGORY_FILE:
            if file_data[DATA_SIZE_TYPE] == SIZE_TYPE_KB:
                file_data[DATA_SIZE] = round(file_data[DATA_SIZE]/1000, 3)
            elif file_data[DATA_SIZE_TYPE] == SIZE_TYPE_MB:
                file_data[DATA_SIZE] = round(file_data[DATA_SIZE]/(1000**2), 3)
            elif file_data[DATA_SIZE_TYPE] == SIZE_TYPE_GB:
                file_data[DATA_SIZE] = round(file_data[DATA_SIZE]/(1000**3), 3) 


    # html에 제출할 데이터
    context = {
        "type": "browser", 
        "user_id": user_id, 
        "file_list": file_list,
        "root": current_path
    }
    
    return render(request, 'app/main.html', context)

# Settings
def main_setting(request):
    try:
        user_id = request.session[SESSION_ID]
    except Exception:
        return HttpResponseRedirect(reverse('access-denied'))

    # Only Admin
    if user_id != "admin":
        return HttpResponseRedirect(reverse('access-denied'))

    # Search Setting ID
    l = User.objects.all()
    user_list = []
    for item in l:
        user_list.append(item.userId)

    context = {"type": "setting", "user_id": user_id, "user_list": user_list}
    return render(request, 'app/main.html', context)

def main_about(request):
    # 어바웃 페이지
    try:
        user_id = request.session[SESSION_ID]
    except Exception:
        return HttpResponseRedirect(reverse('access-denied'))

    context = {"type": "about", "user_id": user_id}
    return render(request, 'app/main.html', context)

# Setting Section
def add_user_page(request):
    try:
        user_id = request.session[SESSION_ID]
    except Exception:
        return HttpResponseRedirect(reverse('access-denied'))

    # Only Admin
    if user_id == 'admin':
        return render(request, 'app/main/settings_page/adduser.html')
    else:
        return HttpResponseRedirect(reverse('access-denied'))

def adduser(request):
    # Is request is post ?& have session
    if (request.method == "POST") and (SESSION_ID in request.session) and (request.session[SESSION_ID] == "admin"):
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
    else:
        return HttpResponseRedirect(reverse('access-denied'))

# Go To Modify User Page
def modify_user_page(request):
    try:
        user_id = request.session[SESSION_ID]
    except Exception:
        return HttpResponseRedirect(reverse('access-denied'))

    if user_id == 'admin':
        target_id = request.POST['user-id']
        context = {"target_id": target_id}
        return render(request, 'app/main/settings_page/modifyuser.html', context)
    else:
        return HttpResponseRedirect(reverse('access-denied'))

# Run modify user
def modifyuser(request):
    if(request.method == "POST") and (SESSION_ID in request.session) and (request.session[SESSION_ID] == "admin"):
        target_id = request.POST['target_id']
        new_pswd = request.POST['new_pswd']
        
        # change user info
        if len(User.objects.filter(userId=target_id)) != 0:
            target_user = User.objects.filter(userId=target_id).first()
            target_user.pswd = new_pswd
            target_user.save()
        return HttpResponseRedirect(reverse('main-setting'))
    else:
        return HttpResponseRedirect(reverse('access-denied'))

# Delete User
def deleteuser(request):
    if(request.method == "POST") and (SESSION_ID in request.session) and (request.session[SESSION_ID] == "admin"):
        target_id = request.POST['user-id']

        if len(User.objects.filter(userId=target_id)) != 0:
            target_user = User.objects.filter(userId=target_id).first()
            target_user.delete()
        return HttpResponseRedirect(reverse('main-setting'))
    else:
        return HttpResponseRedirect(reverse('access-denied'))

# Browser Section

# Download File
def download_file(request):
    if request.method == "GET":
        target_file = request.GET['selected-item']
        current_path = request.session[SESSION_CURRENT_PATH]
        full_root = f'{ABSOLUTE_ROOT}{current_path}{target_file}'

        if os.path.exists(full_root): 
            content_type, _ = mimetypes.guess_type(full_root)
            with open(full_root, 'rb') as f:
                response = HttpResponse(f, content_type=content_type)
                response['Content-Disposition'] = f'attachment; filename={target_file}'
            return response
        else:
            pass
    return HttpResponseRedirect(reverse('main-browser'))

# Download Multi Files
def download_multiple(request):
    if request.method == "POST":
        # Get Datas
        try:
            current_path = request.session[SESSION_CURRENT_PATH]
            user_id = request.session[SESSION_ID]
        except Exception:
            return HttpResponseRedirect(reverse('access-denied'))

        selected_directory_list = request.POST['selected-directories'].split('>')
        selected_file_list = request.POST['selected-files'].split('>')
        
        # Multiple File Algorithm
        target_zip_file = f'{user_id}-download.zip'
        get_file_archive(target_zip_file, selected_directory_list, selected_file_list, ABSOLUTE_ROOT, current_path)
    
        # Release zip file
        content_type, _ = mimetypes.guess_type(target_zip_file)
        with open(target_zip_file, 'rb') as f:
            response = HttpResponse(f, content_type=content_type)
            response['Content-Disposition'] = f'attachment; filename={target_zip_file}'

        # Zip File 제거
        os.remove(target_zip_file)
        return response

        return HttpResponseRedirect(reverse('main-browser'))
    else:
        return HttpResponseRedirect(reverse('access-denied'))


# Upload File
def upload_file(request):
    if request.method == 'POST':

        # Get Current Root
        try:
            current_path = request.session[SESSION_CURRENT_PATH]
        except Exception:
            return HttpResponseRedirect(reverse('access-denied'))

        files = request.FILES.getlist('upload-files')
        for file_data in files:
            filename = str(file_data)
            full_path = ABSOLUTE_ROOT + current_path + filename
            
            with open (full_path, 'wb') as f:
                for chunk in file_data.chunks():
                    f.write(chunk)
            
        return HttpResponseRedirect(reverse('main-browser'))
    else:
        return HttpResponseRedirect(reverse('access-denied'))


# 디렉토리 생성
def make_new_directory(request):
    if request.method == "POST":
        try:
            current_path = request.session[SESSION_CURRENT_PATH]
        except Exception:
            return HttpResponseRedirect(reverse('access-denied'))

        new_directory_name = request.POST['new-directory-name']
        full_path = ABSOLUTE_ROOT + current_path + new_directory_name

        # Search same name of file
        if os.path.isdir(full_path):
            err_msg = "directory is aleady exist!"
            context = {"error_message": err_msg, "back_url": "/microcloudchip/main/browser"}
            return render(request, 'app/err_page/incorrect_redirection.html', context)
        # ADD New Diredtory
        os.mkdir(full_path)
        return HttpResponseRedirect(reverse('main-browser'))
    else:
        return HttpResponseRedirect(reverse('access-denied'))

def delete_datas(request):
    if request.method == "POST":
        try:
            current_path = request.session[SESSION_CURRENT_PATH]
        except Exception:
            return HttpResponseRedirect(reverse('access-denied'))

        deleted_directory_list = request.POST['deleted-directories'].split('>')
        deleted_file_list = request.POST['deleted-files'].split('>')

        # Remove Directory
        for target in deleted_directory_list:
            directory_full_path = ABSOLUTE_ROOT + current_path + target
            if os.path.isdir(directory_full_path):
                shutil.rmtree(directory_full_path)
        
        # Remove File
        for target in deleted_file_list:
            file_full_path = ABSOLUTE_ROOT + current_path + target
            if os.path.isfile(file_full_path):
                os.remove(file_full_path)

        return HttpResponseRedirect(reverse('main-browser'))
    else:
        return HttpResponseRedirect(reverse('access-denied'))


# Access Denied
def access_denied(request):
    return render(request, 'app/err_page/access_denied.html')

# 404 Error

