import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'leidos_project.settings')

import django
django.setup()
from django.contrib.auth.models import User
from leidos_app.models import UserProfile, Business, MenuSection, SectionItem

def populate():
    users = [{'username': 'ben', 'firstname': 'ben',
              'lastname': 'bennison', 'password': '1234', 'profile_pic': 'media/profile_images/default.png', 
              'description': 'ahahahaaha', 'is_business_owner': 'True'}]

    businesses = [{'name': 'ben', 'address': 'ben', 'img': 'media/profile_images/default.png', 
              'description': 'ahahahaaha', 'is_business_owner': 'True'}]

    menuSections = [{}]


def add_user():


def add_business():


def add_menuSection():


def add_sectionItem():