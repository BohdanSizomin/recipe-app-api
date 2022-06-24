from django.test import TestCase
from core.models import User



class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        ''' Test creating a new user with an email is successfull '''

        email = 'test@gmail.com'
        password = 'test123'

        user = User.objects.create_user(
            email = email,
            password = password,
        )


        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))



    def test_new_user_email_normalized(self):
        """ Temp the email for a new user is normalized """
        email = 'test@LONDONAPPDEV.com'

        user = User.objects.create_user(email,'test123')

        self.assertEqual(user.email, email.lower())



    def test_new_user_invalid_email(self):
        """ Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            User.objects.create_user(None,'123456test')

    def test_create_new_superuser(self):
        """ Test creating a new SU"""
        user = User.objects.create_superuser(
            'test@gmail.coM',
            'test123213'
            )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

