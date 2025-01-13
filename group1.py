import re

def validate_course_data(data):
    # בדיקה אם כל השדות הדרושים הוזנו
    required_fields = ['course_name', 'course_number', 'department', 'campus', 'group_priority']
    for field in required_fields:
        if field not in data or not data[field]:
            return f"יש למלא את כל השדות הדרושים: {field}"

    # בדיקה אם מספר הקורס הוא מספר תקני
    if not data['course_number'].isdigit():
        return "מספר הקורס חייב להיות רק מספרים"

    # בדיקה אם קמפוס נבחר
    if data['campus'] not in ['ashdod', 'beersheba']:
        return "יש לבחור קמפוס תקני"

    # בדיקה אם העדיפות של הקבוצה תקינה
    if data['group_priority'] not in ['frontal', 'zoom']:
        return "יש לבחור עדיפות תקינה עבור הקבוצה"
    
    # בדיקות נוספות
    result = validate_contact_info(data)
    if result != "הקלט תקין":
        return result

    return "הקלט תקין"


def validate_contact_info(data):
    # בדיקה אם כל השדות עבור איש קשר מטעם הסטודנטים הוזנו בצורה תקינה
    if 'full_name' not in data or not data['full_name']:
        return "יש למלא את שם מלא של איש הקשר"

    if 'id_number' not in data or not data['id_number'] or len(data['id_number']) != 9 or not data['id_number'].isdigit():
        return "תעודת הזהות חייבת להיות 9 ספרות"

    if 'phone' not in data or not data['phone'] or len(data['phone']) != 10 or not data['phone'].isdigit() or not data['phone'].startswith("05"):
        return "מספר הטלפון חייב להיות 10 ספרות ולתחום ב-05"

    if 'email' not in data or not data['email'] or not re.match(r"[^@]+@[^@]+\.[^@]+", data['email']):
        return "כתובת המייל אינה תקינה"

    if 'department' not in data or not data['department']:
        return "יש למלא את המחלקה"

    # אם כל הבדיקות תקינות
    return "הקלט תקין"


def check_students(data):
    if len(data['students']) < 7:
        return "הדרישה היא לפחות 7 סטודנטים"
    else:
        return "הכמות תקינה"


# דוגמת קלט שנכנס
data = {
    'course_name': 'מתמטיקה 1',
    'course_number': '101',
    'department': 'הנדסה',
    'campus': 'ashdod',
    'group_priority': 'frontal',
    'students': ['סטודנט 1', 'סטודנט 2', 'סטודנט 3', 'סטודנט 4', 'סטודנט 5', 'סטודנט 6', 'סטודנט 7'],
    'times': [
        {'day': 'sunday', 'start': '08:00', 'end': '10:00'},
        {'day': 'monday', 'start': '10:00', 'end': '12:00'},
        {'day': 'wednesday', 'start': '14:00', 'end': '16:00'}
    ],
    'full_name': 'יוסי כהן',
    'id_number': '123456789',
    'phone': '0501234567',
    'email': 'yossi@example.com'
}

# קריאה לפונקציה
result = validate_course_data(data)
print(result)

