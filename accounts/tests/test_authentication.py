from django.test import TestCase

from accounts.authentication import PasswordlessAuthenticationBackend
from accounts.models import Token, User


class AuthenticationTest(TestCase):

    def test_returns_None_if_token_doesnt_exist(self):
        result = PasswordlessAuthenticationBackend().authenticate('no-such-token')
        self.assertIsNone(result)

    def test_return_new_user_if_token_exists(self):
        email = 'edith@example.com'
        token = Token.objects.create(email=email)
        user = PasswordlessAuthenticationBackend().authenticate(token.uid)
        new_user = User.objects.get(email=email)
        self.assertEqual(user, new_user)

    def test_returns_exsiting_user_if_token_exists(self):
        email = 'edith@example.com'
        existing_user = User.objects.create(email=email)
        token = Token.objects.create(email=email)
        user = PasswordlessAuthenticationBackend().authenticate(token.uid)
        self.assertEqual(user, existing_user)


class GetUserTest(TestCase):

    def test_gets_user_by_email(self):
        User.objects.create(email='another@example.com')
        desired_user = User.objects.create(email='edith@example.com')
        found_user = PasswordlessAuthenticationBackend().get_user('edith@example.com')
        self.assertEqual(desired_user, found_user)

    def test_returns_none_if_no_user_with_email(self):
        self.assertIsNone(PasswordlessAuthenticationBackend().get_user('edith@example.com'))
