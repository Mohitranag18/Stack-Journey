from django.shortcuts import render, redirect, get_object_or_404
from .models import BlogPost, Thanks
from .forms import BlogPostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def give_thanks(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)

    if request.user.is_authenticated:
        # Check if the user has already given thanks to this post
        if not Thanks.objects.filter(user=request.user, blog_post=post).exists():
            # If not, create a new thanks entry
            Thanks.objects.create(user=request.user, blog_post=post)
        else:
            # If already thanked, do nothing or show a message (optional)
            print("User has already thanked this post")
        return redirect('view_blog_post', post_id=post.id)
    else:
        # Redirect to login if the user is not authenticated
        return redirect('login')

def thanks_blog_post(request, pk):
    # Get the specific blog post by primary key (pk)
    post = get_object_or_404(BlogPost, pk=pk)

    # Ensure the user is authenticated before they can give thanks
    if request.user.is_authenticated:
        # Check if the user has already given thanks to this post
        if not Thanks.objects.filter(blog_post=post, user=request.user).exists():
            # If not, create a new Thanks entry
            Thanks.objects.create(blog_post=post, user=request.user)
    
    # Redirect the user back to the blog post page after giving thanks
    return redirect('view_blog_post', pk=post.pk)


@login_required
def user_profile(request, username):
    # Get the user object based on the username
    user = get_object_or_404(User, username=username)
    
    # Get all blog posts by this user
    user_posts = BlogPost.objects.filter(author=user)
    
    # Calculate the total thanks for the user's blog posts
    total_thanks = 0
    for post in user_posts:
        total_thanks += post.thanks_set.count()  # Sum the thanks for each post
    
    # Render the profile page with the user and total thanks
    return render(request, 'blogs/profile.html', {'user': user, 'total_thanks': total_thanks, 'user_posts': user_posts})


def home(request):
    category = request.GET.get('category', 'all')  # Default to 'all' if no category is selected

    if category == 'all':
        blog_posts = BlogPost.objects.all().order_by('-created_at')
    else:
        blog_posts = BlogPost.objects.filter(category=category).order_by('-created_at')

    return render(request, 'blogs/home.html', {'blog_posts': blog_posts, 'category': category})


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
def edit_blog_post(request, pk):
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

def view_blog_post(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    
    # Check if the user has already given thanks to the post
    has_thanks = Thanks.objects.filter(blog_post=post, user=request.user).exists() if request.user.is_authenticated else False

    return render(request, 'blogs/view_blog_post.html', {
        'post': post,
        'has_thanks': has_thanks
    })

