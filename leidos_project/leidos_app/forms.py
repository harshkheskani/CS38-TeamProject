from django import forms
from django.contrib.auth.models import User
from .models import *




class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password')


class UserProfileForm(forms.ModelForm):
    is_business_owner = forms.ChoiceField(choices=[("Yes","Yes"), ("No","No")])

    class Meta:
        model = UserProfile
        fields = ('profile_pic',)


class AddSectionForm(forms.ModelForm):

    class Meta:
        model = MenuSection
        exclude = ('business_fk',)


class AddItemForm(forms.ModelForm):


    def __init__(self, *args, **kwargs):

        choices = kwargs.pop("choices", None)
        super(AddItemForm, self).__init__(*args, **kwargs)
        self.fields["sections"] = forms.ChoiceField(choices=choices)

    class Meta:
        model = SectionItem
        exclude = ('section_fk',)
        

class AddOpeningTimesForm(forms.ModelForm):

    class Meta:
        model = OpeningHours
        exclude = ('business_fk',)


class RegisterBusinessForm(forms.ModelForm):

    slug = forms.SlugField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Business
        exclude = ('owner_fk',)


class EditBusinessForm(forms.ModelForm):

    class Meta:
        model = Business
        exclude = ('owner_fk', 'slug', 'name')


class EditOpeningHours(forms.ModelForm):

    class Meta:
        model = OpeningHours
        exclude = ('business_fk',)