from calendar import c
from multiprocessing import context
import re

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from .models import AboutUs, Category, Post
import random
import logging
from django.core.paginator import Paginator
from .forms import ContactForm, LoginForm, NewPostForm, RegisterForm
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User

# posts = [
#         {'id':1,'title':'Post 1', 'content':'Content of Post 1'},
#         {'id':2,'title':'Post 2', 'content':'Content of Post 2'},
#         {'id':3,'title':'Post 3', 'content':'Content of Post 3'},
#         {'id':4,'title':'Post 4', 'content':'Content of Post 4'},
#     ]
def index(request,):
    blog_title = "Latest Posts"
    posts = Post.objects.filter(is_published=True)
    paginator = Paginator(posts,4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'blog_title':blog_title,
        'page_obj':page_obj,
    }
    return render(request,'blog/index.html', context)
def detail(request, slug):
    # static data
#   post = next((item for item in posts if item['id'] == int(post_id)), None)
    try:
        post = Post.objects.get(slug=slug)
        related_posts = Post.objects.filter(category = post.category).exclude(slug = post.slug)
    except Post.DoesNotExist:
        raise Http404("Post Does not exist!")
    # logger = logging.getLogger("TESTING")
    # logger.debug(f'post variable is {post}')
    return render(request,'blog/detail.html',{'post': post, 'related_posts':related_posts})
def old_url_redirect(request):
    return redirect(reverse('blog:new_page_url'))
def new_url_view(request):
    return HttpResponse("This is the new url")

def contact_view(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been sent successfully!")
            return redirect('blog:contact')
    return render(request,'blog/contact.html',{'form': form})

def about_us(request):
    about_content = AboutUs.objects.first()
    if about_content:
        about_content = about_content.content
    else:
        about_content = "Content not available"
    return render(request,'blog/about.html',{'about_content':about_content})

def register(request):
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password'])
                user.save()
                messages.success(request,"Registration successful! You can now log in.")           
                return redirect('blog:login')
        else:
            form = RegisterForm()
        return render(request,'blog/register.html', {'form': form})

def login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = form.user
            if user is not None:
                auth_login(request, user)
                return redirect('blog:dashboard')
    return render(request,'blog/login.html', {'form': form})

def dashboard(request):
    blog_title = "My Posts"
    all_posts = Post.objects.filter(user=request.user)
    paginator = Paginator(all_posts, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'blog_title': blog_title,
        'page_obj': page_obj,
    }
    return render(request,'blog/dashboard.html', context)

def logout_view(request):
    logout(request)
    return redirect('blog:login')

def new_post(request):
    categories = Category.objects.all()
    form = NewPostForm()
    if request.method == 'POST':
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('blog:dashboard')

    return render(request,'blog/new_post.html', {'categories': categories, 'form': form})

def edit_post(request, post_id):
    categories = Category.objects.all()
    post = Post.objects.get(id=post_id)
    form = NewPostForm(instance=post)
    if request.method == 'POST':
        form = NewPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Post updated successfully!")
            return redirect('blog:dashboard')
    return render(request,'blog/edit_post.html', {'categories': categories, 'post': post, 'form': form})

def delete_post(request, post_id):
    post = Post.objects.get(id=post_id)
    post.delete()
    messages.success(request, "Post deleted successfully!")
    return redirect('blog:dashboard')

def publish_post(request, post_id):
    post = Post.objects.get(id=post_id)
    post.is_published = True
    post.save()
    messages.success(request, "Post published successfully!")
    return redirect('blog:dashboard')