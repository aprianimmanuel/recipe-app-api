"""
Sample Tests
"""

from django.test import SimpleTestCase
from app import calc


class CalcTests(SimpleTestCase):
    """Test the calc module"""

    def test_add_numbers(self):
        """Test that two numbers are added together"""
        res = calc.add(3, 8)
        self.assertEqual(res, 11)

    def test_substract_number(self):
        """Test that values are substracted and returned"""
        res = calc.substract(5, 11)
        self.assertEqual(res, 6)
