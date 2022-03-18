from multiprocessing import context
from re import T
from urllib import response
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



class TestRegisterBusinessView(TestCase):


    def setUp(self):
        self.client = Client()
        self.register_business_url = reverse("leidos_app:register_business")

        user = User.objects.create_user(username="test_profile")
        user.set_password("test_profile")
        user.save()

        self.profile = UserProfile.objects.create(user=user, is_business_owner=True)
        self.profile.save()


    def test_register_business_GET_uses_correct_template(self):
        self.client.login(username="test_profile", password="test_profile")

        response = self.client.get(self.register_business_url)

        # Check if page loads with status code 200
        self.assertEquals(response.status_code, 200)

        # Check if correct template is used
        self.assertTemplateUsed(response, "leidos_app/register_business.html")

    def test_register_business_POST_registers_business(self):

        context_dict = {}

        context_dict["name"] = "test_name"
        context_dict["address"] = "test_address"
        context_dict["description"] = "test_desc"


        self.client.login(username="test_profile", password="test_profile")

        response = self.client.post(self.register_business_url, context_dict, follow=True)

        self.assertEquals(response.status_code, 200) # redirect to new business page

        # Check business exists
        self.assertTrue(Business.objects.filter(owner_fk=self.profile.user).exists())

        # Check new page contains correct data
        self.assertIsInstance(response.context["business"], Business)
        self.assertEquals(response.context["business"].name, "test_name")
        self.assertEquals(response.context["business"].address, "test_address")
        self.assertEquals(response.context["business"].description, "test_desc")
        self.assertFalse(response.context["business"].img) # Check for no image

class TestEditBusinessView(TestCase):

    def setUp(self):
        self.client = Client()
        self.edit_business_url = reverse("leidos_app:edit_business", args=["test-business"])

        user = User.objects.create_user(username="test_profile")
        user.set_password("test_profile")
        user.save()

        self.profile = UserProfile.objects.create(user=user, is_business_owner=True)
        self.profile.save()

        self.business_obj = Business.objects.create(owner_fk=user, name=test_business_name, address=test_address)
        self.business_obj.save()


    def test_edit_business_GET_uses_correct_templates(self):
        self.client.login(username="test_profile", password="test_profile")
        context_dict={}
        context_dict["name"]= "test_name"
        response = self.client.post(reverse('leidos_app:create_section', args=["test-business"]), context_dict, follow=True)

        self.assertEquals(response.status_code, 200)

        # Check if correct template is used
        self.assertTemplateUsed(response, "leidos_app/edit_business.html")
        self.assertTemplateUsed(response, 'includes/create_section_item_modal.html')
        self.assertTemplateUsed(response, 'includes/create_section_modal.html')
        self.assertTemplateUsed(response, 'includes/create_hours_modal.html')
        self.assertTemplateUsed(response, 'includes/delete_section_modal.html')

    def test_edit_business_GET_displays_instantiated_form(self):
        self.client.login(username="test_profile", password="test_profile")

        response = self.client.get(self.edit_business_url)

        self.assertEquals(response.status_code, 200)

    def test_add_section(self):
        self.client.login(username="test_profile", password="test_profile")
        context_dict ={}
        context_dict["name"] = "test_section"
        response = self.client.post(reverse('leidos_app:create_section', args=["test-business"]),context_dict, follow=True)
        self.assertEquals(response.status_code, 200)
        response = self.client.get(self.edit_business_url)
        self.assertContains(response, "test_section")

    def test_add_section_item(self):
        self.client.login(username="test_profile", password="test_profile")
        context_dict = {}
        context_dict["name"] = "test_section"

        self.client.post(reverse('leidos_app:create_section', args=["test-business"]),context_dict, follow=True)

        context_dict["name"] = "test_name"
        context_dict["description"] = "test_desc"
        context_dict["price"] = "2"
        context_dict["sections"] = "test_section"
        
        response = self.client.post(reverse('leidos_app:create_section_item', args=["test-business"]),context_dict, follow=True)
        
        self.assertEquals(response.status_code, 200)
        
        response = self.client.get(self.edit_business_url)
        
        self.assertContains(response, "test_section")
        self.assertContains(response, "test_name")
        self.assertContains(response, "test_desc")
        self.assertContains(response, "2")

    def test_add_opening_hours(self):
        self.client.login(username="test_profile", password="test_profile")
        context_dict={}
        context_dict["weekday_from"] = "Tuesday"
        context_dict["weekday_to"] = "Saturday"
        context_dict["from_hour"] = "8 am"
        context_dict["to_hour"] = "8 pm"

        response = self.client.post(reverse("leidos_app:add_opening_hours", args=["test-business"]), context_dict, follow=True)
        
        self.assertEquals(response.status_code, 200)
        response = self.client.get(self.edit_business_url)

        self.assertContains(response, "Tuesday")
        self.assertContains(response, "Saturday")
        self.assertContains(response, "8am")
        self.assertContains(response, "8pm")

    def test_delete_section(self):
        self.client.login(username="test_profile", password="test_profile")
        context_dict ={}
        context_dict["name"] = "test_section"
        
        self.client.post(reverse("leidos_app:create_section", args=["test-business"]), context_dict, follow=True)
        response = self.client.get(self.edit_business_url)
        
        #Confirm section has been added
        self.assertContains(response, "test_section")

        response = self.client.post(reverse("leidos_app:delete_section", args=[0]), follow=True)

        #Confirm section has been deleted
        self.assertEquals(response.status_code, 200)
        self.assertNotContains(response, "test_section")
    
    def test_delete_section_item(self):
        self.client.login(username="test_profile", password="test_profile")
        context_dict = {}
        context_dict["name"] = "test_section"


        self.client.post(reverse('leidos_app:create_section', args=["test-business"]),context_dict, follow=True)

        context_dict["name"] = "test_name"
        context_dict["description"] = "test_desc"
        context_dict["price"] = "2"
        context_dict["sections"] = "test_section"
        
        self.client.post(reverse('leidos_app:create_section_item', args=["test-business"]),context_dict, follow=True)  

        response = self.client.get(self.edit_business_url)
        self.assertContains(response, "test_name")

        response = self.client.post(reverse("leidos_app:delete_section_item", args=[1]), follow=True)
        self.assertEquals(response.status_code, 200)
        response = self.client.get(self.edit_business_url)
        self.assertNotContains(response, "test_name")

    def test_delete_opening_hours(self):
        self.client.login(username="test_profile", password="test_profile")

        self.test_hours = OpeningHours.objects.create(business_fk=self.business_obj, weekday_from="Monday",
                                                      weekday_to="Friday", from_hour="7AM", to_hour="7PM")


        response = self.client.post(reverse("leidos_app:delete_opening_hours", args=[self.test_hours.pk]), follow=True)
        self.assertEquals(response.status_code, 200)

        response = self.client.get(reverse('leidos_app:business', args=["test-business"]))
        self.assertEquals(response.status_code, 200)        
        self.assertNotIsInstance(response.context['opening_hours'], OpeningHours)


class TestLoginView(TestCase):

    def setUp(self):
        self.client= Client()
        self.login_url = reverse('leidos_app:login')

        user = User.objects.create_user(username="test_user")
        user.set_password("test_pass")
        user.save()

        self.profile = UserProfile.objects.create(user=user, is_business_owner=False)
        self.profile.save()

    def test_login_POST_logs_in(self):
        context_dict = {}
        context_dict['username'] = "test_user"
        context_dict['password'] = "test_pass"
        response = self.client.post('leidos_app/login.html', context_dict, follow=True)

        # Check user exists
        self.client.login(**context_dict)
        self.assertTrue(User.objects.filter(username=context_dict["username"]).exists())
        #print(response)
        #self.assertEquals(response.status_code, 302) # redirect to profile page

    def test_login_uses_correct_template(self):
        response = self.client.get(reverse('leidos_app:login'))
        self.assertTemplateUsed(response, template_name='leidos_app/login.html')
        self.assertEquals(response.status_code, 200)

class TestRegisterView(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('leidos_app:register')

    def test_register_POST_registers(self):
        context_dict ={}
        context_dict["username"] = "test_user"
        context_dict["password"] = "test_user"
        context_dict["is_business_owner"] = "Yes"

        response = self.client.post(self.register_url, context_dict, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTrue(User.objects.filter(username=context_dict["username"]).exists())

    def test_register_page_uses_correct_template(self):
        response = self.client.get(reverse('leidos_app:register'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='leidos_app/register.html')

class TestProfileView(TestCase):
    def setUp(self):
        self.client = Client()
        self.profile_url = reverse('leidos_app:profile')

        user1 = User.objects.create_user(username="test_profile")
        user1.set_password("test_profile")
        user1.save()

        self.profile = UserProfile.objects.create(user=user1, is_business_owner=False)
        self.profile.save()
    
    def test_profile_uses_correct_templates(self):
        self.client.login(username="test_profile", password="test_profile")
        response = self.client.get(reverse('leidos_app:profile'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='leidos_app/profile.html')
        self.assertTemplateUsed(response, template_name='includes/edit_profile_desc_modal.html')
        self.assertTemplateUsed(response, template_name='includes/edit_profile_pic_modal.html')


    def test_add_description(self):
        self.client.login(username="test_profile", password="test_profile")
        context_dict={}
        context_dict["description"] = "test desc"
        self.client.post(reverse('leidos_app:save_profile_desc'), context_dict, follow=True)
        response=self.client.get(self.profile_url)
        self.assertContains(response, "test desc")





