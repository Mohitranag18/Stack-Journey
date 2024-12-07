from django.contrib import admin
from .models import BlogPost

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'created_at')  # Fields to display in the list view
    search_fields = ['title', 'content']  # Fields to search in the admin panel

admin.site.register(BlogPost, BlogPostAdmin)
