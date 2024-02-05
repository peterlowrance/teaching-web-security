from django.shortcuts import render
from .models import User
import uuid
from django.shortcuts import redirect
from django.views.decorators.cache import never_cache
import threading
from django.contrib.auth import logout
import json
from urllib.parse import parse_qs
import re

FLAG_1 = "CSRF_IS_EZ"
FLAG_2 = "BIO_HACKING"
FLAG_3 = "XSS_IS_EVEN_EZR"
FLAG_4 = "EMAIL_PROBLEM"
FLAG_5 = "WORM_WORLD"

# The final XSS solution has a race condition this fixes
my_mutex = threading.Lock()
@never_cache
def login(request):
    session = request.COOKIES.get('session')
    try:
        user = User.objects.get(session=session)
        response = redirect('home')
        response['Location'] += '?username=' + user.username
        response.set_cookie('session', user.session)
        return response
    except:
        return render(request, 'login.html')

@never_cache
def system_logout(request):
    logout(request)
    response = render(request, 'login.html')
    response.delete_cookie('session')
    return response

@never_cache
def create_user(request):
    username = request.GET.get('username')
    try:
        user = User.objects.get(username=username)
        token = user.session
    except User.DoesNotExist:
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
        return redirect('login')
    try:
        user = User.objects.get(session=session)
    except:
        return redirect('login')
    # If session token doesn't match user, go to login page
    if session != user.session:
        return redirect('login')

    flag_1 = FLAG_1 if user.friends.filter(username=user.username).exists() else ""
    flag_2 = FLAG_2 if user.bio == "give me the flag" else ""
    flag_3 = FLAG_3 if user.has_xss_flag_1 else ""
    flag_4 = FLAG_4 if user.email == 'I think I have been hacked' else ""
    response = render(request, 'index.html', { 'flag1': flag_1, "flag2": flag_2, "flag3": flag_3, 'flag4': flag_4, 'email': user.email, 'bio': user.bio, 'username': overwrite_username if overwrite_username else user.username, 'friends': [user.username for user in user.friends.all()] if len(user.friends.all()) > 0 else ""})
    return response

@never_cache
def friend_request(request):
    with my_mutex:
        friend = request.GET.get('name')
        session = request.COOKIES.get('session')
        user = User.objects.get(session=session)
        # TODO: They can just type this in the address bar, no idea how to fix
        if friend == "":
            return redirect('home')

        friend_user = User.objects.filter(username=friend)
        if not friend_user.exists():
            token = str(uuid.uuid1()).split('-')[0]
            friend_user = User(username=friend, session=token)
            friend_user.save()
        else:
            friend_user = friend_user.all()[0]
        if user.friends.filter(username=friend).exists():
            user.friends.remove(friend_user)
        else:
            user.friends.add(friend_user)
        user.save()
        friend_user.save()
        response = redirect('home')
        response['Location'] += '?username=' + user.username
    return response

@never_cache
def set_bio(request):
    with my_mutex:
        session = request.COOKIES.get('session')
        user = User.objects.get(session=session)
        bio = parse_qs(request.body.decode())
        if bio != {}:
            bio_text = bio['bio'][0]
            # TODO: change the text you need to put in to <script></script>? Why hardcoding http_referer check?
            if bio_text == 'give me the flag' and 'HTTP_REFERER' in request.META:
                return render(request, 'try_again.html')
            user.bio = bio_text
            user.save()
    return redirect('home')

@never_cache
def set_email(request):
    session = request.COOKIES.get('session')
    user = User.objects.get(session=session)
    email = parse_qs(request.body.decode())
    if email != {}:
        email_text = email['email'][0]
        if email_text == 'I think I have been hacked' and 'HTTP_X_REQUESTED_WITH' not in request.META:
            return render(request, 'try_again.html')
        user.email = email_text
        user.save()
    return redirect('home')

@never_cache
def search(request):
    session = request.COOKIES.get('session')
    user = User.objects.get(session=session)
    search_term = request.GET.get('term')
    regex = "^<script[\s\S]*?>alert\([\"\']your flag is mine![\"\']\);?<\/script[\s\S]*?>$"
    result = re.findall(regex, search_term)
    if len(result) > 0:
        user.has_xss_flag_1 = True
        user.save()

    searched_for_users = User.objects.filter(username=search_term)
    if searched_for_users.exists():
        user_to_send = searched_for_users.all()[0]
        response = render(
            request,
            'search_found.html',
            {
                'email': user_to_send.email,
                'bio': user_to_send.bio,
                'username': user_to_send.username,
                'friends': [user.username for user in user_to_send.friends.all()] if len(user_to_send.friends.all()) > 0 else ""
            }
        )
        return response
    return render(request, 'search.html', context={'content': search_term})