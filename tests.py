from django.test import TestCase, Client  # ייבוא מחלקות לבדיקה ולשליחת בקשות HTTP

from django.urls import reverse  # ייבוא reverse ליצירת כתובות URL
from django.contrib.auth import get_user_model  # ייבוא הפונקציה לקבלת מודל המשתמשים
from django.contrib.auth.hashers import check_password  # ייבוא פונקציה לבדיקה אם הסיסמה מוצפנת
from django.contrib.messages import get_messages  # ייבוא פונקציה לקריאת הודעות מערכת
from django.contrib.auth.models import User
from myapp.models import PrivateDiary, PrivateSession, DiaryGroup, DiaryStudent  # יש להתאים לפי המודלים שלך
from newapp.forms import PrivateDiaryForm  # ייבוא הטופס
from django.shortcuts import render, redirect

from django.forms import formset_factory  # ייבוא formset_factory ליצירת סט טפסים
from newapp.forms import GroupRequestForm, GroupOptionForm, GroupStudentsForm  # ייבוא הטפסים הנדרשים
from newapp.models import GroupRequest, GroupOption, GroupStudents  # ייבוא המודלים הרלוונטיים
from django.http import HttpResponseForbidden
from .models import PrivateDiary, DiaryGroup, Session
from .models import GroupRequest, GroupOption
from .models import PersonalRequest, GroupRequest, Schedule, Student
from .forms import PersonalRequestForm,DiaryGroupForm


#---------------------------------------------------------------------------------------------------------
User = get_user_model()  # השגת מודל המשתמשים המותאם

class FirstLoginTest(TestCase):  # מחלקה לבדיקה של תהליך ההתחברות הראשון
    def setUp(self):  # פונקציה להרצת פעולות הכנה לפני כל בדיקה
        self.client = Client()  # יצירת לקוח לדימוי בקשות HTTP
        self.first_login_url = reverse('first_login')  # יצירת ה-URL לבדיקה
        self.user_data = {  # הגדרת נתוני משתמש לבדיקה
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'securepassword',
            'phone_number': '1234567890',
            'id_number': '123456789',
            'specialization': 'Mathematics'
        }

    def test_first_login_success(self):  # בדיקה של הרשמה מוצלחת
        response = self.client.post(self.first_login_url, self.user_data)  # שליחת בקשה עם נתוני המשתמש
        self.assertEqual(response.status_code, 302)  # בדיקה אם יש הפניה (Redirect)
        self.assertRedirects(response, reverse('Teacherpage'))  # בדיקה אם ההפניה נכונה
        user = User.objects.get(username=self.user_data['username'])  # שליפת המשתמש מהמסד
        self.assertTrue(user)  # בדיקה אם המשתמש נוצר
        self.assertTrue(check_password(self.user_data['password'], user.password))  # בדיקה אם הסיסמה מוצפנת כראוי

    def test_duplicate_username(self):  # בדיקה של שם משתמש כפול
        User.objects.create(username='testuser', email='another@example.com', password='securepassword')  # יצירת משתמש עם אותו שם משתמש
        response = self.client.post(self.first_login_url, self.user_data)  # ניסיון להירשם עם אותו שם
        self.assertRedirects(response, reverse('login_M'))  # בדיקה אם ההפניה לדף ההתחברות
        messages = [m.message for m in get_messages(response.wsgi_request)]  # קבלת הודעות מערכת
        self.assertIn('Username already exists. Please log in.', messages)  # בדיקה אם ההודעה מתאימה

    def test_duplicate_email(self):  # בדיקה של אימייל כפול
        User.objects.create(username='anotheruser', email='testuser@example.com', password='securepassword')  # יצירת משתמש עם אותו אימייל
        response = self.client.post(self.first_login_url, self.user_data)  # ניסיון להירשם עם אותו אימייל
        self.assertRedirects(response, reverse('login_M'))  # בדיקה אם ההפניה לדף ההתחברות
        messages = [m.message for m in get_messages(response.wsgi_request)]  # קבלת הודעות מערכת
        self.assertIn('Email already exists. Please log in.', messages)  # בדיקה אם ההודעה מתאימה

    def test_duplicate_id_number(self):  # בדיקה של מספר זהות כפול
        User.objects.create(username='anotheruser', email='another@example.com', password='securepassword', id_number='123456789')  # יצירת משתמש עם אותו מספר זהות
        response = self.client.post(self.first_login_url, self.user_data)  # ניסיון להירשם עם אותו מספר זהות
        self.assertRedirects(response, reverse('login_M'))  # בדיקה אם ההפניה לדף ההתחברות
        messages = [m.message for m in get_messages(response.wsgi_request)]  # קבלת הודעות מערכת
        self.assertIn('id_number already exists. Please log in.', messages)  # בדיקה אם ההודעה מתאימה

    def test_get_request(self):  # בדיקה של בקשת GET
        response = self.client.get(self.first_login_url)  # שליחת בקשת GET
        self.assertEqual(response.status_code, 200)  # בדיקה אם הדף נטען בהצלחה
        self.assertTemplateUsed(response, 'first_login.html')  # בדיקה אם התבנית הנכונה נטענת


#---------------------------------------------------------------------------------------------------------
User = get_user_model()  # קבלת מודל המשתמשים בפרויקט

class LoginMTest(TestCase):  # מחלקת בדיקות עבור פונקציית ההתחברות login_M
    def setUp(self):  # פעולות הכנה לפני כל בדיקה
        self.client = Client()  # יצירת לקוח לדימוי בקשות HTTP
        self.login_url = reverse('login_M')  # יצירת URL דינמי לדף ההתחברות

        # יצירת משתמש לדוגמה לבדיקה
        self.user = User.objects.create_user(
            username='testteacher',
            email='teacher@example.com',
            password='securepassword',
            user_type='teacher',
            is_active=True
        )

    def test_login_success(self):  # בדיקת התחברות מוצלחת
        response = self.client.post(self.login_url, {  # שליחת בקשת POST עם נתוני המשתמש
            'username': 'testteacher',
            'password': 'securepassword'
        })
        self.assertEqual(response.status_code, 302)  # בדיקה אם יש הפניה (Redirect)
        self.assertRedirects(response, reverse('Teacherpage'))  # בדיקה אם ההפניה היא לדף המורה
        
        messages = [m.message for m in get_messages(response.wsgi_request)]  # קריאת הודעות מערכת
        self.assertIn('Welcome, testteacher!', messages)  # בדיקה אם מופיעה הודעת הצלחה

    def test_login_invalid_username(self):  # בדיקת התחברות עם שם משתמש לא נכון
        response = self.client.post(self.login_url, {  
            'username': 'wronguser',  # שם משתמש שאינו קיים
            'password': 'securepassword'
        })
        self.assertEqual(response.status_code, 200)  # בדיקה אם נשארים באותו עמוד
        self.assertTemplateUsed(response, 'login_M.html')  # בדיקה אם נטענת תבנית דף ההתחברות
        
        messages = [m.message for m in get_messages(response.wsgi_request)]  # קריאת הודעות מערכת
        self.assertIn('Invalid username or password.', messages)  # בדיקה אם מופיעה הודעת שגיאה

    def test_login_invalid_password(self):  # בדיקת התחברות עם סיסמה לא נכונה
        response = self.client.post(self.login_url, {  
            'username': 'testteacher',
            'password': 'wrongpassword'  # סיסמה לא נכונה
        })
        self.assertEqual(response.status_code, 200)  # בדיקה אם נשארים באותו עמוד
        self.assertTemplateUsed(response, 'login_M.html')  # בדיקה אם נטענת תבנית דף ההתחברות
        
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn('Invalid username or password.', messages)  # בדיקה אם מופיעה הודעת שגיאה

    def test_login_inactive_user(self):  # בדיקת התחברות עם משתמש לא פעיל
        self.user.is_active = False  # הפיכת המשתמש ללא פעיל
        self.user.save()  # שמירת השינוי במסד הנתונים
        
        response = self.client.post(self.login_url, {  
            'username': 'testteacher',
            'password': 'securepassword'
        })
        self.assertEqual(response.status_code, 200)  # בדיקה אם נשארים באותו עמוד
        self.assertTemplateUsed(response, 'login_M.html')  # בדיקה אם נטענת תבנית דף ההתחברות
        
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn('You are not an active student.', messages)  # בדיקה אם מופיעה הודעת שגיאה

    def test_login_non_teacher_user(self):  # בדיקת התחברות של משתמש שאינו מורה
        self.user.user_type = 'student'  # שינוי סוג המשתמש ל'סטודנט'
        self.user.save()  
        
        response = self.client.post(self.login_url, {  
            'username': 'testteacher',
            'password': 'securepassword'
        })
        self.assertEqual(response.status_code, 200)  # בדיקה אם נשארים באותו עמוד
        self.assertTemplateUsed(response, 'login_M.html')  # בדיקה אם נטענת תבנית דף ההתחברות
        
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn('You are not an active student.', messages)  # בדיקה אם מופיעה הודעת שגיאה


#---------------------------------------------------------------------------------------------------------
User = get_user_model()  # קבלת מודל המשתמשים בפרויקט

class SignupTest(TestCase):  # מחלקת בדיקות עבור פונקציית ההרשמה Signup
    def setUp(self):  # פעולות הכנה לפני כל בדיקה
        self.client = Client()  # יצירת לקוח לדימוי בקשות HTTP
        self.signup_url = reverse('Signup')  # יצירת URL דינמי לדף ההרשמה
        self.user_data = {  # הגדרת נתוני משתמש לבדיקה
            'username': 'teststudent',
            'email': 'student@example.com',
            'password': 'securepassword',
            'phone_number': '1234567890',
            'id_number': '987654321',
            'specialization': 'Science'
        }

    def test_signup_success(self):  # בדיקת הרשמה מוצלחת
        response = self.client.post(self.signup_url, self.user_data)  # שליחת בקשת POST עם נתוני המשתמש
        self.assertEqual(response.status_code, 302)  # בדיקה אם יש הפניה (Redirect)
        self.assertRedirects(response, reverse('Studentpage'))  # בדיקה אם ההפניה היא לדף הסטודנט
        user = User.objects.get(username=self.user_data['username'])  # שליפת המשתמש מהמסד
        self.assertTrue(user)  # בדיקה אם המשתמש נוצר
        self.assertTrue(check_password(self.user_data['password'], user.password))  # בדיקה אם הסיסמה מוצפנת כראוי

    def test_duplicate_username(self):  # בדיקת הרשמה עם שם משתמש שכבר קיים
        User.objects.create(username='teststudent', email='another@example.com', password='securepassword')  # יצירת משתמש קיים
        response = self.client.post(self.signup_url, self.user_data)  # ניסיון להירשם עם אותו שם משתמש
        self.assertRedirects(response, reverse('login_S'))  # בדיקה אם ההפניה לדף ההתחברות
        messages = [m.message for m in get_messages(response.wsgi_request)]  # קריאת הודעות מערכת
        self.assertIn('Username already exists. Please log in.', messages)  # בדיקה אם מופיעה הודעת שגיאה

    def test_duplicate_email(self):  # בדיקת הרשמה עם אימייל שכבר קיים
        User.objects.create(username='anotheruser', email='student@example.com', password='securepassword')  # יצירת משתמש עם אותו אימייל
        response = self.client.post(self.signup_url, self.user_data)  # ניסיון להירשם עם אותו אימייל
        self.assertRedirects(response, reverse('login_S'))  # בדיקה אם ההפניה לדף ההתחברות
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn('Email already exists. Please log in.', messages)  # בדיקה אם מופיעה הודעת שגיאה

    def test_duplicate_id_number(self):  # בדיקת הרשמה עם מספר זהות שכבר קיים
        User.objects.create(username='anotheruser', email='another@example.com', password='securepassword', id_number='987654321')  # יצירת משתמש עם אותו מספר זהות
        response = self.client.post(self.signup_url, self.user_data)  # ניסיון להירשם עם אותו מספר זהות
        self.assertRedirects(response, reverse('login_S'))  # בדיקה אם ההפניה לדף ההתחברות
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn('id_number already exists. Please log in.', messages)  # בדיקה אם מופיעה הודעת שגיאה

    def test_get_request(self):  # בדיקה של בקשת GET
        response = self.client.get(self.signup_url)  # שליחת בקשת GET
        self.assertEqual(response.status_code, 200)  # בדיקה אם הדף נטען בהצלחה
        self.assertTemplateUsed(response, 'Sign_up.html')  # בדיקה אם התבנית הנכונה נטענת



#---------------------------------------------------------------------------------------------------------
class StudentLoginTest(TestCase):
    def setUp(self):
        # יצירת משתמש פעיל מסוג סטודנט
        self.student_user = User.objects.create_user(username='student1', password='testpass123')
        self.student_user.is_active = True
        self.student_user.user_type = 'student'  # שדה מותאם אישית לסוג המשתמש
        self.student_user.save()

        # יצירת משתמש לא פעיל
        self.inactive_user = User.objects.create_user(username='inactive_student', password='testpass123')
        self.inactive_user.is_active = False
        self.inactive_user.user_type = 'student'
        self.inactive_user.save()

        # יצירת קליינט לבדיקות HTTP
        self.client = Client()

    def test_login_success(self):
        # בדיקה שמשתמש פעיל מסוג סטודנט יכול להתחבר בהצלחה
        response = self.client.post(reverse('login_S'), {
            'username': 'student1',
            'password': 'testpass123'
        })
        self.assertRedirects(response, reverse('Studentpage'))  # לוודא שהמשתמש מופנה לדף הסטודנט

    def test_login_invalid_username(self):
        # בדיקה עם שם משתמש לא נכון
        response = self.client.post(reverse('login_S'), {
            'username': 'wrong_username',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 200)  # לוודא שהדף נטען מחדש
        self.assertContains(response, 'Invalid username or password.')  # לוודא שהודעת שגיאה מוצגת

    def test_login_invalid_password(self):
        # בדיקה עם סיסמה לא נכונה
        response = self.client.post(reverse('login_S'), {
            'username': 'student1',
            'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, 200)  # לוודא שהדף נטען מחדש
        self.assertContains(response, 'Invalid username or password.')  # לוודא שהודעת שגיאה מוצגת

    def test_login_inactive_user(self):
        # בדיקה עם משתמש לא פעיל
        response = self.client.post(reverse('login_S'), {
            'username': 'inactive_student',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 200)  # לוודא שהדף נטען מחדש
        self.assertContains(response, 'You are not an active student.')  # לוודא שהודעת שגיאה מוצגת

    def test_login_non_student_user(self):
        # יצירת משתמש שאינו סטודנט
        non_student_user = User.objects.create_user(username='teacher1', password='teacherpass123')
        non_student_user.is_active = True
        non_student_user.user_type = 'teacher'  # סוג שונה מסטודנט
        non_student_user.save()

        # בדיקה שמשתמש שאינו סטודנט לא יכול להתחבר
        response = self.client.post(reverse('login_S'), {
            'username': 'teacher1',
            'password': 'teacherpass123'
        })
        self.assertEqual(response.status_code, 200)  # לוודא שהדף נטען מחדש
        self.assertContains(response, 'You are not an active student.')  # לוודא שהודעת שגיאה מוצגת

#---------------------------------------------------------------------------------------------------------
class DeanLoginTest(TestCase):
    def setUp(self):
        # הגדרת משתמשים מורשים למבחן
        self.allowed_users = {
            'doha': 'doha1',
            'shaima': 'shaima11',
            'marwa': 'marwa1',
            'tmara': 'tmara1',
        }

        # יצירת קליינט לבדיקות HTTP
        self.client = Client()

    def test_login_success(self):
        # בדיקה שמשתמש מורשה יכול להתחבר בהצלחה
        response = self.client.post(reverse('Deanlogin'), {
            'username': 'doha',
            'password': 'doha1'
        })
        self.assertRedirects(response, reverse('dean_page'))  # לוודא שהמשתמש מופנה לדף הדיקן

    def test_login_invalid_username(self):
        # בדיקה עם שם משתמש לא נכון
        response = self.client.post(reverse('Deanlogin'), {
            'username': 'wrong_username',
            'password': 'doha1'
        })
        self.assertRedirects(response, reverse('Deanlogin'))  # לוודא שהמשתמש נשאר בדף ההתחברות
        self.assertContains(response, 'Invalid username or password')  # לוודא שהודעת שגיאה מוצגת

    def test_login_invalid_password(self):
        # בדיקה עם סיסמה לא נכונה
        response = self.client.post(reverse('Deanlogin'), {
            'username': 'doha',
            'password': 'wrongpass'
        })
        self.assertRedirects(response, reverse('Deanlogin'))  # לוודא שהמשתמש נשאר בדף ההתחברות
        self.assertContains(response, 'Invalid username or password')  # לוודא שהודעת שגיאה מוצגת

    def test_login_user_not_in_allowed_list(self):
        # בדיקה עם משתמש שאינו ברשימת המשתמשים המורשים
        response = self.client.post(reverse('Deanlogin'), {
            'username': 'unauthorized_user',
            'password': 'password123'
        })
        self.assertRedirects(response, reverse('Deanlogin'))  # לוודא שהמשתמש נשאר בדף ההתחברות
        self.assertContains(response, 'Invalid username or password')  # לוודא שהודעת שגיאה מוצגת

    def test_login_blank_fields(self):
        # בדיקה עם שדות ריקים
        response = self.client.post(reverse('Deanlogin'), {
            'username': '',
            'password': ''
        })
        self.assertRedirects(response, reverse('Deanlogin'))  # לוודא שהמשתמש נשאר בדף ההתחברות
        self.assertContains(response, 'Invalid username or password')  # לוודא שהודעת שגיאה מוצגת



#---------------------------------------------------------------------------------------------------------
User = get_user_model()  # השגת מודל המשתמשים המותאם

class PrivateDiaryTest(TestCase):  # מחלקה לבדיקה של פונקציית היומן הפרטי
    def setUp(self):  # פונקציה להרצת פעולות הכנה לפני כל בדיקה
        self.client = Client()  # יצירת לקוח לדימוי בקשות HTTP
        self.private_diary_url = reverse('private_Diary')  # יצירת ה-URL לבדיקה
        self.user = User.objects.create_user(username='testuser', password='testpassword')  # יצירת משתמש לבדיקה
        self.client.login(username='testuser', password='testpassword')  # התחברות עם המשתמש

    def test_private_diary_success(self):  # בדיקה של הוספת נתונים בהצלחה
        data = {
            'student_date[]': ['2025-01-01', '2025-01-02'],  # תאריכים לתלמידים
            'attendance_hours[]': ['2', '3'],  # שעות נוכחות
            'attendance_Topic[]': ['Math', 'Science'],  # נושאים שנלמדו
            'unit[]': ['Algebra', 'Physics'],  # יחידות לימוד
            'student_name[]': ['John Doe', 'Jane Doe'],  # שמות התלמידים
            'student_signature[]': ['sign1', 'sign2'],  # חתימות התלמידים
            'teacher_signature[]': ['tsign1', 'tsign2'],  # חתימות המורה
        }
        response = self.client.post(self.private_diary_url, data)  # שליחת בקשת POST עם הנתונים
        self.assertEqual(response.status_code, 302)  # בדיקה אם יש הפניה (Redirect)
        self.assertTrue(PrivateSession.objects.exists())  # בדיקה אם המפגשים נוצרו במסד הנתונים

    def test_private_diary_invalid_form(self):  # בדיקה של טופס לא תקין
        data = {
            'student_date[]': ['2025-01-01'],  # רק תאריך אחד וללא שאר הנתונים
        }
        response = self.client.post(self.private_diary_url, data)  # שליחת בקשת POST
        self.assertEqual(response.status_code, 200)  # בדיקה אם העמוד נטען שוב
        self.assertFalse(PrivateSession.objects.exists())  # בדיקה אם לא נוצרו רשומות חדשות

    def test_get_private_diary_page(self):  # בדיקה של טעינת הדף בבקשת GET
        response = self.client.get(self.private_diary_url)  # שליחת בקשת GET
        self.assertEqual(response.status_code, 200)  # בדיקה אם הדף נטען בהצלחה
        self.assertTemplateUsed(response, 'private_Diary.html')  # בדיקה אם התבנית הנכונה נטענת


#---------------------------------------------------------------------------------------------------------
class GroupRequestTest(TestCase):  # מחלקה לבדיקה של תהליך בקשת הקבוצה
    def setUp(self):  # פונקציה להרצת פעולות הכנה לפני כל בדיקה
        self.client = Client()  # יצירת לקוח לדימוי בקשות HTTP
        self.group_request_url = reverse('Group_request')  # יצירת ה-URL לבדיקה
        
    def test_group_request_success(self):  # בדיקה של יצירת בקשת קבוצה מוצלחת
        data = {  # יצירת נתוני טופס קבוצה
            'group_name': 'Test Group',
            'description': 'A test group description'
        }
        session_data = {  # יצירת נתוני טופס המפגשים
            'sessions-0-session_date': '2024-01-01',
            'sessions-0-duration': '2'
        }
        student_data = {  # יצירת נתוני טופס הסטודנטים
            'students-0-student_name': 'John Doe',
            'students-0-student_email': 'john@example.com'
        }
        
        form_data = {**data, **session_data, **student_data}  # שילוב כל הנתונים
        response = self.client.post(self.group_request_url, form_data)  # שליחת בקשת POST
        
        self.assertEqual(response.status_code, 302)  # בדיקה אם יש הפניה (Redirect)
        self.assertRedirects(response, reverse('Najah'))  # בדיקה אם ההפניה נכונה
        self.assertTrue(GroupRequest.objects.filter(group_name='Test Group').exists())  # בדיקה אם הבקשה נשמרה

    def test_group_request_invalid_form(self):  # בדיקה של טופס לא תקין
        response = self.client.post(self.group_request_url, {})  # שליחת בקשה עם נתונים ריקים
        self.assertEqual(response.status_code, 200)  # בדיקה שהדף נטען שוב ולא הייתה הפניה
        self.assertTemplateUsed(response, 'Group_request.html')  # בדיקה שהתבנית הנכונה בשימוש

    def test_get_request(self):  # בדיקה של בקשת GET
        response = self.client.get(self.group_request_url)  # שליחת בקשת GET
        self.assertEqual(response.status_code, 200)  # בדיקה אם הדף נטען בהצלחה
        self.assertTemplateUsed(response, 'Group_request.html')  # בדיקה אם התבנית הנכונה נטענת



#---------------------------------------------------------------------------------------------------------
class DeanRequestsViewTest(TestCase):  # מחלקת הבדיקה
    def setUp(self):  # פונקציה להרצת פעולות הכנה לפני כל בדיקה
        self.client = Client()  # יצירת לקוח לדימוי בקשות HTTP
        self.url = reverse("dean_requests")  # יצירת ה-URL לבדיקה

        # יצירת בקשה אישית לבדיקה
        self.personal_request = PersonalRequest.objects.create(
            id_number="123456789", status="ממתין"
        )

        # יצירת בקשת קבוצה לבדיקה
        self.group_request = GroupRequest.objects.create(
            contact_id="123456789", status="ממתין"
        )

    def test_approve_personal_request(self):  # בדיקה של אישור בקשה אישית
        response = self.client.post(self.url, {"request_id": "123456789", "action": "approve"})
        self.personal_request.refresh_from_db()  # רענון הנתונים מהמסד
        self.assertEqual(self.personal_request.status, "מַאֲשָׁר")  # בדיקה אם הסטטוס עודכן נכון

    def test_reject_personal_request(self):  # בדיקה של דחיית בקשה אישית
        response = self.client.post(self.url, {"request_id": "123456789", "action": "reject"})
        self.personal_request.refresh_from_db()
        self.assertEqual(self.personal_request.status, "דָּחָה")

    def test_approve_group_request(self):  # בדיקה של אישור בקשת קבוצה
        response = self.client.post(self.url, {"request_id": "123456789", "action": "approve"})
        self.group_request.refresh_from_db()
        self.assertEqual(self.group_request.status, "מַאֲשָׁר")

    def test_reject_group_request(self):  # בדיקה של דחיית בקשת קבוצה
        response = self.client.post(self.url, {"request_id": "123456789", "action": "reject"})
        self.group_request.refresh_from_db()
        self.assertEqual(self.group_request.status, "דָּחָה")

    def test_request_not_found(self):  # בדיקה של ניסיון עדכון בקשה שלא קיימת
        response = self.client.post(self.url, {"request_id": "000000000", "action": "approve"})
        self.assertContains(response, "לא נמצא בקשה עם מספר זהות זה", status_code=200)



#---------------------------------------------------------------------------------------------------------
User = get_user_model()  # קבלת מודל המשתמשים המותאם
class UpdateUserTest(TestCase):  # מחלקת בדיקה לעדכון משתמשים
    def setUp(self):  # פונקציה שמריצה פעולות הכנה לפני כל בדיקה
        self.client = Client()  # יצירת לקוח לדימוי בקשות HTTP
        self.user = User.objects.create(  # יצירת משתמש לבדיקה
            username='olduser',
            email='old@example.com',
            phone_number='1234567890',
            id_number='987654321',
            specialization='Physics'
        )
        self.update_url = reverse('update_user', args=[self.user.id])  # יצירת ה-URL לבדיקה

    def test_update_user_success(self):  # בדיקה לעדכון מוצלח של משתמש
        new_data = {  # נתונים מעודכנים לשליחה
            'username': 'newuser',
            'email': 'new@example.com',
            'phone_number': '0987654321',
            'id_number': '123456789',
            'specialization': 'Mathematics'
        }
        response = self.client.post(self.update_url, new_data)  # שליחת בקשת POST עם הנתונים החדשים
        self.user.refresh_from_db()  # רענון המשתמש מהמסד
        self.assertEqual(self.user.username, 'newuser')  # בדיקה אם שם המשתמש התעדכן
        self.assertEqual(self.user.email, 'new@example.com')  # בדיקה אם האימייל התעדכן
        self.assertEqual(self.user.phone_number, '0987654321')  # בדיקה אם מספר הטלפון התעדכן
        self.assertEqual(self.user.id_number, '123456789')  # בדיקה אם מספר הזהות התעדכן
        self.assertEqual(self.user.specialization, 'Mathematics')  # בדיקה אם ההתמחות התעדכנה
        self.assertRedirects(response, reverse('manage_users'))  # בדיקה אם המשתמש הופנה לדף הניהול

    def test_update_user_get_request(self):  # בדיקה לשליחת בקשת GET אסורה
        response = self.client.get(self.update_url)  # שליחת בקשת GET
        self.assertEqual(response.status_code, 403)  # בדיקה אם מוחזר קוד 403 (Forbidden)
        self.assertEqual(response.content.decode(), "אסור")  # בדיקה אם מוחזרת ההודעה הנכונה


#---------------------------------------------------------------------------------------------------------
class UpdateTimeTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.personal_request = PersonalRequest.objects.create(
            full_name="Test User",
            id_number="123456789",
            course_name="Math",
            student_day="Monday"
        )
        self.schedule = Schedule.objects.create(
            request=self.personal_request,
            start_time="08:00",
            end_time="10:00"
        )
        self.update_url = reverse('update_time', args=[self.personal_request.id])

    def test_update_time_success(self):
        response = self.client.post(self.update_url, {
            'full_name': 'Updated User',
            'id_number': '987654321',
            'course_name': 'Physics',
            'student_day': 'Tuesday',
            'start_time': '09:00',
            'end_time': '11:00'
        })
        
        self.personal_request.refresh_from_db()
        self.schedule.refresh_from_db()
        
        self.assertEqual(self.personal_request.full_name, 'Updated User')
        self.assertEqual(self.personal_request.id_number, '987654321')
        self.assertEqual(self.personal_request.course_name, 'Physics')
        self.assertEqual(self.personal_request.student_day, 'Tuesday')
        self.assertEqual(self.schedule.start_time, '09:00')
        self.assertEqual(self.schedule.end_time, '11:00')
        
        self.assertEqual(response.status_code, 200)

    def test_update_time_forbidden_get_request(self):
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.content.decode(), "אסור")
#---------------------------------------------------------------------------------------------------------
class AdminDashboardTest(TestCase):
    def setUp(self):
        self.client = Client()  # יצירת לקוח לביצוע בקשות HTTP
        self.url = reverse('admin_dashboard')  # יצירת ה-URL של דף ניהול המערכת

        # יצירת רשומות לבדיקה
        self.diary = PrivateDiary.objects.create(title='Test Diary')
        self.group = DiaryGroup.objects.create(name='Test Group')
        self.session = PrivateSession.objects.create(private=self.diary, student_name='Student A')
        self.student = DiaryStudent.objects.create(name='Student B')

    def test_admin_dashboard_view(self):
        response = self.client.get(self.url)  # שליחת בקשת GET
        self.assertEqual(response.status_code, 200)  # בדיקה שהדף נטען בהצלחה
        self.assertTemplateUsed(response, 'admin_dashboard.html')  # בדיקה שהתבנית הנכונה בשימוש

        # בדיקה שהנתונים הועברו לתבנית
        self.assertIn('diaries', response.context)
        self.assertIn('sessions', response.context)
        self.assertIn('groups', response.context)
        self.assertIn('students', response.context)

        # בדיקה שהנתונים קיימים
        self.assertEqual(response.context['diaries'].count(), 1)
        self.assertEqual(response.context['groups'].count(), 1)
        self.assertEqual(response.context['sessions'].count(), 1)
        self.assertEqual(response.context['students'].count(), 1)
#---------------------------------------------------------------------------------------------------------
# Create your tests here.
def Group_Diary(request):
    # בדיקה אם הבקשה היא מסוג POST לצורך טיפול בנתונים שנשלחו מהטופס
    if request.method == 'POST':
        # יצירת טופס קבוצתי עם הנתונים שנשלחו מהמשתמש
        group_form = DiaryGroupForm(request.POST)
        
        # בדיקה אם הנתונים בטופס תקינים
        if group_form.is_valid():
            # שמירת נתוני הקבוצה אם הטופס תקין
            group = group_form.save()
            
            # יצירת רשימה לאחסון פרטי התלמידים
            students = []
            
            # שליפת הנתונים מהבקשה (שמות התלמידים, תאריכים ושעות)
            student_names = request.POST.getlist('student_name[]')
            attendance_dates = request.POST.getlist('student_date[]')
            attendance_hours_list = request.POST.getlist('student_hours[]')

            # חישוב האורך המקסימלי של הרשימות כדי למנוע שגיאות בעת טיפול ברשימות
            max_length = max(len(student_names), len(attendance_dates), len(attendance_hours_list))

            # לולאה לעיבוד הערכים לפי האורך המקסימלי
            for i in range(max_length):
                # שליפת הערכים מהרשימות תוך בדיקה שהם בטווח
                student_name = student_names[i] if i < len(student_names) else None
                student_date = attendance_dates[i] if i < len(attendance_dates) else None
                student_hours = attendance_hours_list[i] if i < len(attendance_hours_list) else None
                
                # בדיקה שכל הערכים קיימים לפני הוספתם
                if student_name and student_date and student_hours:
                    try:
                        # יצירת אובייקט תלמיד והוספתו לרשימה
                        students.append(DiaryStudent(
                            group=group,
                            student_name=student_name,
                            student_date=student_date,
                            student_hours=int(student_hours)  # המרת השעות למספר שלם
                        ))
                    except Exception as e:
                        # הדפסת שגיאה אם קרתה בזמן עיבוד נתוני התלמיד
                        print(f"Error adding student data: {e}")
            
            # שמירת כל רשומות התלמידים בבת אחת אם יש נתונים
            if students:
                try:
                    DiaryStudent.objects.bulk_create(students)
                except Exception as e:
                    # הדפסת שגיאה אם קרתה במהלך השמירה
                    print(f"Error saving students: {e}")

            # הפניה לעמוד המבוקש לאחר סיום מוצלח של הפעולה
            return redirect('Najah')
        else:
            # הדפסת שגיאות אם הטופס לא תקין
            print("Form errors:", group_form.errors)
    else:
        # אם הבקשה היא GET, יוצרים טופס ריק
        group_form = DiaryGroupForm()

    # הצגת הדף עם הטופס (לבקשת GET או במקרה של שגיאות ב-POST)
    return render(request, 'Group_Diary.html', {'group_form': group_form})



#---------------------------------------------------------------------------------------------------------
class PrivateRequestTest(TestCase):
    def setUp(self):
        # יצירת אובייקט Client לביצוע הבקשות
        self.client = Client()
        # הגדרת ה-URL שבו נבדוק את הבקשות
        self.url = reverse('private_request')  # שים לב שצריך להתאים את השם לפי ה-URL שלך

    def test_get_request_returns_form(self):
        # ביצוע בקשת GET כדי לבדוק אם מתקבל הטופס
        response = self.client.get(self.url)
        # בדיקה שהסטטוס של התגובה הוא 200 (הבקשה הצליחה)
        self.assertEqual(response.status_code, 200)
        # בדיקה שהטופס המתקבל הוא אובייקט מסוג PersonalRequestForm
        self.assertIsInstance(response.context['private_form'], PersonalRequestForm)

    def test_post_valid_data(self):
        # הכנת נתונים תקינים לשליחה בטופס
        data = {
            'request_type': 'Private Request Test',  # סוג הבקשה
            'student_day[]': ['Monday', 'Tuesday'],  # ימים של התלמידים
            'start_time[]': ['10:00', '14:00'],  # זמני התחלה
            'end_time[]': ['12:00', '16:00'],  # זמני סיום
        }
        # ביצוע בקשת POST עם הנתונים שהכנו
        response = self.client.post(self.url, data)
        # בדיקה שהסטטוס של התגובה הוא 302 (הפניה לעמוד אחר)
        self.assertEqual(response.status_code, 302)  # הפניה ל-'Najah'
        # בדיקה שהבקשה נשמרה ב-Django
        self.assertTrue(PersonalRequest.objects.filter(request_type='Private Request Test').exists())
        # שליפת הבקשה שנשמרה
        private = PersonalRequest.objects.get(request_type='Private Request Test')
        # שליפת לוחות הזמנים הקשורים לבקשה
        schedules = Schedule.objects.filter(private=private)
        # בדיקה שיש בדיוק שני לוחות זמנים
        self.assertEqual(schedules.count(), 2)
        # בדיקה שהיום של לוח הזמנים הראשון הוא 'Monday'
        self.assertEqual(schedules[0].student_day, 'Monday')
        # בדיקה שזמן הסיום של לוח הזמנים השני הוא '16:00'
        self.assertEqual(schedules[1].end_time, '16:00')

    def test_post_partial_data(self):
        # הכנת נתונים לא שלמים לשליחה
        data = {
            'request_type': 'Partial Request',  # סוג הבקשה
            'student_day[]': ['Monday'],  # יום של התלמיד
            'start_time[]': ['10:00'],  # זמן התחלה
            # חסר נתון 'end_time[]'
        }
        # ביצוע בקשת POST עם הנתונים החלקיים
        response = self.client.post(self.url, data)
        # בדיקה שהסטטוס של התגובה הוא 302 (הפניה לעמוד אחר)
        self.assertEqual(response.status_code, 302)  # הפניה ל-'Najah'
        # שליפת הבקשה שנשמרה
        private = PersonalRequest.objects.get(request_type='Partial Request')
        # שליפת לוחות הזמנים הקשורים לבקשה
        schedules = Schedule.objects.filter(private=private)
        # בדיקה שאין לוחות זמנים שנשמרו
        self.assertEqual(schedules.count(), 0)

    def test_post_invalid_data(self):
        # הכנת נתונים לא תקינים (סוג בקשה ריק)
        data = {
            'request_type': '',  # סוג בקשה ריק
            'student_day[]': ['Monday'],  # יום של התלמיד
            'start_time[]': ['10:00'],  # זמן התחלה
            'end_time[]': ['12:00'],  # זמן סיום
        }
        # ביצוע בקשת POST עם הנתונים הלא תקינים
        response = self.client.post(self.url, data)
        # בדיקה שהסטטוס של התגובה הוא 200 (הבקשה לא התקבלה בגלל שגיאה)
        self.assertEqual(response.status_code, 200)  # שגיאות בטופס
        # בדיקה שאין בקשה שנשמרה
        self.assertFalse(PersonalRequest.objects.exists())
        # בדיקה שאין לוחות זמנים שנשמרו
        self.assertFalse(Schedule.objects.exists())



#---------------------------------------------------------------------------------------------------------
class DeleteRequestViewsTest(TestCase):
    def setUp(self):
        # יצירת אובייקט Client לביצוע הבקשות
        self.client = Client()

        # יצירת אובייקטים של בקשות קבוצתיות ובקשות אישיות לצורך הבדיקות
        self.group_request = GroupRequest.objects.create(name="Group Test Request")
        self.private_request = PersonalRequest.objects.create(request_type="Private Test Request")

        # הגדרת ה-URLs עבור כל פעולה
        self.group_delete_url = reverse('delete_group_request', kwargs={'request_id': self.group_request.id})
        self.private_delete_url = reverse('delete_private_request', kwargs={'request_id': self.private_request.id})

    def test_delete_group_request_view_get(self):
        # ביצוע בקשת GET לבדוק אם הטופס מוצג נכון
        response = self.client.get(self.group_delete_url)
        # בדיקה שהסטטוס של התגובה הוא 200 (הבקשה הצליחה)
        self.assertEqual(response.status_code, 200)
        # בדיקה שהבקשה מוצגת בדף עם השם הנכון
        self.assertContains(response, 'Group Test Request')

    def test_delete_group_request_view_post(self):
        # ביצוע בקשת POST למחיקת הבקשה
        response = self.client.post(self.group_delete_url)
        # בדיקה שהסטטוס של התגובה הוא 302 (הפניה ל-'Studentpage')
        self.assertEqual(response.status_code, 302)
        # בדיקה שהבקשה נמחקה מהמסד נתונים
        self.assertFalse(GroupRequest.objects.filter(id=self.group_request.id).exists())

    def test_delete_private_request_view_get(self):
        # ביצוע בקשת GET לבדוק אם הטופס מוצג נכון
        response = self.client.get(self.private_delete_url)
        # בדיקה שהסטטוס של התגובה הוא 200 (הבקשה הצליחה)
        self.assertEqual(response.status_code, 200)
        # בדיקה שהבקשה מוצגת בדף עם השם הנכון
        self.assertContains(response, 'Private Test Request')

    def test_delete_private_request_view_post(self):
        # ביצוע בקשת POST למחיקת הבקשה
        response = self.client.post(self.private_delete_url)
        # בדיקה שהסטטוס של התגובה הוא 302 (הפניה ל-'Studentpage')
        self.assertEqual(response.status_code, 302)
        # בדיקה שהבקשה נמחקה מהמסד נתונים
        self.assertFalse(PersonalRequest.objects.filter(id=self.private_request.id).exists())

#---------------------------------------------------------------------------------------------------------


class ManageUsersViewTest(TestCase):
    def setUp(self):
        # יצירת אובייקט Client לביצוע הבקשות
        self.client = Client()

        # יצירת משתמשים לצורך הבדיקה
        self.user1 = User.objects.create_user(username="user1", password="password123")
        self.user2 = User.objects.create_user(username="user2", password="password123")

        # הגדרת ה-URL עבור ניהול המשתמשים
        self.url = reverse('manage_users')  # יש להתאים את השם של ה-URL לפי השם שלך

    def test_manage_users_view_get(self):
        # ביצוע בקשת GET לבדוק אם המשתמשים מוצגים כראוי
        response = self.client.get(self.url)
        # בדיקה שהסטטוס של התגובה הוא 200 (הבקשה הצליחה)
        self.assertEqual(response.status_code, 200)
        # בדיקה שהמשתמשים שנוצרים קיימים בתגובה
        self.assertContains(response, 'user1')  # שם המשתמש הראשון
        self.assertContains(response, 'user2')  # שם המשתמש השני
        # בדיקה שהמשתמשים הוכנסו להקשר
        self.assertEqual(len(response.context['users']), 2)

    def test_manage_users_view_no_users(self):
        # מחיקת המשתמשים לצורך בדיקה שאין משתמשים
        User.objects.all().delete()
        # ביצוע בקשת GET לבדוק אם אין משתמשים
        response = self.client.get(self.url)
        # בדיקה שהסטטוס של התגובה הוא 200 (הבקשה הצליחה)
        self.assertEqual(response.status_code, 200)
        # בדיקה שההקשר לא מכיל משתמשים
        self.assertEqual(len(response.context['users']), 0)


#---------------------------------------------------------------------------------------------------------


class SystemTeacherViewTest(TestCase):
    def setUp(self):
        # יצירת אובייקט Client לביצוע הבקשות
        self.client = Client()

        # יצירת בקשות אישיות וקבוצתיות לצורך הבדיקה
        self.personal_request = PersonalRequest.objects.create(request_type="Personal Test Request")
        self.group_request = GroupRequest.objects.create(name="Group Test Request")
        
        # יצירת אופציות מפגש/סטודנטים בקשות קבוצתיות
        self.group_request.session_options.create(option_name="Test Session")
        self.group_request.students.create(student_name="Test Student")

        # הגדרת ה-URL עבור הצפיה במערכת
        self.url = reverse('system_Teacher')  # יש להתאים את השם של ה-URL לפי השם שלך

    def test_system_teacher_view_get(self):
        # ביצוע בקשת GET כדי לבדוק אם כל המידע מוצג כראוי
        response = self.client.get(self.url)
        # בדיקה שהסטטוס של התגובה הוא 200 (הבקשה הצליחה)
        self.assertEqual(response.status_code, 200)
        # בדיקה שהבקשות האישיות קיימות בתגובה
        self.assertContains(response, 'Personal Test Request')
        # בדיקה שהבקשות הקבוצתיות קיימות בתגובה
        self.assertContains(response, 'Group Test Request')
        # בדיקה שנעשה prefetching של 'Schedules' עבור הבקשות האישיות
        self.assertTrue('personal_requests' in response.context)
        # בדיקה שנעשה prefetching של 'session_options' ו-'students' עבור הבקשות הקבוצתיות
        self.assertTrue('group_requests' in response.context)

    def test_system_teacher_view_no_requests(self):
        # מחיקת כל הבקשות לצורך בדיקה שאין בקשות
        PersonalRequest.objects.all().delete()
        GroupRequest.objects.all().delete()
        # ביצוע בקשת GET לבדוק אם אין בקשות
        response = self.client.get(self.url)
        # בדיקה שהסטטוס של התגובה הוא 200 (הבקשה הצליחה)
        self.assertEqual(response.status_code, 200)
        # בדיקה שההקשר לא מכיל בקשות אישיות
        self.assertEqual(len(response.context['personal_requests']), 0)
        # בדיקה שההקשר לא מכיל בקשות קבוצתיות
        self.assertEqual(len(response.context['group_requests']), 0)


#---------------------------------------------------------------------------------------------------------


class SystemStudentViewTest(TestCase):
    def setUp(self):
        # יצירת אובייקט Client לביצוע הבקשות
        self.client = Client()

        # יצירת בקשות אישיות וקבוצתיות לצורך הבדיקה
        self.personal_request = PersonalRequest.objects.create(request_type="Personal Test Request")
        self.group_request = GroupRequest.objects.create(name="Group Test Request")
        
        # יצירת אופציות מפגש/סטודנטים בקשות קבוצתיות
        self.group_request.session_options.create(option_name="Test Session")
        self.group_request.students.create(student_name="Test Student")

        # הגדרת ה-URL עבור הצפיה במערכת הסטודנט
        self.url = reverse('system_Student')  # יש להתאים את השם של ה-URL לפי השם שלך

    def test_system_student_view_get(self):
        # ביצוע בקשת GET כדי לבדוק אם כל המידע מוצג כראוי
        response = self.client.get(self.url)
        # בדיקה שהסטטוס של התגובה הוא 200 (הבקשה הצליחה)
        self.assertEqual(response.status_code, 200)
        # בדיקה שהבקשות האישיות קיימות בתגובה
        self.assertContains(response, 'Personal Test Request')
        # בדיקה שהבקשות הקבוצתיות קיימות בתגובה
        self.assertContains(response, 'Group Test Request')
        # בדיקה שנעשה prefetching של 'Schedules' עבור הבקשות האישיות
        self.assertTrue('personal_requests' in response.context)
        # בדיקה שנעשה prefetching של 'session_options' ו-'students' עבור הבקשות הקבוצתיות
        self.assertTrue('group_requests' in response.context)

    def test_system_student_view_no_requests(self):
        # מחיקת כל הבקשות לצורך בדיקה שאין בקשות
        PersonalRequest.objects.all().delete()
        GroupRequest.objects.all().delete()
        # ביצוע בקשת GET לבדוק אם אין בקשות
        response = self.client.get(self.url)
        # בדיקה שהסטטוס של התגובה הוא 200 (הבקשה הצליחה)
        self.assertEqual(response.status_code, 200)
        # בדיקה שההקשר לא מכיל בקשות אישיות
        self.assertEqual(len(response.context['personal_requests']), 0)
        # בדיקה שההקשר לא מכיל בקשות קבוצתיות
        self.assertEqual(len(response.context['group_requests']), 0)



#---------------------------------------------------------------------------------------------------------
class UpdateTimeGViewTest(TestCase):
    def setUp(self):
        # יצירת אובייקט Client לביצוע הבקשות
        self.client = Client()

        # יצירת משתמש לצורך הבדיקה
        self.user = User.objects.create_user(username="testuser", password="password123")

        # יצירת בקשת קבוצתית עם אפשרות מפגש
        self.group_request = GroupRequest.objects.create(name="Test Group Request", contact_name="Test Contact", contact_id="123", course_name="Test Course", day="Monday")
        self.group_option = GroupOption.objects.create(group=self.group_request, start_time="09:00", end_time="11:00")

        # הגדרת ה-URL עבור עדכון שעות בקשה קבוצתית
        self.url = reverse('update_timeG', args=[self.group_request.id])  # יש להתאים את השם של ה-URL לפי השם שלך

    def test_update_timeG_post_valid(self):
        # התחברות עם המשתמש שנוצר
        self.client.login(username='testuser', password='password123')

        # ביצוע בקשת POST לעדכון שעות בקשה קבוצתית
        response = self.client.post(self.url, {
            'contact_name': 'Updated Contact',
            'contact_id': '456',
            'course_name': 'Updated Course',
            'day': 'Tuesday',
            'start_time': '10:00',
            'end_time': '12:00'
        })
        # בדיקה שהסטטוס של התגובה הוא 200 (הבקשה הצליחה)
        self.assertEqual(response.status_code, 200)
        
        # בדיקה שהשינויים עודכנו כראוי
        self.group_request.refresh_from_db()
        self.group_option.refresh_from_db()
        self.assertEqual(self.group_request.contact_name, 'Updated Contact')
        self.assertEqual(self.group_request.contact_id, '456')
        self.assertEqual(self.group_request.course_name, 'Updated Course')
        self.assertEqual(self.group_request.day, 'Tuesday')
        self.assertEqual(self.group_option.start_time, '10:00')
        self.assertEqual(self.group_option.end_time, '12:00')

    def test_update_timeG_post_no_group_option(self):
        # מחיקת אפשרות המפגש כדי לבדוק את המקרה שבו אין אפשרות
        self.group_option.delete()

        # ביצוע בקשת POST לעדכון שעות בקשה קבוצתית
        response = self.client.post(self.url, {
            'contact_name': 'Updated Contact',
            'contact_id': '456',
            'course_name': 'Updated Course',
            'day': 'Tuesday',
            'start_time': '10:00',
            'end_time': '12:00'
        })
        # בדיקה שהסטטוס של התגובה הוא 403 (אסור)
        self.assertEqual(response.status_code, 403)
        self.assertContains(response, "אסור")

    def test_update_timeG_get_not_allowed(self):
        # ביצוע בקשת GET במקום POST
        response = self.client.get(self.url)
        # בדיקה שהסטטוס של התגובה הוא 403 (אסור)
        self.assertEqual(response.status_code, 403)
        self.assertContains(response, "אסור")



#---------------------------------------------------------------------------------------------------------
class DeleteUserViewTest(TestCase):
    def setUp(self):
        # יצירת אובייקט Client לביצוע הבקשות
        self.client = Client()

        # יצירת משתמש לצורך הבדיקה
        self.user = User.objects.create_user(username="testuser", password="password123")

        # יצירת משתמש אחר לבדיקת המחיקה
        self.user_to_delete = User.objects.create_user(username="testuser2", password="password456")

        # הגדרת ה-URL עבור מחיקת המשתמש
        self.url = reverse('delete_user', args=[self.user_to_delete.id])  # יש להתאים את השם של ה-URL לפי השם שלך

    def test_delete_user_post_valid(self):
        # התחברות עם המשתמש שנוצר
        self.client.login(username='testuser', password='password123')

        # ביצוע בקשת POST למחיקת המשתמש
        response = self.client.post(self.url)

        # בדיקה שהסטטוס של התגובה הוא 302 (מעבר לדף אחר)
        self.assertEqual(response.status_code, 302)
        # בדיקה שהמשתמש נמחק מהמאגר
        self.assertFalse(User.objects.filter(id=self.user_to_delete.id).exists())

    def test_delete_user_get_not_allowed(self):
        # ביצוע בקשת GET במקום POST למחיקת משתמש
        response = self.client.get(self.url)
        # בדיקה שהסטטוס של התגובה הוא 405 (שיטה לא מורשית)
        self.assertEqual(response.status_code, 405)
        # בדיקה שהתוכן לא מכיל הודעה לא מורשית
        self.assertNotContains(response, 'המשתמש לא נמחק')

    def test_delete_user_not_logged_in(self):
        # ביצוע בקשה למחיקת משתמש ללא התחברות
        response = self.client.post(self.url)
        # בדיקה שהסטטוס של התגובה הוא 302 (מעבר לדף כניסה)
        self.assertEqual(response.status_code, 302)
        # בדיקה שהמערכת מפנה את המשתמש לדף ההתחברות
        self.assertRedirects(response, '/login/?next=' + self.url)



#---------------------------------------------------------------------------------------------------------
class DiaryViewsTest(TestCase):
    def setUp(self):
        # יצירת אובייקט משתמש לצורך הבדיקות
        self.user = User.objects.create_user(username="testuser", password="password123")

        # יצירת יומן פרטי
        self.private_diary = PrivateDiary.objects.create(title="Test Private Diary", user=self.user)
        
        # יצירת ישיבות קשורות ליומן הפרטי
        self.session1 = Session.objects.create(diary=self.private_diary, content="Session 1 Content")
        self.session2 = Session.objects.create(diary=self.private_diary, content="Session 2 Content")

        # יצירת יומן קבוצתי
        self.group_diary = DiaryGroup.objects.create(title="Test Group Diary")
        
        # יצירת תלמידים בקבוצת היום-יומיים
        self.student1 = User.objects.create_user(username="student1", password="password1")
        self.student2 = User.objects.create_user(username="student2", password="password2")
        self.group_diary.students.add(self.student1, self.student2)

        # הגדרת ה-URLs עבור הצפייה ביומני פרטי וקבוצתי
        self.private_diary_url = reverse('private_diary_view', args=[self.private_diary.id])  # יש להתאים את השם של ה-URL לפי השם שלך
        self.group_diary_url = reverse('group_diary_view', args=[self.group_diary.id])  # יש להתאים את השם של ה-URL לפי השם שלך

    def test_private_diary_view(self):
        # התחברות עם המשתמש שנוצר
        self.client.login(username='testuser', password='password123')

        # ביצוע בקשת GET עבור צפייה ביומן פרטי
        response = self.client.get(self.private_diary_url)

        # בדיקה שהסטטוס של התגובה הוא 200 (הבקשה הצליחה)
        self.assertEqual(response.status_code, 200)

        # בדיקה שהתוכן של יומן פרטי מוצג
        self.assertContains(response, "Test Private Diary")
        self.assertContains(response, "Session 1 Content")
        self.assertContains(response, "Session 2 Content")

    def test_group_diary_view(self):
        # התחברות עם המשתמש שנוצר
        self.client.login(username='testuser', password='password123')

        # ביצוע בקשת GET עבור צפייה ביומן קבוצתי
        response = self.client.get(self.group_diary_url)

        # בדיקה שהסטטוס של התגובה הוא 200 (הבקשה הצליחה)
        self.assertEqual(response.status_code, 200)

        # בדיקה שהתוכן של יומן קבוצתי מוצג
        self.assertContains(response, "Test Group Diary")
        self.assertContains(response, "student1")
        self.assertContains(response, "student2")

    def test_private_diary_view_not_found(self):
        # ביצוע בקשת GET עבור יומן פרטי שלא קיים
        response = self.client.get(reverse('private_diary_view', args=[9999]))  # ID לא קיים

        # בדיקה שהסטטוס של התגובה הוא 404 (לא נמצא)
        self.assertEqual(response.status_code, 404)

    def test_group_diary_view_not_found(self):
        # ביצוע בקשת GET עבור יומן קבוצתי שלא קיים
        response = self.client.get(reverse('group_diary_view', args=[9999]))  # ID לא קיים

        # בדיקה שהסטטוס של התגובה הוא 404 (לא נמצא)
        self.assertEqual(response.status_code, 404)
