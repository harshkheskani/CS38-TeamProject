from django.test import TestCase, Client
from django.urls import resolve
from django.urls import reverse
from leidos_app.views import *


test_address = "93 Douglas Street, Glasgow, Scotland"
test_business_name = "Test Business"

class TestBusinessView(TestCase):

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

    def test_business_GET_uses_correct_template(self):
        response = self.client.get(self.business_url)

        # Check if page loads with status code 200
        self.assertEquals(response.status_code, 200)

        # Check if correct template is used
        self.assertTemplateUsed(response, "leidos_app/business.html")

    def test_business_GET_displays_correct_data(self):

        # Create comment associated with the business
        #Comment.objects.create(movie=self.test_business, user=self.test_profile,
                               #time_posted=datetime.now(), text="Test Comment")

        # Create rating associated with the business
        #Rating.objects.create(business=self.test_business, user=self.test_profile, rating=5)

        self.client.login(username="test_profile", password="test_profile")
        response = self.client.get(self.business_url)

        # Check if page loads with status code 200
        self.assertEquals(response.status_code, 200)

        # Check if correct object is queried (instance of Business)
        self.assertIsInstance(response.context['business'], Business)
        self.assertIsInstance(response.context['opening_hours'][0], OpeningHours)
        self.assertIsInstance(response.context['sections'][0][0], MenuSection)
        self.assertIsInstance(response.context['sections'][0][1][0], SectionItem)

        # Compare each field with expected value
        self.assertEquals(response.context['business'].name, 'Test Business')
        self.assertEquals(response.context['business'].owner_fk, self.test_profile.user)
        self.assertEquals(response.context['opening_hours'][0].weekday_from, "Monday")
        self.assertEquals(response.context['opening_hours'][0].weekday_to,  "Tuesday")
        self.assertEquals(response.context['opening_hours'][0].from_hour, "1AM")
        self.assertEquals(response.context['opening_hours'][0].to_hour,   "1PM")
        self.assertEquals(len(response.context['opening_hours']), 1)
        self.assertEquals(response.context['sections'][0][0].name, "test_section")
        self.assertEquals(response.context['sections'][0][1][0].name, "test_item")
        self.assertEquals(response.context['sections'][0][1][0].price, 10)


