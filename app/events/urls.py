from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    # API login/registration
    path('api/socials/', views.Socials.as_view(), name='socials'),
    path('api/register/', views.RegisterAPI.as_view(), name='register'),
    path('api/login/', views.LoginAPI.as_view(), name='login'),

    # API URLs
    path('api/', views.api_events, name='api_events'),
    path('api/<int:event_id>/', views.api_get_event, name='api_get_event'),

    # Token refresh
    path('api/token_refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Test APIs (I'll add some more later)
    path('api/aut/<int:event_id>/', views.api_aut_event, name='api_aut_event'),
    # path('api/', views.like_event, name='like_event'),
]
