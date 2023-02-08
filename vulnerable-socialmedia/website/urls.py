from django.urls import path
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    path('', RedirectView.as_view(url='login', permanent=False), name='login'),
    path('login', views.login, name='login'),
    path('home', views.index, name='home'),
    path('create-user', views.create_user, name='create-user'),
    path('friend', views.friend_request, name='send'),
    path('logout', views.system_logout, name='logout'),
    path('search', views.search, name='search'),
    path('set-email', views.set_email, name='set-email'),
    path('set-bio', views.set_bio, name='set-bio')
]