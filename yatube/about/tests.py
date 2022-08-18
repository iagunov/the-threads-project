from http import HTTPStatus
from django.test import TestCase, Client
from django.urls import reverse


class StaticPagesURLTests(TestCase):
    def setUp(self):
        # Создаем неавторизованый клиент
        self.guest_client = Client()

    def test_about_url_exists_at_desired_location(self):
        """Проверка доступности адреса /author/."""
        response = self.guest_client.get('/about/author/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_tech_url_exists_at_desired_location(self):
        """Проверка доступности адреса /tech/."""
        response = self.guest_client.get('/about/tech/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_about_url_uses_correct_template(self):
        """Проверка шаблона для адреса /author/."""
        response = self.guest_client.get('/about/author/')
        self.assertTemplateUsed(response, 'about/author.html')

    def test_about_url_uses_correct_template(self):
        """Проверка шаблона для адреса /tech/."""
        response = self.guest_client.get('/about/tech/')
        self.assertTemplateUsed(response, 'about/tech.html')


class StaticViewsTestsAuthor(TestCase):
    def setUp(self):
        # Создаем неавторизованый клиент
        self.guest_client = Client()

    def test_author_page_accessible_by_name(self):
        """URL, генерируемый при помощи имени about:author, доступен."""
        response = self.guest_client.get(reverse('about:author'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_author_page_uses_correct_template(self):
        """При запросе к about:author
        применяется шаблон about/author.html."""
        response = self.guest_client.get(reverse('about:author'))
        self.assertTemplateUsed(response, 'about/author.html')

    def test_tech_page_accessible_by_name(self):
        """URL, генерируемый при помощи имени about:tech, доступен."""
        response = self.guest_client.get(reverse('about:tech'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_tech_page_uses_correct_template(self):
        """При запросе к about:tech
        применяется шаблон about/tech.html."""
        response = self.guest_client.get(reverse('about:tech'))
        self.assertTemplateUsed(response, 'about/tech.html')
