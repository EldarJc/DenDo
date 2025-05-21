from django.test import TestCase
from django.contrib.auth import get_user_model, authenticate

from .forms import (
    SignUpForm,
    LogInForm,
    UserEditForm,
    PasswordUpdateForm,
)
# Create your tests here.

USERNAME = 'newuser'
EMAIL = 'newuser@example.com'
PASSWORD = '12345678'
BIO = 'Testing bio field.'


def create_test_form(form_class, **kwargs):
        USERNAME = 'testuser'
        EMAIL = 'test@example.com'
        PASSWORD = 'correct_password'
        BIO = 'This is a sample bio used purely for testing purposes.'
        forms={
            'SignUpForm':{
                'data':{
                    'username': kwargs.get('username', USERNAME),
                    'email': kwargs.get('email', EMAIL),
                    'password': kwargs.get('password', PASSWORD),
                    'confirm_password': kwargs.get('confirm_password', PASSWORD)

                },
                'files':{},
                'kwargs':{}
            },
            'UserEditForm':{
                'data':{
                    'username':kwargs.get('username', USERNAME),
                    'bio': kwargs.get('bio', BIO),
                },
                'files':{
                    'banner': kwargs.get('banner', None),
                    'avatar': kwargs.get('avatar', None),
                },
                'kwargs':{
                    'user': kwargs.get('user', None)
                }
            },
            'PasswordUpdateForm':{
                'data':{
                    'old_password':kwargs.get('old_password', PASSWORD),
                    'new_password': kwargs.get('new_password', '12345678'),
                },
                'files': {},
                'kwargs':{
                    'current_password_hash': kwargs.get('current_password_hash', None),
                }
            },
            'LogInForm':{
                'data':{
                    'username_or_email': kwargs.get('username_or_email', EMAIL),
                    'password': kwargs.get('password', PASSWORD)
                },
                'files': {},
                'kwargs':{}
            }
        }
        if form_class.__name__ in forms:
            form_data = forms[form_class.__name__]
            return form_class(data=form_data.get('data'), files=form_data.get('files'), **form_data.get('kwargs'))
        
        raise ValueError(f"Test data for form '{form_class.__name__}' is not defined in FormHelper.")

class BaseUserTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username=USERNAME,
            email=EMAIL,
            password=PASSWORD,
            bio=BIO,
            avatar=None,
            banner=None
        )

class SignUpFormTest(TestCase):
    def test_signup_form_valid_data(self):
        valid_form = create_test_form(SignUpForm)
        self.assertTrue(valid_form.is_valid())

    def test_signup_form_invalid_data(self):
        invalid_form = create_test_form(SignUpForm,username= '', email='', password='', confirm_password='')
        self.assertFalse(invalid_form.is_valid())

class UserEditFormTest(BaseUserTestCase):
    def test_valid_update_form(self):
        valid_form = create_test_form(UserEditForm,user=self.user)
        print(self.user)
        self.assertTrue(valid_form.is_valid())
        valid_form.save()
        self.user.refresh_from_db()
        print(self.user)

    def test_no_data_update_form(self):
        invalid_form = create_test_form(UserEditForm, username='', bio='', banner=None, avatar=None, user=self.user)
        print(self.user)
        self.assertTrue(invalid_form.is_valid())
        invalid_form.save()
        print(self.user)


class PasswordUpdateFormTest(BaseUserTestCase):
    def test_valid_data_update_password(self):
        form = create_test_form(PasswordUpdateForm, old_password=PASSWORD, new_password='newpassword', current_password_hash=self.user.password)
        self.assertTrue(form.is_valid())
        self.assertEqual(len(form.errors), 0)

    def test_invalid_data_update_password(self):
        form = create_test_form(PasswordUpdateForm, current_password_hash=self.user.password)

        self.assertFalse(form.is_valid())
        self.assertIn('old_password', form.errors)
        self.assertIn('new_password', form.errors)

class LoginFormTest(BaseUserTestCase):
    def test_valid_form_data(self):
        form = create_test_form(LogInForm, username_or_email=self.user.username, password=PASSWORD)
        self.assertTrue(form.is_valid())
     
    def test_invalid_form_data(self):
        form = create_test_form(LogInForm, username_or_email='', password='')
        self.assertFalse(form.is_valid())
    
    def test_authenticate_custom_backend(self):
        user_with_username = authenticate(username=USERNAME, password=PASSWORD)
        user_with_email = authenticate(username=EMAIL, password=PASSWORD)
        self.assertEqual(user_with_username, self.user)
        self.assertEqual(user_with_email, self.user)
        self.assertEqual(authenticate(username='', password=''), None)