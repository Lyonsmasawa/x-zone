import unittest
from app.models import User

class TestUser(unittest.TestCase):
    """
    Test User Class
    """     
    def setUp(self):
        self.new_user = User(username = 'Lyons', email = 'lyons@gmail.com', password = 'lyonspass')

    def test_password_setter(self):
        self.assertTrue(self.new_user.pass_secure is not None)

    def test_no_access_password(self):
        with self.assertRaises(AttributeError):
            self.new_user.password

    def test_verify_password(self):
        self.assertTrue(self.new_user.verify_password('banana'))