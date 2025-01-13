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

 # בדיקה אם יש יותר מ-7 סטודנטים
def check_students(data):
    if len(data['students']) < 7:
        return "הדרישה היא לפחות 7 סטודנטים"
    else:
        return "הכמות תקינה"


    # בדיקה אם כל השדות עבור הימים והשעות הוזנו בצורה תקינה
    for option in data['times']:
        day = option['day']
        start_time = option['start']
        end_time = option['end']

        # בדיקה אם יום הוזן בצורה תקינה
        if day not in ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday']:
            return f"יום {day} לא תקני"

        # בדיקה אם השעות הוזנו בצורה תקינה
        time_format = re.compile(r"^([01]?[0-9]|2[0-3]):([0-5]?[0-9])$")
        if not re.match(time_format, start_time):
            return f"שעת התחלה {start_time} לא תקנית"
        if not re.match(time_format, end_time):
            return f"שעת סיום {end_time} לא תקנית"

    return "הקלט תקין"

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
    ]
}

# קריאה לפונקציה
result = validate_course_data(data)
print(result)

