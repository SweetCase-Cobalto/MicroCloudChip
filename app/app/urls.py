from django.urls import path

from . import views

urlpatterns = [

    # Login
    path(r'', views.login_page, name='login_page'),
    path(r'login', views.login, name='login'),
    path(r'login_failed', views.login_failed, name='login-failed'),
    path(r'main/logout', views.logout, name='logout'),

    # Main Page
    path(r'main/browser', views.main_browser, name='main-browser'),
    path(r'main/setting', views.main_setting, name='main-setting'),
    path(r'main/about', views.main_about, name='main-about'),

    # Setting Section
    path(r'main/setting/adduser', views.add_user_page, name='add-user'),
    path(r'main/setting/adduser-redirection', views.adduser, name='add-user-redirection')
    
]