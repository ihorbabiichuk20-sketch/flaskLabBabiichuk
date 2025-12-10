import unittest
from app import create_app
from app.extensions import db
from app.posts.models import Post

class PostsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_create_post_get(self):
        response = self.client.get("/post/create")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Create a New Post", response.data)

    def test_create_post_post(self):
        response = self.client.post(
            "/post/create",
            data={
                "title": "Test post",
                "content": "Some content",
                "is_active": "y",
                "publish_date": "2025-12-10T10:00",
                "category": "news",
                "submit": "Save",
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Post added successfully", response.data)
        self.assertEqual(db.session.scalar(db.select(Post).count()), 1)

    def test_list_posts(self):
        post = Post(title="P1", content="C1")
        db.session.add(post)
        db.session.commit()
        response = self.client.get("/post/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"P1", response.data)

    def test_detail_post_404(self):
        response = self.client.get("/post/9999")
        self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    unittest.main()
