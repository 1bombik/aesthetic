from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from django.conf import settings

urlpatterns = [
    path('register', views.user_register, name='register'),
    path('login', views.user_login, name='login'),
    path('logout/', LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout'),
    path('profile/<str:pk>/', views.user_profile, name='user-profile')
]
