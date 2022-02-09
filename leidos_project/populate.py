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

    businesses = [{'owner': 'ben', 'name':'Bobs Burgers', 'address': 'University Avenue, G12 8QW', 'img': 'media/business_images/business_default.png', 
              }]

    menuSections = [{'business': 'Bobs Burgers', 'name': 'Mains'},
                    {'business': 'Bobs Burgers', 'name': 'Sides'},
                    {'business': 'Bobs Burgers', 'name': 'Drinks'}]

    sectionItems = [{'business': 'Bobs Burgers', 'section': 'Mains', 'name': 'Cheeseburger', 
                        'description': 'food', 'price': '5', 'img': 'media/item_images/defaultfood.png'},
                    {'business': 'Bobs Burgers', 'section': 'Mains', 'name': 'Pizza', 
                        'description': 'food', 'price': '6', 'img': 'media/item_images/defaultfood.png'},
                    {'business': 'Bobs Burgers', 'section': 'Drinks', 'name': 'Coke', 
                        'description': 'food', 'price': '2', 'img': 'media/item_images/defaultfood.png'},
                    {'business': 'Bobs Burgers', 'section': 'Drinks', 'name': 'Fanta', 
                        'description': 'food', 'price': '2', 'img': 'media/item_images/defaultfood.png'},
                    {'business': 'Bobs Burgers', 'section': 'Sides', 'name': 'Fries', 
                        'description': 'food', 'price': '3', 'img': 'media/item_images/defaultfood.png'}]

    for u in users:
        add_user(u['username'], u['firstname'], u['lastname'], u['password'], u['profile_pic'], u['description'], u['is_business_owner'])

    for b in businesses:
        add_business(b['owner'], b['name'], b['address'], b['img'])

    for s in menuSections:
        add_menuSection(s['business'], s['name'])

    for i in sectionItems:
        add_sectionItem(i['business'], i['section'], i['name'], i['description'], i['price'], i['img'])


def add_user(username, firstname, lastname, password, profile_pic, description, is_business_owner):
    new_user = User.objects.get_or_create(username=username, password=password, first_name=firstname, last_name=lastname)
    if new_user[1]:
        new_profile = UserProfile(user=User.objects.get(username=username))
        new_profile.profile_pic = profile_pic
        new_profile.description = description
        new_profile.is_business_owner = is_business_owner
        new_profile.save()

def add_business(owner, name, address, img):
    new_business = Business(name=name, owner_fk=User.objects.get(username=owner))
    new_business.address = address
    new_business.img = img
    new_business.save()

def add_menuSection(business, name):
    new_section = MenuSection(business_fk=Business.objects.get(name=business))
    new_section.name = name
    new_section.save()

def add_sectionItem(business, section, name, description, price, img):
    new_item = SectionItem(section_fk=MenuSection.objects.get(name=section))
    new_item.name = name
    new_item.description = description
    new_item.price = price
    new_item.img = img
    new_item.save()


if __name__ == '__main__':
    print('Starting Population Script ...')
    populate()
    print('All OK')
