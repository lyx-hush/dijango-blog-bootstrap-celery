from django.shortcuts import render, HttpResponse, redirect, reverse
from django.urls.base import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST, require_GET
from .models import BlogCategory, Blog, BlogComment
from .formers import PubblogForm
from django.http.response import JsonResponse
from django.db.models import Q


# Create your views here.
def index(request):
    blogs = Blog.objects.all()
    return render(request, template_name='index.html',context={'blogs':blogs})


def blog_detail(request, blog_id):
    try:
        blog = Blog.objects.get(pk=blog_id)
    except Exception as e:
        blog = None

    return render(request, template_name='blog_detail.html', context={'blog': blog})


@require_http_methods(['GET', 'POST'])
@login_required()
def pub_blog(request):
    if request.method == 'GET':
        categorys = BlogCategory.objects.all()
        return render(request, template_name='pub_blog.html', context={'categorys': categorys})
    else:
        form = PubblogForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            content = form.cleaned_data.get('content')
            category_id = form.cleaned_data.get('category')
            blog = Blog.objects.create(title=title, content=content, category_id=category_id, author=request.user)
            return JsonResponse({'code': 200, 'message': '文章添加成功', 'data': {'blog_id': blog.id}})
        else:
            return JsonResponse({'code': 400, 'message': '文章添加错误'})


@require_POST
@login_required()
def pub_comment(request):
    blog_id = request.POST.get('blog_id')
    content = request.POST.get('content')
    BlogComment.objects.create(content=content, blog_id=blog_id, author=request.user)
    return redirect(reverse('blog:blog_detail', kwargs={'blog_id': blog_id}))


@require_GET
def search(request):
    query = request.GET.get('q')
    blogs = Blog.objects.filter(Q(title__icontains=query) | Q(content__icontains=query)).all()
    return render(request, template_name='index.html', context={'blogs': blogs})
