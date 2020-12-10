from django.urls import path

from . import views

urlpatterns = [
    path(r'', views.login_page, name='login_page'),
    path(r'login', views.login, name='login'),
    path(r'main/browser', views.main_browser, name='main-browser'),
    path(r'main/setting', views.main_setting, name='main-setting')
]