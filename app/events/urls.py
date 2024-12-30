from django.urls import path
from . import views

urlpatterns = [
    # User URLs
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('delete_account/', views.delete_account, name='delete_account'),

    # Event URLs
    path('', views.list_events, name='list_events'),  # Homepage shows all events
    path('event/add/', views.add_event, name='add_event'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('event/<int:event_id>/delete/', views.delete_event, name='delete_event'),

    # Comment URLs
    path('event/<int:event_id>/add_comment/', views.add_comment, name='add_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),

    # Category URLs
    path('categories/', views.category_list, name='category_list'),
    path('category/add/', views.add_category, name='add_category'),
    path('category/<int:category_id>/modify/', views.modify_category, name='modify_category'),
    path('category/<int:category_id>/delete/', views.delete_category, name='delete_category'),

    # Like URLs
    path('event/<int:event_id>/like/', views.like_event, name='like_event'),

    # API URLs
    path('api/', views.api_events, name='api_events'),
    path('api/<int:event_id>/', views.api_get_event, name='api_get_event'),

    # Test APIs (I'll add some more later)
    path('api/', views.like_event, name='like_event'),
]
