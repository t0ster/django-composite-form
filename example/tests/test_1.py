# Regression test for https://github.com/t0ster/django-composite-form/issues/1

from django.test import TestCase
from django.contrib.auth.models import User


from example.forms import ProfileForm, BaseProfileForm, UserCreationForm, AnotherForm
from example.models import Profile


class FormsTests(TestCase):
    def setUp(self):
        profile_form = ProfileForm({
            "address": "13 Test St",
            "username": "test_user",
            "password1": "123456",
            "password2": "123456",
        })
        profile_form.save()
        self.user = User.objects.all()[0]
        self.profile = Profile.objects.all()[0]

    def test_1(self):
        profile_form = ProfileForm(instances=[self.user, self.profile])
        self.assertEqual(profile_form.get_form(UserCreationForm).instance, self.user)
        self.assertEqual(profile_form.get_form(BaseProfileForm).instance, self.profile)

    def test_2(self):
        profile_form = ProfileForm(instances=[self.user, None])
        self.assertEqual(profile_form.get_form(UserCreationForm).instance, self.user)
        self.assertIsInstance(profile_form.get_form(BaseProfileForm).instance, Profile)

    def test_3(self):
        profile_form = ProfileForm(instances=[None, self.profile])
        self.assertEqual(profile_form.get_form(BaseProfileForm).instance, self.profile)
        self.assertIsInstance(profile_form.get_form(UserCreationForm).instance, User)

    def test_4(self):
        another_form = AnotherForm({}, instances=[None, self.user])
        another_form.is_valid()
