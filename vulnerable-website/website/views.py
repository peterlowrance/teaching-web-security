from django.shortcuts import render
from .models import User
import uuid
from django.views.generic.base import RedirectView
from django.shortcuts import redirect
from django.views.decorators.cache import never_cache


@never_cache
def login(request):
    session = request.COOKIES.get('session')
    try:
        user = User.objects.get(session=session)
        response = redirect('home')
        response['Location'] += '?username=' + user.username
        return response
    except:
        return render(request, 'login.html')

@never_cache
def create_user(request):
    username = request.GET.get('username')
    try:
        user = User.objects.get(username=username)
        token = user.session
    except:
        token = str(uuid.uuid1()).split('-')[0]
        print('Creating first time user ', username, ', session token', token)
        user = User(username=username, session=token)
        user.save()
    response = redirect('home')
    response.set_cookie("session", token)
    response['Location'] += '?username=' + username
    return response

@never_cache
def index(request):
    overwrite_username = request.GET.get('username')
    session = request.COOKIES.get('session')
    if session is None:
        print('Not logged in')
        return RedirectView.as_view(url='login', permanent=False)
    
    user = User.objects.get(session=session)
    # If session token doesn't match user, go to login page
    if session != user.session:
        return RedirectView.as_view(url='login', permanent=False)

    response = render(request, 'index.html', {'username': overwrite_username if overwrite_username else user.username, 'balance': user.balance})
    return response

@never_cache
def send(request):
    amount = int(request.GET.get('amount', 0))
    session = request.COOKIES.get('session')
    user = User.objects.get(session=session)
    user.balance -= amount
    user.save()
    response = redirect('home')
    response['Location'] += '?username=' + user.username
    return response