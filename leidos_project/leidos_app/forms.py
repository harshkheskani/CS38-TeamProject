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


class AddItemForm(forms.ModelForm):


    def __init__(self, *args, **kwargs):

        choices = kwargs.pop("choices")
        super(AddItemForm, self).__init__(*args, **kwargs)
        self.fields["sections"] = forms.ChoiceField(choices=choices)

    class Meta:
        model = SectionItem
        fields = ('name', 'description', 'price', 'img')
        exclude = ('section_fk',)
        





