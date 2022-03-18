from random import choices
from unicodedata import category
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.db import models

HOUR_OF_DAY_24 = [(str(i) + j,str(i) + j) for j in ["am","pm"] for i in range(1,13)]

WEEKDAYS = [
  ("Monday", "Monday"),
  ("Tuesday", "Tuesday"),
  ("Wednesday", "Wednesday"),
  ("Thursday", "Thursday"),
  ("Friday", "Friday"),
  ("Saturday", "Saturday"),
  ("Sunday", "Sunday"),
]


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to="profile_images", blank=True, default="profile_images/default.png")
    description = models.TextField(max_length=1024, blank=True, default="")

    # boolean flag for identifying business owners
    is_business_owner = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Business(models.Model):

    owner_fk = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=128)
    address = models.CharField(max_length=128)
    lat = models.FloatField(default=0.0)
    long = models.FloatField(default=0.0)
    img = models.ImageField(upload_to="business_images", blank=True)
    description = models.TextField(max_length=1024, blank=True)

    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = 'Businesses'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Business, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} owned by {self.owner_fk.username}"


class OpeningHours(models.Model):
    business_fk = models.ForeignKey(Business, on_delete=models.CASCADE)
    weekday_from = models.CharField(max_length=10, choices=WEEKDAYS, unique=False)
    weekday_to = models.CharField(max_length=10, choices=WEEKDAYS, blank=True)
    from_hour = models.CharField(max_length=5, choices=HOUR_OF_DAY_24)
    to_hour = models.CharField(max_length=5, choices=HOUR_OF_DAY_24)

class MenuSection(models.Model):

    business_fk = models.ForeignKey(Business, on_delete=models.CASCADE)

    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class SectionItem(models.Model):

    section_fk = models.ForeignKey(MenuSection, on_delete=models.CASCADE)

    name = models.CharField(max_length=128)
    description = models.TextField(max_length=128, blank=True, default="")
    price = models.FloatField()
    img = models.ImageField(upload_to="item_images", blank=True)

    def __str__(self):
        return self.name

class Comment(models.Model):

    user_fk = models.ForeignKey(User, on_delete=models.CASCADE)
    business_fk = models.ForeignKey(Business, on_delete=models.CASCADE)

    content = models.TextField(max_length=1024, blank=False)
    date_posted = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.content


class Favorite(models.Model):

    user_fk = models.ForeignKey(User, on_delete=models.CASCADE)
    business_fk = models.ForeignKey(Business, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.business_fk.name}"






