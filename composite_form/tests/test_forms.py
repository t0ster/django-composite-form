from django.test import TestCase
from django import forms

from composite_form.forms import CompositeForm


class ProfileAddressForm(forms.Form):
    address = forms.CharField()


class ProfileBirthDayForm(forms.Form):
    birthday = forms.DateField()


class ProfileForm(CompositeForm):
    form_list = [ProfileAddressForm, ProfileBirthDayForm]


class FormsTests(TestCase):
    def test_forms(self):
        profile_form = ProfileForm()
        profile_form = ProfileForm({"address": "13 Test St"})
        self.assertEqual(profile_form.errors, {'birthday': [u'This field is required.']})
