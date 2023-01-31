from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import redirect
from django.views.decorators.cache import never_cache

index_file_path = './website/templates/index.html'
index_backup_file_path = './website/templates/indexBACKUP.html'

@never_cache
def create_page(request):
    username = request.COOKIES.get('username')
    if username is None:
        return redirect('create')
    return render(request, 'create.html')

@never_cache
def index(request, username):
    username = request.COOKIES.get('username')
    if username is None:
        return redirect('create')
    res = render(request, f'{username}_index.html')
    return res

@never_cache
def redirect_index(request):
    username = request.COOKIES.get('username')
    return redirect('home', username=username)

@never_cache
def edit(request, username):
    username = request.COOKIES.get('username')
    if username is None:
        return redirect('create')
    # res = render(request, f'{username}_index.html')
    user_html_path = index_file_path.replace('index', f'{username}_index')
    with open(user_html_path, 'rt') as f:
        content = f.read()
        return render(request, 'edit.html', context={'filecontent': content, 'username': username})

@never_cache
def redirect_edit(request):
    username = request.COOKIES.get('username')
    return redirect('edit', username=username)

@never_cache
@api_view(['POST'])
def content(request):
    username = request.COOKIES.get('username')
    if username is None:
        return Response(status=400)
    content = request.body.decode()
    user_html_path = index_file_path.replace('index', f'{username}_index')
    with open(user_html_path, 'wt') as f:
        f.write(content)
    return Response()

@never_cache
@api_view(['GET'])
def create_website(request):
    username = request.GET['username']
    with open(index_backup_file_path, 'rt') as f:
        user_html_path = index_file_path.replace('index', f'{username}_index')
        with open(user_html_path, 'wt') as f_write:
            f_write.write(f.read())
    response = redirect('home', username=username)
    response.set_cookie("username", username)
    return response