from model.admin import Admin
from model.employee import Employee
from main import User
import unittest
import mock
class UserTest(unittest.TestCase):
    def setUp(self):
        self.user = User()

    @mock.patch.object(Admin, 'login')
    @mock.patch.object(Employee, 'login')
    @mock.patch('builtins.input')
    def test_main_dashboard(self, mock_input, mock_login1, mock_login2):
        db = mock.Mock()
        user = mock.Mock()
        mock_input.side_effect = ("a", "1")
        self.user.main_dashboard(db, user)
        mock_login2.assert_called_once()

        mock_input.side_effect = "2"
        self.user.main_dashboard(db, user)
        mock_login1.assert_called_once()

        mock_input.side_effect = "3"
        with self.assertRaises(SystemExit) as cm:
            self.user.main_dashboard(db, user)
        self.assertEqual(cm.exception.code, 1)

if __name__ == '__main__':
    unittest.main()