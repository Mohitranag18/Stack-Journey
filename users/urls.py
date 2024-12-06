from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/confirm/', views.logout_confirm, name='logout_confirm'),  # Logout confirmation
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),  # Actual logout
]
