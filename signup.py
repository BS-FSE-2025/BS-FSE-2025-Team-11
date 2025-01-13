import mysql.connector

# חיבור לבסיס הנתונים
conn = mysql.connector.connect(
    host='localhost',
    username='root',
    password='Tmara12345@',
    database='new_project'
)
cursor = conn.cursor()

print("Connection successfully created!")

# פונקציה להוספת משתמש לטבלה
def add_user(username, password, email, id_number, phone_number=None, department=None):
    try:
        # הוספת משתמש לטבלה
        query = '''
        INSERT INTO users (username, password, email, id_number, phone_number, department)
        VALUES (%s, %s, %s, %s, %s, %s)
        '''
        cursor.execute(query, (username, password, email, id_number, phone_number, department))
        conn.commit()  # שמירת השינויים
        print("User added successfully!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# פונקציה לקבלת נתונים מהמשתמש
def get_user_input():
    username = input("הכנס שם משתמש: ")
    password = input("הכנס סיסמה: ")
    email = input("הכנס כתובת אימייל: ")
    id_number = input("הכנס מספר תעודת זהות (9 ספרות): ")
    phone_number = input("הכנס מספר טלפון (אופציונלי): ")
    department = input("הכנס תחום התמחות (אופציונלי): ")

    return username, password, email, id_number, phone_number, department

# קבלת נתונים מהמשתמש
print("הכנס את פרטי המשתמש:")
user_data = get_user_input()

# הוספת המשתמש לבסיס הנתונים
add_user(*user_data)

# הצגת כל המשתמשים
def get_all_users():
    try:
        # שליפת נתונים מהטבלה
        query = "SELECT * FROM users"
        cursor.execute(query)
        rows = cursor.fetchall()
        print("\nUsers in the database:")
        for row in rows:
            print(row)
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# הצגת הנתונים מהטבלה
get_all_users()

# סגירת החיבור
cursor.close()
conn.close()
print("Connection closed.")
