from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from .models import Post
import random
import logging
from django.core.paginator import Paginator
from .forms import ContactForm
# posts = [
#         {'id':1,'title':'Post 1', 'content':'Content of Post 1'},
#         {'id':2,'title':'Post 2', 'content':'Content of Post 2'},
#         {'id':3,'title':'Post 3', 'content':'Content of Post 3'},
#         {'id':4,'title':'Post 4', 'content':'Content of Post 4'},
#     ]
def index(request,):
    blog_title = "Latest Posts"
    posts = Post.objects.all()
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
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            logger = logging.getLogger("TESTING")
            logger.debug(f'post Data is {form.cleaned_data['name']} {form.cleaned_data['email']} {form.cleaned_data['message']}')
    return render(request,'blog/contact.html')