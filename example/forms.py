from django import forms
from django.contrib.auth.forms import UserCreationForm

from composite_form.forms import CompositeForm

from example.models import Profile


class BaseProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ("user")


class ProfileForm(CompositeForm):
    form_list = [UserCreationForm, BaseProfileForm]

    def clean_address(self):
        return "blah"

    def save(self, commit=True):
        if not self.is_valid():
            raise ValueError("Invalid form")
        user_form = self.get_form(UserCreationForm)
        user = user_form.save()
        profile_form = self.get_form(BaseProfileForm)
        profile_form.instance.user = user
        return profile_form.save()


class AddressForm(forms.Form):
    address1 = forms.CharField()


class AnotherForm(CompositeForm):
    form_list = [AddressForm, UserCreationForm]

    def save(self, commit=True):
        if not self.is_valid():
            raise ValueError("Invalid form")
        address_form = self.get_form(AddressForm)
        user_form = self.get_form(UserCreationForm)
        user_form.save()
