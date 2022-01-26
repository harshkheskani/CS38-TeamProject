from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from leidos_app.forms import *
from django.contrib import messages
from django.urls import reverse

# Create your views here.
def base(request):
    return render(request, 'leidos_app/base.html')


def create_menu(request):
    return render(request, 'leidos_app/create_menu.html')  

def menu(request):
    return render(request, 'leidos_app/menu.html')  

def  homepage(request):
    return render(request, 'leidos_app/homepage.html')


def user_register(request):
    registered = False

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
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'leidos_app/register.html', context={'user_form': user_form, 'profile_form': profile_form})


def user_login(request):
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
        return render(request, 'leidos_app/login.html')


@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return redirect(reverse('leidos_app:homepage'))


def create_item(request, business_name_slug):

    if request.method == 'GET':
        tuples = []
        for section in MenuSection.objects.get(business_fk=Business.objects.get(slug=business_name_slug)):
            tuples.append((section, section.name))

        form = forms.AddItemForm(choices=tuples)
        print(form)
        return render(request, "leidos_app/create_menu.html", {"form":form})

    if request.method == 'POST':
        form = AddItemForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect(reverse("leidos_app:business", kwargs={"business_name_slug":business_name_slug}))


def business(request, business_name_slug):

    if request.method == 'GET':
        # Retrieve all relevant information for business
        context_dict = get_business_info(business_name_slug)

        if context_dict is not None:

            context_dict["is_business_owner"] = request.user.is_autheticated and\
                                                request.user == context_dict["business"].user

            return render(request, "leidos_app/business.html", context_dict)
        else:
            messages.error(request, f"Business {business_name_slug} does not exists")
            return redirect(reverse('leidos_app:homepage'))

    else:
        messages.error(request, f"business.view() only accepts 'GET' requests, got {request.method} instead")
        return redirect(reverse('leidos_app:homepage'))


def get_business_info(business_slug):

    business = Business.objects.get(slug=business_slug)

    if business is not None:
        context_dict = {}
        context_dict["business"] = business

        menu_sections = MenuSection.objects.filter(business_fk=business)

        if menu_sections is not None:

            sections_list = []

            for menu_section in menu_sections:
                section_items = SectionItems.objects.filter(section_fk=menu_section)
                sections_list.append([menu_section] + section_items)

            context_dict["sections"] = sections_list    # [[section, sec_items, ...], ... ]
        else:
            context_dict["sections"] = None


        opening_times = OpeningTimes.objects.filter(business_fk=business)

        if opening_times is not None:
            context_dict["opening_times"] = opening_times
        else:
            context_dict["opening_times"] = None

        return context_dict

    else:
        return None