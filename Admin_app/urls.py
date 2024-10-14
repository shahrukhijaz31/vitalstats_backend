
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path('auth_api/signup/', views.api_signup, name='api_signup'),
    path('auth_api/login/', views.api_login, name='api_login'),
    path('auth_api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), 
    path('auth_api/health-report/', views.api_health_report_view, name='health-report'),

    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='login_out'),
    path('home/', views.home, name='home'),
]