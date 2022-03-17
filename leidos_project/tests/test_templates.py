from urllib import response
from django.test import TestCase, Client
from django.urls import resolve
from django.urls import reverse
from leidos_app.views import *
from leidos_app.forms import *


test_address = "93 Douglas Street, Glasgow, Scotland"
test_business_name = "Test Business"

class TestBusinessTemplate(TestCase):

    def setUp(self):
        self.client = Client()
        self.business_url = reverse("leidos_app:business", args=["test-business"])

        user = User.objects.create_user(username="test_profile")
        user.set_password("test_profile")
        user.save()

        self.test_profile = UserProfile.objects.create(user=user)

        self.test_business = Business.objects.create(name=test_business_name, owner_fk=self.test_profile.user,
                                                     address=test_address)

        self.test_hours = OpeningHours.objects.create(business_fk=self.test_business, weekday_from="Monday",
                                                      weekday_to="Tuesday", from_hour="1AM", to_hour="1PM")

        self.menu_section = MenuSection.objects.create(business_fk=self.test_business,name="test_section")

        self.section_item = SectionItem.objects.create(section_fk=self.menu_section,name="test_item", price=10)


    def test_business_template_displays_correct_data(self):

        self.client.login(username="test_profile", password="test_profile")
        response = self.client.get(self.business_url)

        # Check if page loads with status code 200
        self.assertEquals(response.status_code, 200)

        # Check template contains correct data
        self.assertContains(response, "Test Business")                          # Business Name
        self.assertContains(response, "93 Douglas Street, Glasgow, Scotland")   # Business Address
        self.assertContains(response, "Monday")                                 # Weekday_from
        self.assertContains(response, "Tuesday")                                # Weekday_to
        self.assertContains(response, "1AM")                                    # From_hour
        self.assertContains(response, "1PM")                                    # To_hour
        self.assertContains(response, "test_section")                           # Section Name
        self.assertContains(response, "test_item")                              # Item Name
        self.assertContains(response, 10)                                       # Item Price

class TestRegisterBusinessTemplate(TestCase):

    def setUp(self):
        self.client = Client()
        self.register_business_url = reverse("leidos_app:register_business")

        user1 = User.objects.create_user(username="test_profile_1")
        user1.set_password("test_profile")
        user1.save()

        user2 = User.objects.create_user(username="test_profile_2")
        user2.set_password("test_profile")
        user2.save()

        self.business_owner = UserProfile.objects.create(user=user1, is_business_owner=True)
        self.non_business_owner = UserProfile.objects.create(user=user2, is_business_owner=False)


    def test_register_business_template_displays_correct_data(self):

        # Login business owner client
        self.client.login(username="test_profile_1", password="test_profile")
        response1 = self.client.get(self.register_business_url)

        # Check if page loads with status code 200
        self.assertEquals(response1.status_code, 200)

        # Check response1 for correctness
        self.assertContains(response1, "Name")
        self.assertContains(response1, "Address")
        self.assertContains(response1, "Description")
        self.assertNotContains(response1, "Owner_fk")
        self.assertNotContains(response1, "Slug")

        self.client.logout() # Logout business owning client

        # Login non-business owner client
        self.client.login(username="test_profile_2", password="test_profile")
        response2 = self.client.get(self.register_business_url)

        # Check if page loads with status code 302 (redirect)
        self.assertEquals(response2.status_code, 302)

        # Check response2 for correctness
        self.assertRedirects(response2, "/leidos_app/") # Non-business owner should be redirected to homepage

        # TODO figure out how to check for redirected content

class TestRegisterTemplate(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse("leidos_app:register")

    def test_register_template_displays_form(self):
        response = self.client.get(self.register_url)

        self.assertEquals(response.status_code, 200)

        self.assertContains(response, "username")
        self.assertContains(response, "password")
        self.assertContains(response, "is_business_owner")
        self.assertContains(response, "profile_pic")


class TestLoginTemplate(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse("leidos_app:login")

    def test_login_template_displays_form(self):
        response = self.client.get(self.login_url)

        self.assertEquals(response.status_code, 200)

        self.assertContains(response, "username")
        self.assertContains(response, "password")


class TestEditBusinessTemplate(TestCase):
    def setUp(self):
        self.client = Client()
        self.edit_business_url = reverse("leidos_app:edit_business", args=["test-business"])

        user = User.objects.create_user(username="test_profile")
        user.set_password("test_profile")
        user.save()

        self.test_profile = UserProfile.objects.create(user=user, is_business_owner=True)
        self.test_business = Business.objects.create(name=test_business_name, owner_fk=self.test_profile.user,
                                                     address=test_address)

        self.menu_section = MenuSection.objects.create(business_fk=self.test_business,name="test_section")

    def test_edit_opening_hours_form_displays(self):
        self.client.login(username="test_profile", password="test_profile")

        response = self.client.get(self.edit_business_url)

        self.assertEquals(response.status_code, 200)

        self.assertContains(response, "weekday_from")
        self.assertContains(response, "weekday_to")
        self.assertContains(response, "from_hour")
        self.assertContains(response, "to_hour")
    
    def test_create_section_form_displays(self):
        self.client.login(username="test_profile", password="test_profile")

        response = self.client.get(self.edit_business_url)

        self.assertEquals(response.status_code, 200)

        self.assertContains(response, "name")
    
    def test_add_item_form_displays(self):
        self.client.login(username="test_profile", password="test_profile")

        response =  self.client.get(self.edit_business_url)

        self.assertEquals(response.status_code, 200)

        self.assertContains(response, "name")
        self.assertContains(response, "description")
        self.assertContains(response, "img")
        self.assertContains(response, "price")




