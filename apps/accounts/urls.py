from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'


urlpatterns = [
    # path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('change-password/', views.change_password, name='change_password')
    
    # path('edit-profile/', views.edit_profile, name='edit_profile'),
]