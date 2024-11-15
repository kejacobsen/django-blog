from django.templatetags.tz import utc
from django.test import TestCase
from django.urls import reverse

from django.contrib.auth.models import User
from django.utils import timezone
import datetime


from blogging.models import Post, Category

class PostTestCase(TestCase):
    fixtures = ['blogging_test_fixture.json']

    def setUp(self):
        self.user = User.objects.get(pk=1)

    def test_string_representation(self):
        expected = "This is a blog title"
        p1 = Post(title=expected)
        actual = str(p1)
        self.assertEqual(actual, expected)

class CategoryTestCase(TestCase):

    def test_string_representation(self):
        expected = "A Category"
        category1 = Category(name=expected)
        actual = str(category1)
        self.assertEqual(actual, expected)

class FrontEndTestCase(TestCase):
    fixtures = ['blogging_test_fixture.json']

    def setUp(self):
        self.now = timezone.now()
        self.timedelta = datetime.timedelta(15)
        author = User.objects.get(pk=1)
        print(f"Author retrieved: {author}")
        for count in range(1, 11):
            post = Post(title=f"Post {count} Title", text="foo", author=author)
            if count < 6:
                pubdate = self.now - self.timedelta * count
                post.published_date = pubdate
            post.save()

    def test_list_only_published(self):
        resp = self.client.get("/blogging/")
        resp_text = resp.content.decode(resp.charset)
        self.assertTrue("Recent Posts" in resp_text)
        for count in range(1, 11):
            title = f"Post {count} Title"
            if count < 6:
                self.assertContains(resp, title, count=1)
            else:
                self.assertNotContains(resp, title)

    def test_details_only_published(self):
        for count in range(1, 11):
            title = f"Post {count} Title"
            post = Post.objects.get(title=title)
            response = self.client.get(f'/blogging/posts/%d/' % post.pk)
            if count < 6:
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, title)
            else:
                self.assertEqual(response.status_code, 404)
