import unittest
from unittest.mock import patch, MagicMock

from io import StringIO
import sys

from private import validate_input

class TestValidateInput(unittest.TestCase):

    @patch('builtins.input', side_effect=['Jo', '12345678', 'Computer Science', 'A', '123456789', 'john@example', 'B\'er Sheva', 'Math,Physics', 'Sunday', '10:00-12:00'])
    def test_validate_input_failure(self, mock_input):
        # Capture the output
        captured_output = StringIO()
        sys.stdout = captured_output
        
        validate_input()
        
        # Restore stdout
        sys.stdout = sys.__stdout__

        # Check for expected error messages
        output = captured_output.getvalue()
        self.assertIn("שגיאות:", output)
        self.assertIn("שם מלא חייב להכיל לפחות 3 תווים.", output)
        self.assertIn("תעודת זהות חייבת להכיל בדיוק 9 ספרות.", output)

if __name__ == '__main__':
    unittest.main()