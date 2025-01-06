from django.test import TestCase, Client
import json

class UpdateRequestTest(TestCase):
    def setUp(self):
        # יצירת לקוח לבדיקות
        self.client = Client()
        self.url = '/update-request/'  # כתובת ה-URL של ה-View

    def test_valid_data(self):
        # בדיקה עם נתונים תקינים
        valid_data = {
            'full_name': 'יוסי כהן',
            'id_number': '123456789',
            'department': 'מחשבים',
            'year': '2024',
            'phone': '0501234567',
            'email': 'yossi@example.com'
        }
        response = self.client.post(self.url, data=json.dumps(valid_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('message'), 'Request updated successfully')

    def test_missing_required_fields(self):
        # בדיקה עם נתונים חסרים
        invalid_data = {
            'full_name': 'יוסי כהן',
            # חסר id_number
            'department': 'מחשבים',
            'year': '2024',
            'phone': '0501234567',
            'email': 'yossi@example.com'
        }
        response = self.client.post(self.url, data=json.dumps(invalid_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())

    def test_invalid_method(self):
        # בדיקה עם שיטה לא חוקית (GET במקום POST)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)
        self.assertIn('error', response.json())
