from django.test import TestCase, Client
from django.urls import resolve
from django.urls import reverse
from leidos_app.views import *


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