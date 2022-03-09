import re
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from leidos_app.forms import *
from django.contrib import messages
from django.urls import reverse
from django.utils.text import slugify


def homepage(request):

    context_dict = {
        "businesses": get_all_businesses()
    }

    #TODO query list of closest businesses and return it in context dict.
    return render(request, 'leidos_app/homepage.html', context_dict)

def search_business(request, path):

    path = path.replace("X", "/")

    b_name = request.GET.get("business_name", "")

    b_slug = slugify(b_name)

    if business_exists(b_slug):
        return redirect(reverse("leidos_app:business", kwargs={"business_name_slug":b_slug}))
    else:
        messages.warning(request, f"Business {b_name} does not exist")
        return redirect(path)



@login_required
def profile(request):

    context_dict = {
        "businesses": get_all_businesses()
    }

    return render(request, 'leidos_app/profile.html', context_dict)

def user_register(request):

    context_dict = {
        "businesses": get_all_businesses()
    }

    if request.method == "POST":
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user

            # Set profile image if included (else set default [set in models])
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.is_business_owner = request.POST.get("is_business_owner") == "Yes"


            profile.save()

            login(request, user)
            messages.success(request, "You have successfully registered!")
            return redirect(reverse("leidos_app:homepage"))

        else:
            for field in user_form:
                for error in field.errors:
                    messages.warning(request, error)
            for field in profile_form:
                for error in field.errors:
                    messages.warning(request, error)

            return redirect(reverse("leidos_app:register"))

    else:
        context_dict["user_form"] = UserForm()
        context_dict["profile_form"] = UserProfileForm()

    return render(request, 'leidos_app/register.html', context_dict)


def user_login(request):

    context_dict = {
        "businesses": get_all_businesses()
    }

    # If the request is an HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)
        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                messages.success(request, "You have successfully logged in!")
                return redirect(reverse('leidos_app:homepage'))
            else:
                # An inactive account was used - no logging in!
                messages.error(request, "Your Leidos account is disabled")
                return redirect(reverse("leidos_app:login"))
        else:
            # Bad login details were provided. So we can't log the user in.
            print(f"Invalid login details: {username}, {password}")
            messages.error(request, "Invalid login details")
            return redirect(reverse("leidos_app:login"))
    # The request is not a HTTP POST, so display the login form
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'leidos_app/login.html', context_dict)


@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return redirect(reverse('leidos_app:homepage'))

@login_required
def create_section_item(request, business_name_slug):

    if not business_exists(business_name_slug):
        messages.error(request, f"Business {business_name_slug} does not exists")
        return redirect('leidos_app:homepage')

    if request.user != Business.objects.get(slug=business_name_slug).owner_fk:
        messages.error(request, "You do not have access to this option")
        return redirect(reverse('leidos_app:business', kwargs={"business_name_slug":business_name_slug}))

    if MenuSection.objects.filter(business_fk=Business.objects.get(slug=business_name_slug)).exists():
        sections = MenuSection.objects.filter(business_fk=Business.objects.get(slug=business_name_slug))
    else:
        messages.error(request, "FATAL_ERROR:: Item creation attempted without pre-existing Section")
        return redirect("leidos_app:homepage")

    form = AddItemForm(request.POST or None, choices=[(section, section.name) for section in sections])

    if request.method == 'POST':

        if form.is_valid():
            section_item = form.save(commit=False)
            section_item.section_fk = MenuSection.objects.get(name=request.POST.get("sections"),
                                                              business_fk=Business.objects.get(slug=business_name_slug))

            if "img" in request.FILES:
                section_item.img = request.FILES["img"]

            section_item.save()

            messages.success(request, f"Added '{section_item.name}' to section "
                                      f"'{section_item.section_fk.name}'")
            return redirect(reverse("leidos_app:edit_business", kwargs={"business_name_slug":business_name_slug}))
        else:
            print(form.errors)
            messages.error(request, form.errors)
            return redirect(reverse("leidos_app:edit_business", kwargs={"business_name_slug":business_name_slug}))

@login_required
def delete_section_item(request, item_pk):
    if request.user != SectionItem.objects.get(pk=item_pk).section_fk.business_fk.owner_fk and not request.user.is_superuser:
        messages.error(request, "You do not have access to this feature")
        return redirect("leidos_app:homepage")

    object_to_delete = SectionItem.objects.get(pk=item_pk)
    business_name_slug = object_to_delete.section_fk.business_fk.slug
    s_name = object_to_delete.name
    object_to_delete.delete()

    if not SectionItem.objects.filter(pk=item_pk).exists():
        messages.success(request, f"Item '{s_name}' successfully deleted")
        return redirect(reverse("leidos_app:edit_business", kwargs={"business_name_slug": business_name_slug}))
    else:
        messages.error(request, f"Failed to delete Item '{s_name}'")
        return redirect(reverse("leidos_app:edit_business", kwargs={"business_name_slug": business_name_slug}))

@login_required
def create_section(request, business_name_slug):

    if not business_exists(business_name_slug):
        messages.error(request, f"Business '{business_name_slug}' does not exist")
        return redirect(reverse("leidos_app:homepage"))

    if request.user != Business.objects.get(slug=business_name_slug).owner_fk:
        messages.error(request, "You do not have access to this option")
        return redirect(reverse('leidos_app:business', kwargs={"business_name_slug":business_name_slug}))

    if request.method == 'POST':

        form = AddSectionForm(request.POST)

        if form.is_valid():
            section = form.save(commit=False)
            section.business_fk = Business.objects.get(slug=business_name_slug)
            section.save()

            messages.success(request, f"Sections '{section.name}' has been created successfully.")
            return redirect(reverse("leidos_app:edit_business", kwargs={"business_name_slug": business_name_slug}))
        else:
            return HttpResponse(form.errors)

@login_required
def delete_section(request, section_pk):

    if request.user != MenuSection.objects.get(pk=section_pk).business_fk.owner_fk and not request.user.is_superuser:
        messages.error(request, "You do not have access to this feature")
        return redirect("leidos_app:homepage")

    object_to_delete = MenuSection.objects.get(pk=section_pk)
    business_name_slug = object_to_delete.business_fk.slug
    s_name = object_to_delete.name
    object_to_delete.delete()

    if not MenuSection.objects.filter(pk=section_pk).exists():
        messages.success(request, f"Section '{s_name}' successfully deleted")
        return redirect(reverse("leidos_app:edit_business", kwargs={"business_name_slug": business_name_slug}))
    else:
        messages.error(request, f"Failed to delete Section '{s_name}'")
        return redirect(reverse("leidos_app:edit_business", kwargs={"business_name_slug": business_name_slug}))


def business(request, business_name_slug):

    if not business_exists(business_name_slug):
        messages.error(request, f"Business '{business_name_slug}' does not exist")
        return redirect(reverse("leidos_app:homepage"))

    context_dict = {
        "businesses": get_all_businesses()
    }

    if request.method == 'GET':
        # Retrieve all relevant information for business
        context_dict.update(get_business_info(business_name_slug))

        if context_dict is not None:

            context_dict["is_business_owner"] = request.user == context_dict["business"].owner_fk
            context_dict["comment_form"] = AddCommentForm()

            if Comment.objects.filter(business_fk=context_dict["business"]).exists():
                context_dict["comments"] = Comment.objects.filter(business_fk = context_dict["business"])

            if not request.user.is_anonymous:
                context_dict["is_favorite"] = Favorite.objects.filter(user_fk=request.user,
                                                                  business_fk=context_dict["business"]).exists()

            return render(request, "leidos_app/business.html", context_dict)
        else:
            messages.error(request, f"Business {business_name_slug} does not exists")
            return redirect(reverse('leidos_app:homepage'))

    else:
        messages.error(request, f"business.view() only accepts 'GET' requests, got {request.method} instead")
        return redirect(reverse('leidos_app:homepage'))

@login_required
def add_opening_hours(request, business_name_slug):

    if not business_exists(business_name_slug):
        messages.error(request, f"Business {business_name_slug} does not exists")
        return redirect('leidos_app:homepage')

    if request.user != Business.objects.get(slug=business_name_slug).owner_fk:
        messages.error(request, "You do not have access to this option")
        return redirect(reverse('leidos_app:business', kwargs={"business_name_slug":business_name_slug}))


    if request.method == 'POST':
        form = AddOpeningTimesForm(request.POST)

        if form.is_valid():
            opening_hours_form = form.save(commit=False)
            opening_hours_form.business_fk = Business.objects.get(slug=business_name_slug)
            opening_hours_form.save()

            messages.success(request, "New opening time successfully added")

            return redirect(reverse('leidos_app:edit_business', kwargs={"business_name_slug": business_name_slug}))
        else:
            return HttpResponse(form.errors)

@login_required
def delete_opening_hours(request, hours_pk):

    if request.user != OpeningHours.objects.get(pk=hours_pk).business_fk.owner_fk and not request.user.is_superuser:
        messages.error(request, "You do not have access to this feature")
        return redirect("leidos_app:homepage")

    object_to_delete = OpeningHours.objects.get(pk=hours_pk)
    business_name_slug = object_to_delete.business_fk.slug
    object_to_delete.delete()

    if not OpeningHours.objects.filter(pk=hours_pk).exists():
        messages.success(request, "Opening Hours successfully deleted")
        return redirect(reverse("leidos_app:edit_business", kwargs={"business_name_slug": business_name_slug}))
    else:
        messages.error(request, "Failed to delete Opening Hours")
        return redirect(reverse("leidos_app:edit_business", kwargs={"business_name_slug": business_name_slug}))

@login_required
def edit_business(request, business_name_slug):

    if not business_exists(business_name_slug):
        messages.error(request, f"Business '{business_name_slug}' does not exist")
        return redirect(reverse("leidos_app:homepage"))

    business_obj = Business.objects.get(slug=business_name_slug)

    if request.user != business_obj.owner_fk and not request.user.is_superuser:
        messages.error(request, "You do not have access to this feature")
        return redirect(reverse("leidos_app:homepage"))

    context_dict = {
        "businesses": get_all_businesses()
    }

    if request.method == 'GET':

        context_dict.update({"business":business_obj})

        edit_business_form = EditBusinessForm(initial={
            "name":business_obj.name,
            "address": business_obj.address,
            "img":business_obj.img,
            "description": business_obj.description,
        },)

        context_dict["business_form"] = edit_business_form
        opening_hour_obj_form_list = []

        if OpeningHours.objects.filter(business_fk=business_obj).exists():
            for opening_hours_obj in OpeningHours.objects.filter(business_fk=business_obj):
                opening_hours_form = EditOpeningHours(initial={
                    "weekday_from":opening_hours_obj.weekday_from,
                    "weekday_to":opening_hours_obj.weekday_to,
                    "from_hour":opening_hours_obj.from_hour,
                    "to_hour":opening_hours_obj.to_hour,
                })
                # [(opening_hours_obj, opening_hours_form), ...]
                opening_hour_obj_form_list.append((opening_hours_obj, opening_hours_form))

            context_dict["hours_forms"] = opening_hour_obj_form_list
        else:
            context_dict["hours_forms"] = None

        if MenuSection.objects.filter(business_fk=business_obj).exists():

            menu_sections = MenuSection.objects.filter(business_fk=business_obj)

            sections_list = []

            for menu_section in menu_sections:
                section_items = SectionItem.objects.filter(section_fk=menu_section)
                sections_list.append((menu_section,section_items))

            context_dict["sections"] = sections_list    # [ (section, QuerySet<item....>),.... ]
        else:
            context_dict["sections"] = None


        context_dict["section_form"] = AddSectionForm()
        context_dict["hours_form"] = AddOpeningTimesForm()

        if MenuSection.objects.filter(business_fk=Business.objects.get(slug=business_name_slug)).exists():
            sections = MenuSection.objects.filter(business_fk=Business.objects.get(slug=business_name_slug))
            context_dict["section_item_form"] = AddItemForm(choices=[(section, section.name) for section in sections])
        else:
            sections = None
            context_dict["section_item_form"] = None



        return render(request, "leidos_app/edit_business.html", context_dict)

@login_required
def save_business_edit(request, business_name_slug):
    if request.method == 'POST':
        edit_form = EditBusinessForm(request.POST, instance=Business.objects.get(slug=business_name_slug))

        if edit_form.is_valid():
            business_edit = edit_form.save(commit=False)

            if 'img' in request.FILES:
                business_edit.img = request.FILES['img']

            business_edit.save()
            messages.success(request, "Business details successfully changed")
            return redirect(reverse("leidos_app:edit_business", kwargs={"business_name_slug": business_name_slug}))

        else:
            return HttpResponse(edit_form.errors)

@login_required
def save_opening_hours_edit(request, hours_pk):
    if request.method == 'POST':
        hours = OpeningHours.objects.get(pk=hours_pk)
        edit_form = EditOpeningHours(request.POST, instance=hours)

        if edit_form.is_valid():
            edit_form.save()
            messages.success(request, "Opening hours details successfully changed")
            return redirect(reverse("leidos_app:edit_business", kwargs={"business_name_slug": hours.business_fk.slug}))

        else:
            return HttpResponse(edit_form.errors)


@login_required
def register_business(request):

    if not UserProfile.objects.get(user=request.user).is_business_owner:
        messages.error(request, "You do not have access to this feature")
        return redirect(reverse("leidos_app:homepage"))

    if request.method == 'GET':

        context_dict = {
            "businesses": get_all_businesses(),
            "form": RegisterBusinessForm()
        }

        return render(request, "leidos_app/register_business.html", context_dict)

    if request.method == 'POST':
        form = RegisterBusinessForm(request.POST)

        if form.is_valid():
            business_obj = form.save(commit=False)

            if 'img' in request.FILES:
                business_obj.img = request.FILES['img']

            business_obj.owner_fk = request.user

            business_obj.save()

            return redirect(reverse("leidos_app:business", kwargs={"business_name_slug": business_obj.slug}))
        else:
            return HttpResponse(form.errors)

@login_required
def add_favorite(request, business_name_slug):

    if not business_exists(business_name_slug):
        messages.error(request, f"Business {business_name_slug} does not exists")
        return redirect('leidos_app:homepage')

    try:
        Favorite.objects.get(user_fk=request.user,business_fk=Business.objects.get(slug=business_name_slug))

    except Favorite.DoesNotExist: # I.e. user does not have this specific business in favorites already
        fav_obj = Favorite(user_fk = request.user, business_fk=Business.objects.get(slug=business_name_slug))
        fav_obj.save()

    return redirect(reverse("leidos_app:business",kwargs={"business_name_slug":business_name_slug}))

def remove_favorite(request, business_name_slug):

    if not business_exists(business_name_slug):
        messages.error(request, f"Business {business_name_slug} does not exists")
        return redirect('leidos_app:homepage')

    try:
        fav_obj = Favorite.objects.get(user_fk=request.user,business_fk=Business.objects.get(slug=business_name_slug))
        fav_obj.delete()
    except Favorite.DoesNotExist:
        return HttpResponse("Attempted to remove favorite without pre-existing object")

    return redirect(reverse("leidos_app:business", kwargs={"business_name_slug":business_name_slug}))

@login_required
def add_comment(request, business_name_slug):

    if not business_exists(business_name_slug):
        messages.error(request, f"Business {business_name_slug} does not exists")
        return redirect('leidos_app:homepage')

    business_obj = Business.objects.get(slug=business_name_slug)

    if request.user == business_obj.owner_fk:
        messages.info(request, f"You can not post comment on you own business")
        return redirect(reverse("leidos_app:business", kwargs={"business_name_slug":business_name_slug}))

    form = AddCommentForm(request.POST or None)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.business_fk = business_obj
        comment.user_fk = request.user
        comment.save()
        messages.success(request, "Comment successfully added")
        return redirect(reverse("leidos_app:business", kwargs={"business_name_slug": business_name_slug}))

    else:
        return HttpResponse(form.errors)

def delete_comment(request, comment_pk):

    if request.user != Comment.objects.get(pk=comment_pk).user_fk and not request.user.is_superuser:
        messages.error(request, "You do not have access to this feature")
        return redirect("leidos_app:homepage")

    object_to_delete = Comment.objects.get(pk=comment_pk)
    business_name_slug = object_to_delete.business_fk.slug
    object_to_delete.delete()

    if not Comment.objects.filter(pk=comment_pk).exists():
        messages.success(request, "Comment successfully deleted")
        return redirect(reverse("leidos_app:business", kwargs={"business_name_slug": business_name_slug}))
    else:
        messages.error(request, "Failed to delete Comment")
        return redirect(reverse("leidos_app:business", kwargs={"business_name_slug": business_name_slug}))


# UTILS #
def get_business_info(business_slug):

    try:
        business = Business.objects.get(slug=business_slug)

        context_dict = {}
        context_dict["business"] = business

        if MenuSection.objects.filter(business_fk=business).exists():

            menu_sections = MenuSection.objects.filter(business_fk=business)

            sections_list = []

            for menu_section in menu_sections:
                section_items = SectionItem.objects.filter(section_fk=menu_section)
                sections_list.append((menu_section,section_items))

            context_dict["sections"] = sections_list    # [ (section, QuerySet<item....>),.... ]
        else:
            context_dict["sections"] = None


        if OpeningHours.objects.filter(business_fk=business).exists():
            opening_hours = OpeningHours.objects.filter(business_fk=business)
            context_dict["opening_hours"] = opening_hours

        else:
            context_dict["opening_hours"] = None

        return context_dict

    except Business.DoesNotExist:
        return None


def business_exists(business_name_slug):
    try:
        Business.objects.get(slug=business_name_slug)
        return True
    except:
        return False


def get_all_businesses(): return Business.objects.all()