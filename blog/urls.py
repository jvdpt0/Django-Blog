from django.urls import path

from . import views

urlpatterns = [
    path('', views.landing_page, name='index'),
    path('posts', views.all_posts, name='all-posts'),
    path('posts/<slug:slug>', views.post, name='post')
]
