from django.test import TestCase
from .models import UserProfile

class UserProfileTests(TestCase):

    def test_create_user_profile(self):
        profile = UserProfile.objects.create(
            full_name='Duha Abu Hamid',
            id_number='123456789',
            department='Software Engineering',
            year=2023,
            mobile_number='0501234567',
            email='duha@example.com'
        )
        self.assertEqual(profile.full_name, 'Duha Abu Hamid')
        self.assertEqual(profile.department, 'Software Engineering')
        self.assertEqual(profile.year, 2023)
        self.assertEqual(profile.mobile_number, '0501234567')
        self.assertEqual(profile.email, 'duha@example.com')

    def test_invalid_email(self):
        with self.assertRaises(ValueError):
            UserProfile.objects.create(
                full_name='Duha Abu Hamid',
                id_number='123456789',
                department='Software Engineering',
                year=2023,
                mobile_number='0501234567',
                email='invalid-email'  # Invalid email
            )
    
    def test_invalid_id_number_length(self):
        with self.assertRaises(ValueError):
            UserProfile.objects.create(
                full_name='Duha Abu Hamid',
                id_number='12345',  # Invalid length
                department='Software Engineering',
                year=2023,
                mobile_number='0501234567',
                email='duha@example.com'
            )
