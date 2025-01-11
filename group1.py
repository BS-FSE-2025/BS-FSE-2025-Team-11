import re
import mysql.connector

def connect_to_db():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Tmara12345@',
            database='student'  # בהנחה שבסיס הנתונים "student" כבר קיים
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def create_table_if_not_exists(conn):
    cursor = conn.cursor()
    cursor.execute('''  
        CREATE TABLE IF NOT EXISTS group_request (
            course_name VARCHAR(80) NOT NULL,
            course_number INT,
            department VARCHAR(80),
            campus VARCHAR(15),
            preferred_mode ENUM('פרונטלי', 'זום'),
            suggested_times TEXT,
            students_list TEXT,
            contact_name VARCHAR(80),
            contact_id_number VARCHAR(20),
            contact_phone VARCHAR(15),
            contact_email VARCHAR(60)
        );
    ''')
    conn.commit()

def insert_request_to_db(conn, course_name, course_number, department, campus, preferred_mode, suggested_times, students_list, contact_name, contact_id_number, contact_phone, contact_email):
    cursor = conn.cursor()
    cursor.execute('''  
        INSERT INTO group_request (course_name, course_number, department, campus, preferred_mode, suggested_times, students_list, contact_name, contact_id_number, contact_phone, contact_email)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ''', (course_name, course_number, department, campus, preferred_mode, suggested_times, students_list, contact_name, contact_id_number, contact_phone, contact_email))
    conn.commit()

def validate_request():
    print("בדיקת נתוני בקשה לתגבור קבוצתי")

    course_name = input("שם הקורס: ").strip()
    course_number = input("מספר הקורס: ").strip()
    department = input("מחלקה: ").strip()
    campus = input("קמפוס: ").strip()
    preferred_mode = input("עדיפות הקבוצה (פרונטלי / זום): ").strip()
    suggested_times = input("3 הצעות למועדי התגבור (פורמט יום משעה עד שעה): ").strip()
    students_list = input("רשימת הסטודנטים (מינימום 7 סטודנטים): ").strip()
    contact_name = input("שם איש קשר: ").strip()
    contact_id_number = input("ת.ז. איש קשר: ").strip()
    contact_phone = input("טלפון נייד של איש קשר: ").strip()
    contact_email = input("כתובת מייל של איש קשר: ").strip()

    errors = []

    # בדיקות תקינות
    if len(course_name) < 3:
        errors.append("שם הקורס חייב להכיל לפחות 3 תווים.")
    
    if not re.match(r"^\d+$", course_number):
        errors.append("מספר הקורס חייב להיות מספר.")
    
    if len(department) < 3:
        errors.append("שם המחלקה חייב להכיל לפחות 3 תווים.")
    
    if len(campus) < 2:
        errors.append("שם הקמפוס חייב להיות לפחות 2 תווים.")
    
    if preferred_mode not in ['פרונטלי', 'זום']:
        errors.append("יש לבחור בין תגבור פרונטלי או תגבור בזום.")
    
    if len(suggested_times.split("\n")) < 3:
        errors.append("יש להזין 3 הצעות למועדי התגבור.")
    
    if len(students_list.split(',')) < 7:
        errors.append("יש לציין לפחות 7 סטודנטים בבקשה.")
    
    if len(contact_name) < 3:
        errors.append("שם איש הקשר חייב להכיל לפחות 3 תווים.")
    
    if not re.match(r"^05\d{8}$", contact_phone):
        errors.append("טלפון של איש הקשר חייב להתחיל ב-05 ולהכיל 10 ספרות.")

    if not re.match(r"[^@]+@[^@]+\.[^@]+", contact_email):
        errors.append("כתובת מייל לא תקינה.")

    # הצגת השגיאות
    if errors:
        print("\nשגיאות שנמצאו:")
        for error in errors:
            print(f"- {error}")
        return

    # אם הכל תקין
    print("\nהבקשה תקינה ונשלחה בהצלחה!")
    print(f"שם הקורס: {course_name}")
    print(f"מספר הקורס: {course_number}")
    print(f"מחלקה: {department}")
    print(f"קמפוס: {campus}")
    print(f"עדיפות: {preferred_mode}")
    print(f"מועדי תגבור: {suggested_times}")
    print(f"רשימת הסטודנטים: {students_list}")
    print(f"איש קשר: {contact_name}")
    print(f"טלפון של איש הקשר: {contact_phone}")

    # חיבור לבסיס נתונים והכנסת הנתונים
    conn = connect_to_db()
    if conn:
        create_table_if_not_exists(conn)
        insert_request_to_db(conn, course_name, course_number, department, campus, preferred_mode, suggested_times, students_list, contact_name, contact_id_number, contact_phone, contact_email)
        conn.close()
    else:
        print("לא הצלחנו להתחבר לבסיס הנתונים.")

if __name__ == "__main__":
    validate_request()
