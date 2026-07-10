from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("posts.urls")),
    path("", views.HomeView.as_view(), name="home"),
    path("<slug:slug>/", views.PostDetailView.as_view(), name="post-detail"),
]
