from django.shortcuts import render
from .models import User
import uuid
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

def index(request):
    overwrite_username = request.GET.get('username')
    session = request.COOKIES.get('session')
    if session is None:
        print('Not logged in')
        return redirect('login')
    try:
        user = User.objects.get(session=session)
    except:
        return redirect('login')
    # If session token doesn't match user, go to login page
    if session != user.session:
        return redirect('login')

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

@never_cache
def fake_search(request):
    search_term = request.GET.get('term')
    return render(request, 'search.html', context={'content': search_term})