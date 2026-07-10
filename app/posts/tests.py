from django.test import TestCase
from django.utils.text import slugify
from rest_framework.test import APIClient
from .models import Post, Category, Comment


class PostModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Tech")
        self.post = Post.objects.create(
            title="Test Post",
            content="Content here",
            excerpt="Excerpt",
            category=self.category,
            published=True,
        )

    def test_post_auto_slug(self):
        self.assertEqual(self.post.slug, slugify("Test Post"))

    def test_post_str(self):
        self.assertEqual(str(self.post), "Test Post")

    def test_published_ordering(self):
        post2 = Post.objects.create(
            title="Older Post",
            content="Older",
            published=True,
        )
        posts = Post.objects.filter(published=True)
        self.assertEqual(posts.first(), self.post)

    def test_category_str(self):
        self.assertEqual(str(self.category), "Tech")

    def test_category_auto_slug(self):
        self.assertEqual(self.category.slug, "tech")


class CommentModelTest(TestCase):
    def setUp(self):
        self.post = Post.objects.create(title="Post", content="Content", published=True)
        self.comment = Comment.objects.create(
            post=self.post,
            author_name="Alice",
            author_email="alice@example.com",
            content="Great post!",
        )

    def test_comment_default_not_approved(self):
        self.assertFalse(self.comment.approved)

    def test_comment_str(self):
        self.assertIn("Alice", str(self.comment))
        self.assertIn("Post", str(self.comment))


class PostAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(name="Tech", slug="tech")
        self.post = Post.objects.create(
            title="API Test",
            content="Testing API",
            category=self.category,
            published=True,
        )

    def test_list_posts(self):
        resp = self.client.get("/api/posts/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.data["results"]), 1)

    def test_post_detail_by_slug(self):
        resp = self.client.get(f"/api/posts/{self.post.slug}/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data["title"], "API Test")

    def test_unpublished_post_hidden(self):
        Post.objects.create(title="Draft", content="Draft", published=False)
        resp = self.client.get("/api/posts/")
        self.assertEqual(len(resp.data["results"]), 1)

    def test_list_categories(self):
        resp = self.client.get("/api/categories/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.data), 1)

    def test_create_comment(self):
        resp = self.client.post(
            f"/api/posts/{self.post.slug}/comments/",
            {"author_name": "Bob", "content": "Nice!"},
            format="json",
        )
        self.assertEqual(resp.status_code, 201)

    def test_health_endpoint(self):
        resp = self.client.get("/api/health/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), {"status": "ok"})
