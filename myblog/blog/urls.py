

from django.urls import path, include
from . import views
from .feeds import LatestPostsFeed
from django.contrib.auth import views as auth_views
app_name = 'blog'
urlpatterns = [
 #    path('', views.post_list, name='post_list'),
    path('', views.PostListView.as_view(), name='post_list'),
    path('email/', views.email_message, name='email'),
    path('<int:year>/<int:month>/<str:title>/<slug:post>/', views.post_detail, name='post_detail'),
    path('feed/', LatestPostsFeed(), name='post_feed'),
    path('1', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),

]