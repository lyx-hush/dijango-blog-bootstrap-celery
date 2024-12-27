from django.contrib import admin
from .models import BlogCategory, Blog, BlogComment


# Register your models here.
@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'content', 'pub_time', 'category']


@admin.register(BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ['content', 'blog', 'pub_time', 'author']
