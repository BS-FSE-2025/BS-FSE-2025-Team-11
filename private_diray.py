import re
from datetime import datetime

def validate_mentor_data(data):
    # בדיקה אם שם המתגבר הוזן
    if not data.get('mentor_name'):
        return "שם המתגבר לא הוזן."

    # בדיקה אם תעודת זהות תקינה (9 ספרות)
    id_number = data.get('id_number')
    if not id_number or len(id_number) != 9 or not id_number.isdigit():
        return "תעודת זהות לא תקינה. יש להזין 9 ספרות."

    # בדיקה אם שם הקורס הוזן
    if not data.get('course_name'):
        return "שם הקורס לא הוזן."

    # בדיקה אם מחלקה הוזנה
    if not data.get('department'):
        return "המחלקה לא הוזנה."

    # בדיקה אם תאריכים תקינים
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    try:
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        return "תאריכים לא תקינים."

    if start_date_obj > end_date_obj:
        return "תאריך הסיום לא יכול להיות לפני תאריך ההתחלה."

    # בדיקה אם סה"כ השעות תקין
    total_hours = data.get('total_hours')
    if not total_hours or total_hours <= 0:
        return "יש להזין סך הכל שעות חיוביות."

    return "הקלט תקין"

def validate_row_data(row_data):
    # בדיקה אם התאריך תקין
    try:
        datetime.strptime(row_data.get('date'), '%Y-%m-%d')
    except ValueError:
        return "התאריך לא תקין."

    # בדיקה אם מספר שעות תקין
    if not row_data.get('hours') or row_data.get('hours') <= 0:
        return "מספר השעות לא תקין."

    # בדיקה אם נושא התגבור הוזן
    if not row_data.get('subject'):
        return "נושא התגבור לא הוזן."

    # בדיקה אם שם הסטודנט הוזן
    if not row_data.get('student_name'):
        return "שם הסטודנט לא הוזן."

    # בדיקה אם חתימות הוזנו
    if not row_data.get('signature_student') or not row_data.get('signature_mentor'):
        return "יש להזין את חתימות הסטודנט והמתגבר."

    return "הקלט תקין"

def validate_approval_data(approval_data):
    # בדיקה אם תאריך האישור תקין
    try:
        datetime.strptime(approval_data.get('approval_date'), '%Y-%m-%d')
    except ValueError:
        return "תאריך האישור לא תקין."

    # בדיקה אם שם המאשר הוזן
    if not approval_data.get('approve_name'):
        return "שם המאשר לא הוזן."

    # בדיקה אם תפקיד המאשר הוזן
    if not approval_data.get('position'):
        return "תפקיד המאשר לא הוזן."

    # בדיקה אם שעות מאושרות לתשלום הוזנו
    if not approval_data.get('approved_hours') or approval_data.get('approved_hours') <= 0:
        return "יש להזין את מספר השעות המאושרות לתשלום."

    # בדיקה אם חתימה הוזנה
    if not approval_data.get('signature'):
        return "חתימת המאשר לא הוזנה."

    return "הקלט תקין"

# דוגמה לשימוש
mentor_data = {
    'mentor_name': 'יוסי כהן',
    'id_number': '123456789',
    'course_name': 'מתודולוגיה מחקרית',
    'department': 'הנדסת תוכנה',
    'start_date': '2025-01-01',
    'end_date': '2025-02-01',
    'total_hours': 40
}

row_data = {
    'date': '2025-01-01',
    'hours': 4,
    'subject': 'מבוא למתודולוגיה',
    'student_name': 'מיכל ישראלי',
    'signature_student': 'מיכל',
    'signature_mentor': 'יוסי'
}

approval_data = {
    'approval_date': '2025-02-02',
    'approve_name': 'ד"ר שמעון פרץ',
    'position': 'דיקן הפקולטה',
    'approved_hours': 40,
    'signature': 'שמעון פרץ'
}

# בדיקת תקינות
print(validate_mentor_data(mentor_data))
print(validate_row_data(row_data))
print(validate_approval_data(approval_data))
