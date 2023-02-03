from django.urls import path
from django.views.generic.base import RedirectView
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    path('', RedirectView.as_view(url='create', permanent=False), name='login'),
    path('home/<str:username>', views.index, name='home'),
    path('home/', views.redirect_index, name='redirect_index'),
    path('create/', views.create_page, name='create'),
    path('edit/<str:username>', views.edit, name='edit'),
    path('edit/', views.redirect_edit, name='redirect_edit'),
    path('api/content', views.content, name='content'),
    path('api/restore', views.restore, name='restore'),
    path('api/create-website', views.create_website, name='create-website')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)