from django import forms
from django.contrib.auth.models import User
from .models import *




class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'password')

        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "password": forms.PasswordInput(attrs={"class": "form-control"}),
        }


class UserProfileForm(forms.ModelForm):
    is_business_owner = forms.ChoiceField(choices=[("Yes","Yes"), ("No","No")],
                                          label="Are you a business owner?",
                                          widget=forms.Select(attrs={"class": "form-control"}))

    class Meta:
        model = UserProfile
        fields = ('profile_pic',)

        labels = {
            "profile_pic": "Profile Picture",
        }

        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "password": forms.PasswordInput(attrs={"class": "form-control"}),
            "profile_pic": forms.FileInput(attrs={"class": "form-control"}),
        }


class AddSectionForm(forms.ModelForm):

    class Meta:
        model = MenuSection
        exclude = ('business_fk',)

        widgets = {
            "name": forms.TextInput(attrs={"class":"form-control"}),
        }


class AddItemForm(forms.ModelForm):


    def __init__(self, *args, **kwargs):

        choices = kwargs.pop("choices", None)
        super(AddItemForm, self).__init__(*args, **kwargs)
        self.fields["sections"] = forms.ChoiceField(choices=choices, widget=forms.Select(attrs={"class":"form-select"}))

    class Meta:
        model = SectionItem
        exclude = ('section_fk',)

        labels = {
            "img": "Item Image",
        }

        widgets = {
            "name": forms.TextInput(attrs={"class":"form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "img": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "price": forms.NumberInput(attrs={"class": "form-control"}),
        }

class AddOpeningTimesForm(forms.ModelForm):

    class Meta:
        model = OpeningHours
        exclude = ('business_fk',)

        widgets = {
            "weekday_from": forms.Select(attrs={"class": "form-control"}),
            "weekday_to": forms.Select(attrs={"class": "form-control"}),
            "from_hour": forms.Select(attrs={"class": "form-control"}),
            "to_hour": forms.Select(attrs={"class": "form-control"}),
        }

class RegisterBusinessForm(forms.ModelForm):

    slug = forms.SlugField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Business
        exclude = ('owner_fk',)

        labels = {
            "img": "Cover Image",
        }

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "address": forms.TextInput(attrs={"class": "form-control"}),
            "img": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows":3}),
        }

class EditBusinessForm(forms.ModelForm):

    class Meta:
        model = Business
        exclude = ('owner_fk', 'slug', 'name')

        labels = {
            "img": "Cover Image"
        }

        widgets = {
            "address": forms.TextInput(attrs={"class": "form-control"}),
            "img": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows":3}),
        }

class EditOpeningHours(forms.ModelForm):

    class Meta:
        model = OpeningHours
        exclude = ('business_fk',)

        widgets = {
            "weekday_from": forms.Select(attrs={"class": "form-control"}),
            "weekday_to": forms.Select(attrs={"class": "form-control"}),
            "from_hour": forms.Select(attrs={"class": "form-control"}),
            "to_hour": forms.Select(attrs={"class": "form-control"}),
        }

