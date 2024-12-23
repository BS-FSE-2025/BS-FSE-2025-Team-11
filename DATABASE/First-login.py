import mysql.connector

# إعدادات الاتصال بقاعدة البيانات
conn = mysql.connector.connect(
    host="localhost",       # اسم الخادم
    user="root",            # اسم المستخدم
    password="",            # كلمة المرور
    database="user_data"    # اسم قاعدة البيانات
)

# إنشاء كائن Cursor لتنفيذ الأوامر
cursor = conn.cursor()

# إدخال البيانات
def insert_user(username, password, email, phone_number, id_number, specialization):
    try:
        query = INSERT INTO users (username, password, email, phone_number, id_number, specialization)
        VALUES (%s, %s, %s, %s, %s, %s)
        cursor.execute(query, (username, password, email, phone_number, id_number, specialization))
        conn.commit()  
        print("User added successfully!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# عرض البيانات
def get_users():
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    for row in results:
        print(row)


if __name__ == "__main__":
    insert_user("Ali123", "securepassword", "ali@example.com", "0123456789", "123456789", "Computer Science")
    print("Current Users:")
    get_users()


cursor.close()
conn.close()
