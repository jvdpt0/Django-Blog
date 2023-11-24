from typing import Any
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView
from django.views import View

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

class DetailedPostView(View):
    def is_saved_for_later(self, request, post_id):
        saved_for_later = request.session.get('marked_posts')
        if saved_for_later is not None:
            saved_for_later = post_id in saved_for_later
        else:
            saved_for_later = False 

        return saved_for_later

    def get(self, request, slug):
        post = Post.objects.get(slug=slug)

        context = {
            'post': post,
            'tags': post.tag.all(),
            'comment_form': CommentForm(),
            'comments': post.comments.all().order_by('-id'),
            'saved_for_later': self.is_saved_for_later(request, post.id),
        }
        return render(request, 'blog/detailed-post.html', context)

    def post(self, request, slug):
        comment_form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse('post', args=[slug]))
        
        context = {
            'post': post,
            'tags': post.tag.all(),
            'comment_form': comment_form,
            'comments': post.comments.all().order_by('-id'),
            'saved_for_later': self.is_saved_for_later(request, post.id),
        }
        return render(request, 'blog/detailed-post.html', context)

class ReadLaterView(View):
    def get(self, request):
        marked_posts = request.session.get('marked_posts')

        context = {}

        if marked_posts is None or len(marked_posts) == 0:
            context['posts'] = []
            context['has_posts'] = False
        else:
            posts = Post.objects.filter(id__in=marked_posts)
            context['posts'] = posts
            context['has_posts'] = True

        return render(request, 'blog/read-later.html', context)

    def post(self, request):
        marked_posts = request.session.get('marked_posts')

        if marked_posts is None:
            marked_posts = []
        
        post_id = int(request.POST['post_id'])

        if post_id not in marked_posts:
            marked_posts.append(post_id)
        else:
            marked_posts.remove(post_id)

        request.session['marked_posts'] = marked_posts

        return HttpResponseRedirect('/')