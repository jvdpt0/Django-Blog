from typing import Any
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from .models import Post
from .forms import CommentForm


# Create your views here.

class LandingPageView(ListView):
    template_name = 'blog/index.html'
    model = Post
    ordering = ['-date']
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = super().get_queryset()
        data = queryset[:3]
        return data


class AllPostsView(ListView):
    template_name = 'blog/all-posts.html'
    model = Post
    ordering = ['-date']
    context_object_name = 'posts'

class DetailedPostView(DetailView):
    template_name = 'blog/detailed-post.html'
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['tags'] = self.object.tag.all()
        return context
