import re

def validate_full_name(full_name):
    # בודק אם שם מלא לא ריק
    if len(full_name) > 0:
        return True
    return "Full name cannot be empty."

def validate_id_number(id_number):
    # בודק אם מספר הזהות מכיל בדיוק 9 ספרות
    if id_number.isdigit() and len(id_number) == 9:
        return True
    return "ID number must be exactly 9 digits."

def validate_department(department):
    # בודק אם שם המחלקה לא ריק
    if len(department) > 0:
        return True
    return "Department cannot be empty."

def validate_phone(phone_number):
    # בודק אם מספר הטלפון מכיל בדיוק 10 ספרות ומתחיל ב-05
    if phone_number.isdigit() and len(phone_number) == 10 and phone_number.startswith("05"):
        return True
    return "Phone number must be exactly 10 digits and start with '05'."

def validate_email(email):
    # בודק אם כתובת המייל תקינה
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(email_regex, email):
        return True
    return "Invalid email format."

def validate_courses(courses):
    # בודק אם שדות הקורסים לא ריקים
    if len(courses) > 0:
        return True
    return "Courses field cannot be empty."

def validate_time_slots(time_slots):
    # בודק אם יש לפחות שעת התחלה ושעת סיום
    if len(time_slots) >= 1:
        for slot in time_slots:
            if 'start' not in slot or 'end' not in slot or slot['start'] == '' or slot['end'] == '':
                return "Each time slot must have a start and end time."
        return True
    return "At least one time slot is required."

def validate_signup(data):
    # בודק את כל השדות ומחזיר את התוצאות
    validations = {
        "full_name": validate_full_name(data.get('full_name', '')),
        "id_number": validate_id_number(data.get('id_number', '')),
        "department": validate_department(data.get('department', '')),
        "phone": validate_phone(data.get('phone', '')),
        "email": validate_email(data.get('email', '')),
        "courses": validate_courses(data.get('courses', '')),
        "time_slots": validate_time_slots(data.get('time_slots', []))
    }
    
    # בודק אם יש בעיות עם אחד מהשדות
    for field, result in validations.items():
        if result != True:
            return {field: result}
    
    return "All fields are valid."

# דוגמה של נתוני טופס
form_data = {
    "full_name": "יוסי כהן",
    "id_number": "123456789",
    "department": "מדעי המחשב",
    "phone": "0501234567",
    "email": "yossi@example.com",
    "courses": "מתמטיקה, פיזיקה",
    "time_slots": [
        {"start": "10:00", "end": "12:00"},
        {"start": "13:00", "end": "15:00"}
    ]
}

# הפעלת הבדיקה
validation_result = validate_signup(form_data)

if validation_result == "All fields are valid.":
    print("Form is valid!")
else:
    print("Validation errors:", validation_result)
