from rest_framework import generics
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Post, Category, Comment
from .serializers import PostListSerializer, PostDetailSerializer, CategorySerializer, CommentSerializer


def health(request):
    return JsonResponse({"status": "ok"})


class PostListView(generics.ListAPIView):
    queryset = Post.objects.filter(published=True)
    serializer_class = PostListSerializer


class PostDetailView(generics.RetrieveAPIView):
    queryset = Post.objects.filter(published=True)
    serializer_class = PostDetailSerializer
    lookup_field = "slug"


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(
            approved=True,
            post__slug=self.kwargs["post_slug"],
        )

    def perform_create(self, serializer):
        post = get_object_or_404(Post, slug=self.kwargs["post_slug"])
        serializer.save(post=post)
