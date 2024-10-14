
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views, api_views

urlpatterns = [
    # mobile Api
    path('vitalstats_api/signup/', api_views.api_signup, name='api_signup'),
    path('vitalstats_api/login/', api_views.api_login, name='api_login'),
    path('vitalstats_api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), 
    path('vitalstats_api/get_health_report/', api_views.api_health_report_get, name='health_report_get'),
    path('vitalstats_api/post_health_report/', api_views.api_health_report_post, name='health_report_post'),

    # web Api
    path('', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='login_out'),
    path('home/', views.home, name='home'),
]