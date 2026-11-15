import unittest

from app import create_app, db
from app.posts.models import Post


class PostTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()

        self.context = self.app.app_context()
        self.context.push()

        db.create_all()

        post = Post(
            title='Тестовий пост',
            content='Текст тестового поста.',
            category='tech'
        )

        db.session.add(post)
        db.session.commit()
        self.post_id = post.id

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.context.pop()

    # Створення поста
    def test_create_post(self):
        response = self.client.post('/post/create', data={
            'title': 'Новий пост',
            'content': 'Новий текст.',
            'enabled': 'y',
            'publish_date': '2026-11-15T12:30',
            'category': 'news'
        })

        self.assertEqual(response.status_code, 302)

        post = db.session.scalar(
            db.select(Post).where(Post.title == 'Новий пост')
        )

        self.assertIsNotNone(post)
        self.assertEqual(post.content, 'Новий текст.')
        self.assertEqual(post.author, 'Anonymous')

    # Перегляд списку
    def test_posts_list(self):
        response = self.client.get('/post')

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            'Тестовий пост',
            response.get_data(as_text=True)
        )

    # Перегляд одного поста
    def test_post_detail(self):
        response = self.client.get(f'/post/{self.post_id}')

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            'Текст тестового поста.',
            response.get_data(as_text=True)
        )

    # Редагування поста
    def test_update_post(self):
        response = self.client.post(
            f'/post/{self.post_id}/update',
            data={
                'title': 'Оновлений пост',
                'content': 'Оновлений текст.',
                'enabled': 'y',
                'publish_date': '2026-11-15T13:00',
                'category': 'other'
            }
        )

        self.assertEqual(response.status_code, 302)

        db.session.expire_all()
        post = db.session.get(Post, self.post_id)

        self.assertEqual(post.title, 'Оновлений пост')
        self.assertEqual(post.content, 'Оновлений текст.')
        self.assertEqual(post.category, 'other')

    # Видалення поста
    def test_delete_post(self):
        response = self.client.post(
            f'/post/{self.post_id}/delete'
        )

        self.assertEqual(response.status_code, 302)
        self.assertIsNone(
            db.session.get(Post, self.post_id)
        )

    # Неіснуючий пост
    def test_missing_post(self):
        response = self.client.get('/post/999')

        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()