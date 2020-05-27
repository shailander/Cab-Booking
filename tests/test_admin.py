import unittest
import mock
from model.admin import Admin
from model.employee import Employee

class AdminTest(unittest.TestCase):
    def setUp(self) :
        db = mock.Mock()
        user = mock.Mock()
        self.admin = Admin(db, user)

    @mock.patch.object(Admin, 'check_total_booking')
    @mock.patch.object(Admin, 'check_employee_booking')
    @mock.patch.object(Admin, 'add_cab')
    @mock.patch.object(Admin, 'update_cab_details')
    @mock.patch.object(Admin, 'crud_employee')
    @mock.patch('builtins.input')
    def test_login(self, mock_input, mock_crud_employee, mock_update_cab_details,
                   mock_add_cab, mock_check_employee_booking, mock_check_total_booking):
        self.admin.db = mock.Mock()
        mock_input.side_effect = ("username", "password")
        self.admin.db.validate_credentials.return_value = False
        assert self.admin.login() == None

        self.admin.db.validate_credentials.return_value = True
        self.admin.db.get_name.return_value = "Admin"
        mock_input.side_effect = ("1","2","3","4","5","7","6")
        self.admin.login()
        mock_check_total_booking.assert_called_once()
        mock_check_employee_booking.assert_called_once()
        mock_add_cab.assert_called_once()
        mock_update_cab_details.assert_called_once()
        mock_crud_employee.assert_called_once()

    @mock.patch('builtins.input')
    def test_check_total_booking(self, mock_input):
        self.admin.db = mock.Mock()
        mock_input.side_effect = ("27-05-2020", "a", "1")
        self.admin.db.get_record_datewise.return_value = []
        assert self.admin.check_total_booking() == None

        mock_input.side_effect = ("27-05-2020", "2")
        self.admin.db.get_record_weekwise.return_value = [(1,2,3,4,5,6,7)]
        self.admin.check_total_booking()
        self.admin.db.get_record_weekwise.assert_called_once()

        mock_input.side_effect = ("27-05-2020", "3")
        self.admin.db.get_record_monthwise.return_value = []
        self.admin.check_total_booking()
        self.admin.db.get_record_monthwise.assert_called_once()

    @mock.patch('builtins.input')
    def test_check_employee_booking(self, mock_input):
        self.admin.db = mock.Mock()
        mock_input.side_effect = ("a", "1")
        self.admin.db.validate_record_existence.return_value = False
        assert self.admin.check_employee_booking() == None

        mock_input.side_effect = ("1")
        self.admin.db.validate_record_existence.return_value = True
        self.admin.db.get_travel_history.return_value = []
        assert self.admin.check_employee_booking() == None

        mock_input.side_effect = ("1")
        self.admin.db.validate_record_existence.return_value = True
        self.admin.db.get_travel_history.return_value = []
        assert self.admin.check_employee_booking() == None

        mock_input.side_effect = ("1")
        self.admin.db.validate_record_existence.return_value = True
        self.admin.db.get_travel_history.return_value = [(1,2,3,4,5,6)]
        assert self.admin.check_employee_booking() == None

    @mock.patch.object(Admin, 'input_cab_details')
    def test_add_cab(self, mock_input_cab_details):
        self.admin.db = mock.Mock()
        mock_input_cab_details.return_value = []
        self.admin.add_cab()
        self.admin.db.insert_cab_details.assert_called_once()
        mock_input_cab_details.assert_called_once()

    @mock.patch.object(Admin, 'input_cab_details')
    @mock.patch('builtins.input')
    def test_update_cab_details(self, mock_input, mock_input_cab_details):
        self.admin.db = mock.Mock()
        mock_input.side_effect = ("a", "1")
        self.admin.db.validate_record_existence.return_value = False
        assert self.admin.update_cab_details() == None

        mock_input.side_effect = ("1")
        self.admin.db.validate_record_existence.return_value = True
        mock_input_cab_details.return_value = []
        self.admin.update_cab_details()
        self.admin.db.update_details.assert_called_once()
        mock_input_cab_details.assert_called_once()

    @mock.patch('builtins.input')
    def test_input_cab_details(self, mock_input):
        self.admin.db = mock.Mock()
        mock_input.side_effect = ("123", "a", "1", "a", "1", "12:00")
        assert self.admin.input_cab_details() == {'cab_number': '123', 'seat_capacity': 1, 'seat_available': 1,
                                                  'route': 'Koramangala', 'timing': '12:00'}

    @mock.patch.object(Employee, 'create_member')
    @mock.patch.object(Employee, 'update_member')
    @mock.patch.object(Employee, 'delete_member')
    @mock.patch('builtins.input')
    def test_crud_employee(self, mock_input, mock_delete_member, mock_update_member, mock_create_member):
        self.admin.db = mock.Mock()
        mock_input.side_effect = ("1", "2", "3", "4")
        self.admin.crud_employee()
        mock_create_member.assert_called_once()
        mock_update_member.assert_called_once()
        mock_create_member.assert_called_once()



















if __name__ == '__main__':
    unittest.main()