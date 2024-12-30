import unittest
from private import validate_input  # החלף בנתיב הנכון לקובץ שלך

class TestValidateInput(unittest.TestCase):
    def test_valid_input(self):
        # הכנת נתוני קלט תקניים
        valid_data = {
            "full_name": "John Doe",
            "id_number": "123456789",
            # ... שאר השדות עם נתונים תקניים
        }
        
        # קריאה לפונקציה עם נתונים תקניים
        validate_input(**valid_data)  # פריקת מילון לפרמטרים
        # בדיקה שאין שגיאות (אפשר להוסיף בדיקות נוספות, למשל בדיקה שהנתונים נשמרו כראוי למסד הנתונים)

    def test_invalid_id_number(self):
        # הכנת נתוני קלט עם ת.ז. לא תקינה
        invalid_data = {
            "full_name": "John Doe",
            "id_number": "1234567",  # ת.ז. קצרה מדי
            # ... שאר השדות
        }

        # קריאה לפונקציה ואימות שהיא מעלה את השגיאה המתאימה
        with self.assertRaises(Exception) as context:
            validate_input(**invalid_data)
        self.assertIn("תעודת זהות חייבת להכיל בדיוק 9 ספרות.", str(context.exception))

    # הוסף מקרי בדיקה נוספים לבדיקת שאר תנאי האימות
    # לדוגמה: בדיקת פורמט מייל, בדיקת טלפון, בדיקת שמות ימים, וכו'