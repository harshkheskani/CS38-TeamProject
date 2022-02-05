from django.test import TestCase
from django.urls import resolve
from django.urls import reverse
from leidos_app.views import *


class TestUrls(TestCase):

    def test_index_url_is_resolved(self):
        url = reverse('homepage')
        self.assertEquals(resolve(url).func, homepage)

    def test_register_url_is_resolved(self):
        url = reverse('leidos_app:register')
        self.assertEquals(resolve(url).func, user_register)

    def test_login_url_is_resolved(self):
        url = reverse('leidos_app:login')
        self.assertEquals(resolve(url).func, user_login)

    def test_logout_url_is_resolved(self):
        url = reverse('leidos_app:logout')
        self.assertEquals(resolve(url).func, user_logout)

    def test_movie_url_is_resolved(self):
        url = reverse('leidos_app:business')
        self.assertEquals(resolve(url).func, business)
