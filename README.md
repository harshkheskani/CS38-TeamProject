---
author:
- Team CS38
date: March 2022
title: Roll Vans Documentation
---

# Introduction

This paper presents brief documentation on existing bugs (as of March
2022) as well as guide on how to use existing features.

# Bugs And Quirks

As of now, there are no known bugs present in the web application.
However, there are few quirks that should be noted especially for user
presentation.

## Quirks

Firsts thing to notice it that when registering business, auto fill
function is used to fill address field of business. This function also
fills invisible fields of latitude and longitude. Therefore, care should
be taken that this auto fill is used and that address is not just typed
in. This also applies to address field in Edit Business page.\
Second thing to notice is saving of different edits on Edit Business
Page. As you will see, there are can be multiple forms present on the
page, namely different Opening Hours forms and Business info form. These
form must be edited 1 at a time. For example, assume you have two
opening hours forms. You edit both of the and press edit button on one
of the two. Despite setting changes to both, only the form that had its
'Edit' button pressed will apply those changes. The rest of changes to
other forms will be discarded.

# Guide On Features

## Login and Register

**Login** functionality requires to fill out 2 field. Username and
password field. Upon logging in, user is redirected to the main page. If
the process fails, error message describing the issue displays on the
top of the page.\
**Register** functionality requires fill out 2 required fields, username
and password, 1 optional field allows upload of an image file for user
profile picture, last field is a choice field (default value \"Yes\")
describing if user is business owner (can create businesses). Upon
successful registration, user is immediately logged in and redirected to
the main page. If the process fails, error message describing the issue
displays on the top of the page.\

## Register Business

**Register Business** functionality requires to fill out 2 required
fields, business name and business address. Business address is should
be auto completed as it automatically assigns latitude and longitude to
business (required by maps API). Additional 2 optional fields are
present, business description and business cover image.

## Business View

**Business view** is used to visually represent a business on the web
application. This view is accessible to all the users (logged in or
not). General layout is as follows:\
**Top of the page** contains the banner of the business. It presents user
with business name, business address as well as opening hours if they
are included (Fig. 1 does not have opening hours included). In addition,
Edit Business button is present for business owners to use to redirect
to edit business page.\
**Top navigation bar** contains name of each section of the business as well
as review section which is present for every business. Section are used
as logical groupings of items on the page. Clicking on section name will
scroll the section into view.\
**Sections** contain specific section. Each section may or may not
contain items (present in blue boxes).\
**Content per section** are items, each item has an image and name, followed
by its price (only £ are supported as displayed currency) and item
description.\
**Reviews section** contains comments. Each
comment is contained in a box with the name of the user and their
profile picture shown on top, as well as the date posted. Underneath is
shown the review itself. In addition, each user can delete their review
by clicking on delete review button. Each user, that is logged in and is
not owner of that specific business can leave a review.

## Edit Business

**Edit Business** view is used to edit information regarding business,
such as its address, description and cover images as well as edit or add
opening hours, add or delete sections and section items.

### Edit Details

Top of the page contains edit form. This form is filled out with pre-existing information about
business. Upon changing some information and pressing Edit button, these
changes are saved and success message is displayed.

### Add Opening Hours

Add Hours button can be used to trigger modal. This modal contains 4 choice fields.
First, second to last and last fields are required. Second field can be
left empty.\
Once the form is field, pressing create will create new opening hours.
Provided form was valid, success message is displayed.


### Edit Opening Hours

Provided there are already created Opening Hours, forms are displayed on the Edit Business Page.
Each form can be manipulated to change specific aspect(s) of the Opening
Hours. Once changes are selected, edit button will apply these changes.
Success message is displayed if the change was successful. Additionally,
delete icon is present for deleting specific opening hours.

### Create Section

Create Section button can be used to trigger a
modal. This modal contains form with singe
field for name of the section. Once this field is filled out, Create
button can be pressed. Success message is displayed if action was
successful.


### Create Item

Create Section button can be used to trigger
modal. However, this button is only present if
there are existing section. If business does not have any section, this
button is omitted.\
Once the modal is triggered, form is presented with form containing 5
fields. Name and price fields are required. Moreover, price fields
allows values that are $\geq$ 0. Section filed is a choice field,
containing list of names of existing section. To add item to specific
section, select the name of that section it the choice field.


### Delete Section

In the lower parts of the Edit Business page, layout similar to the
Business page can be seen. Additionally, next to each section name is
delete icon, which when pressed, triggers modal informing user about
their action. If section contains items, it warns user all associated
items (provides specific number of times) will be deleted as well.

[Delete Section Warning]{.image}

### Delete Item

Delete item button is present next to each item in each section. Once
pressed, item is deleted. Success message is displayed once items is
deleted.

## Profile Page

Profile page is used to customize user information and also provided
access to list of associated businesses (owned, favorite, reviewed).

### Edit Profile Image

Profile image can be edited via Edit Image button which triggers a modal. In this modal, user can select an image they want to uplaod as well as clear option to remove existing image (defaul image will be used in that case)

### Edit Profile Description

Profile description can be changed via Edit Description button which triggers a modal. In this modal, user can write exhaustive description of themselves. Note however, description is not used anywhere in the web app and serves no practical purpose as of now.
