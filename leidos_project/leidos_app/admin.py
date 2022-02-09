from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import UserProfile, Business, OpeningHours, MenuSection, SectionItem, Comment, Favorite

admin.site.register(UserProfile)
admin.site.register(Business)
admin.site.register(OpeningHours)
admin.site.register(MenuSection)
admin.site.register(SectionItem)
admin.site.register(Comment)
admin.site.register(Favorite)