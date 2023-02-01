from django.urls import path
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    path('', RedirectView.as_view(url='login', permanent=False), name='login'),
    path('login', views.login, name='login'),
    path('home', views.index, name='home'),
    path('create-user', views.create_user, name='create-user'),
    path('send', views.send, name='send')
]