from django.urls import path

from . import views

urlpatterns = [
    path(r'', views.login_page, name='login_page'),
    path(r'login', views.login, name='login'),
    path(r'main', views.main, name='main')
]