import unittest
import mysql.connector

class TestDatabaseUpdate(unittest.TestCase):

    def setUp(self):
        """
        إعداد قاعدة البيانات للبدء بالاختبارات.
        إنشاء اتصال واختبار إذا كان يعمل.
        """
        self.connection = mysql.connector.connect(
            host="localhost",  # قم بتعديل الإعدادات حسب قاعدة البيانات الخاصة بك
            user="root",
            password="password",
            database="test_db"
        )
        self.cursor = self.connection.cursor()

        # إعداد جدول تجريبي
        self.cursor.execute("CREATE TABLE IF NOT EXISTS test_table (id INT PRIMARY KEY, name VARCHAR(100))")
        self.cursor.execute("INSERT INTO test_table (id, name) VALUES (1, 'Original') ON DUPLICATE KEY UPDATE name='Original'")
        self.connection.commit()

    def test_update_row(self):
        """
        اختبار تحديث صف معين في الجدول.
        """
        # إعداد الاستعلام
        table_name = "test_table"
        column_to_update = "name"
        new_value = "Updated"
        condition = "id = 1"

        # تنفيذ التحديث
        update_query = f"UPDATE {table_name} SET {column_to_update} = %s WHERE {condition}"
        self.cursor.execute(update_query, (new_value,))
        self.connection.commit()

        # التحقق من التحديث
        self.cursor.execute(f"SELECT {column_to_update} FROM {table_name} WHERE {condition}")
        result = self.cursor.fetchone()

        # التحقق من أن النتيجة مطابقة
        self.assertEqual(result[0], new_value, "The value in the database was not updated correctly.")

    def tearDown(self):
        """
        تنظيف قاعدة البيانات بعد انتهاء الاختبارات.
        """
        self.cursor.execute("DROP TABLE IF EXISTS test_table")
        self.connection.commit()
        self.cursor.close()
        self.connection.close()


if __name__ == "__main__":
    unittest.main()
