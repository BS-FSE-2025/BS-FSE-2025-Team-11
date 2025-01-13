import re

def validate_username(username):
    # בודק אם שם המשתמש לא ריק ויש בו לפחות 5 תווים
    if len(username) >= 5:
        return True
    return "Username must be at least 5 characters long."

def validate_password(password):
    # בודק אם הסיסמה לפחות 8 תווים ומכילה תו מיוחד, אות רישית, תו קטן ומספר
    if len(password) >= 8 and re.search(r'[A-Z]', password) and re.search(r'[a-z]', password) and re.search(r'[0-9]', password) and re.search(r'[\W_]', password):
        return True
    return "Password must be at least 8 characters long, contain at least one uppercase letter, one lowercase letter, one number, and one special character."

def validate_email(email):
    # בודק אם כתובת האימייל תקינה
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(email_regex, email):
        return True
    return "Invalid email format."

def validate_id_number(id_number):
    # בודק אם מספר הזהות מכיל בדיוק 9 ספרות
    if id_number.isdigit() and len(id_number) == 9:
        return True
    return "ID number must be exactly 9 digits."

def validate_phone_number(phone_number):
    # בודק אם מספר הטלפון מכיל בדיוק 10 ספרות ומתחיל ב-"05"
    if phone_number.isdigit() and len(phone_number) == 10:
        if phone_number.startswith("05"):
            return True
        return "Phone number must start with '05'."
    return "Phone number must be exactly 10 digits."

def validate_department(department):
    # בודק אם שם המחלקה לא ריק
    if len(department) > 0:
        return True
    return "Department cannot be empty."

def validate_signup(data):
    # בודק את כל השדות ומחזיר את התוצאות
    validations = {
        "username": validate_username(data.get('username', '')),
        "password": validate_password(data.get('password', '')),
        "email": validate_email(data.get('email', '')),
        "id_number": validate_id_number(data.get('id_number', '')),
        "phone_number": validate_phone_number(data.get('phone_number', '')),
        "department": validate_department(data.get('department', ''))
    }
    
    # בודק אם יש בעיות עם אחד מהשדות
    for field, result in validations.items():
        if result != True:
            return {field: result}
    
    return "All fields are valid."

# דוגמה של נתוני טופס
form_data = {
    "username": "user123",
    "password": "Password123!",
    "email": "user@example.com",
    "id_number": "123456789",
    "phone_number": "0501234567",
    "department": "Computer Science"
}

# הפעלת הבדיקה
validation_result = validate_signup(form_data)

if validation_result == "All fields are valid.":
    print("Form is valid!")
else:
    print("Validation errors:", validation_result)

