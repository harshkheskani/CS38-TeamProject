from django.test import TestCase
from django.urls import resolve
from django.urls import reverse
from leidos_app.views import *


class TestUrls(TestCase):

    def test_homepage_url_is_resolved(self):
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

    def test_business_url_is_resolved(self):
        url = reverse('leidos_app:business', args=["slug"])
        self.assertEquals(resolve(url).func, business)

    def test_add_opening_hours_url_is_resolved(self):
        url = reverse('leidos_app:add_opening_hours', args=["slug"])
        self.assertEquals(resolve(url).func, add_opening_hours)

    def test_create_section_url_is_resolved(self):
        url = reverse('leidos_app:create_section', args=["slug"])
        self.assertEquals(resolve(url).func, create_section)

    def test_create_section_item_url_is_resolved(self):
        url = reverse('leidos_app:create_section_item', args=["slug"])
        self.assertEquals(resolve(url).func, create_section_item)

    def test_register_business_url_is_resolved(self):
        url = reverse('leidos_app:register_business')
        self.assertEquals(resolve(url).func, register_business)

    def test_edit_business_url_is_resolved(self):
        url = reverse('leidos_app:edit_business', args=["slug"])
        self.assertEquals(resolve(url).func, edit_business)

