from django.urls import path
from . import views
from .views import view_blog_post, thanks_blog_post

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_blog_post, name='create_blog_post'),
    path('edit/<int:pk>/', views.edit_blog_post, name='edit_blog_post'),
    path('delete/<int:pk>/', views.delete_blog_post, name='delete_blog_post'),
    path('post/<int:pk>/', views.view_blog_post, name='view_blog_post'),
    path('post/<int:pk>/give-thanks/', views.give_thanks, name='give_thanks'),
    path('post/<int:pk>/thanks/', thanks_blog_post, name='thanks_blog_post'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
]
