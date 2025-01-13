import mysql.connector
from mysql.connector import Error

# חיבור לבסיס הנתונים
def connect_to_db():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Tmara12345@',
            database='new_project'
        )
        if conn.is_connected():
            print("החיבור לבסיס הנתונים הצליח")
            return conn
    except Error as e:
        print(f"יש שגיאה בחיבור לבסיס הנתונים: {e}")
        return None

# שמירת בקשה בטבלה personal_request
def save_personal_request(conn, full_name, id_number, department, academic_year, phone_number, email, campus, course_names, shifts_hours, preferred_days):
    try:
        cursor = conn.cursor()
        query = '''
            INSERT INTO personal_request (full_name, id_number, department, academic_year, phone_number, email, campus, course_names, shifts_hours, preferred_days)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        cursor.execute(query, (full_name, id_number, department, academic_year, phone_number, email, campus, course_names, shifts_hours, preferred_days))
        conn.commit()
        print("הנתונים נשמרו בהצלחה")
    except Error as e:
        print(f"יש שגיאה בשמירת הנתונים: {e}")

# הצגת כל הבקשות שנשמרו
def select_all_requests(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM personal_request;")
        rows = cursor.fetchall()
        print("הבקשות שנשמרו:")
        for row in rows:
            print(row)
    except Error as e:
        print(f"יש שגיאה בהבאת הנתונים: {e}")

# פונקציה לבדוק אם הקלט תקין
def validate_input(full_name, id_number, phone_number):
    # בדיקת מספר טלפון (10 ספרות ותחיל ב-05)
    if len(phone_number) != 10:
        raise ValueError("מספר הטלפון חייב להיות 10 ספרות")
    if not phone_number.startswith("05"):
        raise ValueError("מספר הטלפון חייב להתחיל ב-05")

    # בדיקת תעודת זהות (9 ספרות בלבד)
    if len(id_number) != 9 or not id_number.isdigit():
        raise ValueError("מספר תעודת הזהות חייב להיות 9 ספרות בלבד")
    
    # בדיקת שם מלא
    if not full_name.strip():
        raise ValueError("שם מלא לא יכול להיות ריק")
    
    return True

# פונקציה לקבלת הנתונים מהמשתמש
def get_user_input():
    full_name = input("שם מלא: ").strip()
    id_number = input("ת.ז: ").strip()
    department = input("מחלקה: ").strip()
    academic_year = input("שנה אקדמית: ").strip()
    phone_number = input("טלפון נייד: ").strip()
    email = input("כתובת מייל: ").strip()
    campus = input("קמפוס: ").strip()
    course_names = input("שמות קורסים: ").strip()
    shifts_hours = input("שעות תגבור: ").strip()
    preferred_days = input("ימים מועדפים: ").strip()

    return full_name, id_number, department, academic_year, phone_number, email, campus, course_names, shifts_hours, preferred_days

def main():
    # קבלת קלט מהמשתמש
    full_name, id_number, department, academic_year, phone_number, email, campus, course_names, shifts_hours, preferred_days = get_user_input()

    # בדיקת תקינות קלט
    try:
        validate_input(full_name, id_number, phone_number)
    except ValueError as e:
        print(f"שגיאה: {e}")
        return

    # חיבור לבסיס הנתונים
    conn = connect_to_db()
    if conn:
        # שמירת הנתונים בטבלה
        save_personal_request(conn, full_name, id_number, department, academic_year, phone_number, email, campus, course_names, shifts_hours, preferred_days)

        # הצגת כל הבקשות שנשמרו
        select_all_requests(conn)

        # סגירת החיבור לבסיס הנתונים
        conn.close()

if __name__ == "__main__":
    main()