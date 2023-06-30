from django.shortcuts import render

# Create your views here.

def landing_page(request):
    return render(request, 'blog/index.html')

def all_posts(request):
    pass

def post(request):
    pass