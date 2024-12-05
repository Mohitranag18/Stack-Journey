from django.shortcuts import render, redirect, get_object_or_404
from .models import BlogPost
from .forms import BlogPostForm
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'blogs/home.html')

@login_required
def create_blog_post(request):
    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.author = request.user #set the current user as authour
            blog_post.save()
            return redirect('home')
    else:
        form = BlogPostForm()
    return render(request, 'blogs/create_blog_post.html',{'form': form})

@login_required
def edit_blog__post(request, pk):
    blog_post = get_object_or_404(BlogPost, pk=pk)

    if request.user != blog_post.author:
        return redirect('home')
    
    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES, instance=blog_post)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = BlogPostForm(instance=blog_post)
    return render(request, 'blogs/edit_blog_post.html', {'form': form})

@login_required
def delete_blog_post(request, pk):
    blog_post = get_object_or_404(BlogPost, pk=pk)

    if request.user != blog_post.author:
        return redirect('home')
    
    if request.method == "POST":
        blog_post.delete()
        return redirect('home')
    return render(request, 'blogs/confirm_delete.html', {'blog_post': blog_post})