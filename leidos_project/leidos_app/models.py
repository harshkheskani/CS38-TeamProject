from random import choices
from unicodedata import category
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to="profile_images", blank=True, default="profile_images/default.png")
    description = models.TextField(max_length=1024, default="")

    # boolean flag for identifying business owners
    is_business_owner = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Business(models.Model):

    owner_fk = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=128)
    address = models.CharField(max_length=128)
    img = models.ImageField(upload_to="business_images", blank=True)

    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = 'Businesses'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Business, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} owned by {UserProfile.objects.get(pk=self.owner_fk).username}"


class MenuSection(models.Model):

    business_fk = models.ForeignKey(Business, on_delete=models.CASCADE)

    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class SectionItem(models.Model):

    section_fk = models.ForeignKey(MenuSection, on_delete=models.CASCADE)

    #category = models.Choices(value=choices)
    name = models.CharField(max_length=128)
    description = models.TextField(max_length=128, default="")
    price = models.IntegerField()
    img = models.ImageField(upload_to="item_images", blank=True)

class Comment(models.Model):

    user_fk = models.ForeignKey(User, on_delete=models.CASCADE)
    business_fk = models.ForeignKey(Business, on_delete=models.CASCADE)

    content = models.TextField(max_length=1024, blank=False)

    def __str__(self):
        return self.content


class Favorite(models.Model):

    user_fk = models.ForeignKey(User, on_delete=models.CASCADE)
    business_fk = models.ForeignKey(Business, on_delete=models.CASCADE)

    def __str__(self):
        return f"{Business.objects.get(pk=self.business_fk).name}"






