from django.test import TestCase
from .models import UserProfile

class UserProfileTests(TestCase):

    def test_create_user_profile(self):
        """Test creating a valid user profile."""
        profile = UserProfile.objects.create(
            full_name='Duha Abu Hamid',
            id_number='123456789',
            department='Software Engineering',
            year=2023,
            mobile_number='0501234567',
            email='duha@example.com'
        )
        self.assertEqual(profile.full_name, 'Duha Abu Hamid')
        self.assertEqual(profile.id_number, '123456789')
        self.assertEqual(profile.department, 'Software Engineering')
        self.assertEqual(profile.year, 2023)
        self.assertEqual(profile.mobile_number, '0501234567')
        self.assertEqual(profile.email, 'duha@example.com')

    def test_invalid_email(self):
        """Test that an exception is raised for invalid email."""
        with self.assertRaises(ValueError):
            UserProfile.objects.create(
                full_name='Duha Abu Hamid',
                id_number='123456789',
                department='Software Engineering',
                year=2023,
                mobile_number='0501234567',
                email='invalid-email'  # Invalid email
            )

    def test_invalid_mobile_number(self):
        """Test that an exception is raised for invalid mobile numbers."""
        with self.assertRaises(ValueError):
            UserProfile.objects.create(
                full_name='Duha Abu Hamid',
                id_number='123456789',
                department='Software Engineering',
                year=2023,
                mobile_number='1234567890',  # Invalid mobile number
                email='duha@example.com'
            )
    INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    ]

    def test_valid_submission(self):
        """Test the submission process with valid data."""
        response = self.client.post('/submit/', {
            'full_name': 'Duha Abu Hamid',
            'id_number': '123456789',
            'department': 'Software Engineering',
            'year': '2023',
            'mobile_number': '0501234567',
            'email': 'duha@example.com'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Full Name: Duha Abu Hamid', response.content)

    def test_invalid_submission_phone(self):
        """Test the submission process with an invalid phone number."""
        response = self.client.post('/submit/', {
            'full_name': 'Duha Abu Hamid',
            'id_number': '123456789',
            'department': 'Software Engineering',
            'year': '2023',
            'mobile_number': '1234567890',  # Invalid phone number
            'email': 'duha@example.com'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Error: Phone number must start with '05' and be 10 digits long.", response.content)

    def test_invalid_submission_email(self):
        """Test the submission process with an invalid email."""
        response = self.client.post('/submit/', {
            'full_name': 'Duha Abu Hamid',
            'id_number': '123456789',
            'department': 'Software Engineering',
            'year': '2023',
            'mobile_number': '0501234567',
            'email': 'invalid-email'  # Invalid email
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Error: Invalid email address.', response.content)