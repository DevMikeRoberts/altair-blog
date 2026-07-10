from django.views.generic import ListView, DetailView
from posts.models import Post


class HomeView(ListView):
    model = Post
    template_name = "index.html"
    context_object_name = "posts"
    queryset = Post.objects.filter(published=True)


class PostDetailView(DetailView):
    model = Post
    template_name = "post_detail.html"
    context_object_name = "post"
    slug_field = "slug"
