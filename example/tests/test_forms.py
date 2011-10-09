from django.test import TestCase
from django.contrib.auth.models import User

from example.forms import ProfileForm, BaseProfileForm, UserCreationForm
from example.models import Profile


class FormsTests(TestCase):
    def test_forms(self):
        profile_form = ProfileForm()
        profile_form = ProfileForm({
            "username": "test_user",
            "password1": "123456",
            "password2": "123456",
        })
        self.assertEqual(profile_form.errors, {
            'address': [u'This field is required.'],
        })
        self.assertRaises(ValueError, lambda: profile_form.save())
        self.assertEqual(User.objects.count(), 0)

        profile_form = ProfileForm({
            "address": "13 Test St",
        })
        self.assertEqual(profile_form.errors, {
                'password1': [u'This field is required.'],
                'password2': [u'This field is required.'],
                'username': [u'This field is required.']
        })

        profile_form = ProfileForm({
            "address": "13 Test St",
            "username": "test_user",
            "password1": "123456",
            "password2": "123456",
        })
        self.assertRaises(NotImplementedError, lambda: unicode(profile_form))
        profile_form.save()
        self.assertEqual(Profile.objects.count(), 1)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Profile.objects.all()[0].user, User.objects.all()[0])
        self.assertEqual(Profile.objects.all()[0].address, "blah")

        user = User.objects.all()[0]
        profile = Profile.objects.all()[0]
        self.assertRaises(ValueError, lambda: ProfileForm(instances=profile))
        self.assertRaises(ValueError, lambda: ProfileForm(instances=[profile]))
        profile_form = ProfileForm(instances=[user, profile])
        self.assertEqual(profile_form.get_form(UserCreationForm).instance.username, "test_user")
        self.assertEqual(profile_form.get_form(BaseProfileForm).instance.address, "blah")
        unicode(profile_form.get_form(UserCreationForm))
        unicode(profile_form.get_form(BaseProfileForm))
