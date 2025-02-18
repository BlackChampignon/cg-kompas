from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('api/register/', views.RegisterAPI.as_view(), name='register'),
    path('api/login/', views.LoginAPI.as_view(), name='login'),

    # Actions with user table
    path('api/change_username/', views.change_username, name='change_username'),

    # API URLs
    path('api/', views.api_events, name='api_events'),
    path('api/<int:event_id>/', views.api_get_event, name='api_get_event'),
    path('api/user/', views.user_profile, name='user_profile'),
    path('api/like/', views.like, name='toggle_like'),

    # Token refresh
    path('api/token_refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
