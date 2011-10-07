from django.test import TestCase
from django.contrib.auth.models import User

from example.forms import ProfileForm
from example.models import Profile


class FormsTests(TestCase):
    def test_forms(self):
        profile_form = ProfileForm()
        profile_form = ProfileForm({
            "username": "t0ster",
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
            "username": "t0ster",
            "password1": "123456",
            "password2": "123456",
        })
        profile_form.save()
        self.assertEqual(Profile.objects.count(), 1)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Profile.objects.all()[0].user, User.objects.all()[0])
        self.assertEqual(Profile.objects.all()[0].address, "blah")
