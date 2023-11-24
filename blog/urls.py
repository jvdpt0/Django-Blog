from django.urls import path

from . import views

urlpatterns = [
    path('', views.LandingPageView.as_view(), name='index'),
    path('posts', views.AllPostsView.as_view(), name='all-posts'),
    path('posts/<slug:slug>', views.DetailedPostView.as_view(), name='post'),
    path('read-later', views.ReadLaterView.as_view(), name='read-later')
]
