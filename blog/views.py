from django.shortcuts import render,HttpResponseRedirect, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib import messages
from .models import Post


# Create your views here.

def home(request):
    posts = Post.objects.all()                          # to show post model data in html home page
    return render(request, 'blog/home.html', {'posts':posts})


def about(request):
    return render(request, 'blog/about.html')


def contact(request):
    return render(request, 'blog/contact.html')

def dashboard(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        return render(request, 'blog/dashboard.html', {'posts':posts})
    else:
        return HttpResponseRedirect('/login/')

from django.contrib.auth.models import User
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            return render(request, 'blog/signup.html')


        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = first_name
        user.last_name = last_name

        user.save()
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Congratulations...Successfully SignIn...!")

            return redirect('signup')  # Replace 'home' with the name of your home view

    return render(request, 'blog/signup.html')



def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Congratulations...Successfully Loginnn...!")
            return redirect('home')

        else:
            # Authentication failed
            return render(request, 'blog/login.html', {'error_message': 'Invalid login credentials'})

    return render(request, 'blog/login.html')


def user_logout(request):
    logout(request)
    return redirect('dashboard')



def add_posts(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            title = request.POST.get('title')
            desc = request.POST.get('desc')
            new_post = Post(title=title, desc=desc)
            new_post.save()
            return redirect('home')
        return render(request, 'blog/addpost.html')

    else:
            return HttpResponseRedirect('/login/')
    



def update_post(request, post_id):
    if request.user.is_authenticated:
        be_updated = Post.objects.get(id=post_id)
        if request.method == 'POST':
            title = request.POST.get('title')
            desc = request.POST.get('desc')

            
            if title:
                be_updated.title = title
            if desc:
                be_updated.desc = desc
            be_updated.save()

            return redirect('dashboard')
        else:
            data = {'title': be_updated.title, 'desc': be_updated.desc}
            return render(request, 'blog/updatepost.html', {'post': be_updated, 'data': data})

    else:
            return HttpResponseRedirect('/login/')




def delete_post(request, id):
    if request.user.is_authenticated:
            data_to_be_deleted = Post.objects.get(id=id)
            if request.method == 'POST':
                data_to_be_deleted.delete()
                return redirect('dashboard')
            return render(request, 'blog/dashboard.html', {'posts': data_to_be_deleted})
    else:
        return HttpResponseRedirect('/login/')
