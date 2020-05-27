import unittest
import mock
from model.employee import Employee
from datetime import datetime

class EmployeeTest(unittest.TestCase):
    def setUp(self) :
        db = mock.Mock()
        user = mock.Mock()
        self.employee = Employee(db, user)

    @mock.patch.object(Employee,'booking_cab')
    @mock.patch.object(Employee, 'booking_history')
    @mock.patch.object(Employee, 'cancel_booking')
    @mock.patch('builtins.input')
    def test_login(self, mock_input, mock_cancel_booking, mock_booking_history, mock_booking_cab):
        self.employee.db = mock.Mock()
        mock_input.side_effect = ("username", "password")
        self.employee.db.validate_credentials.return_value = False
        assert self.employee.login() == None

        self.employee.db.validate_credentials.return_value = True
        self.employee.db.get_name.return_value = "Admin"
        self.employee.db.get_id.return_value = 1
        mock_input.side_effect = ("username", "password", "5", "1", "2", "3", "4")
        self.employee.login()
        mock_booking_cab.assert_called_once()
        mock_booking_history.assert_called_once()
        mock_cancel_booking.assert_called_once()

    @mock.patch.object(Employee, 'filter_cab_by_timings')
    @mock.patch('builtins.input')
    def test_booking_cab(self, mock_input, mock_filter_cab_by_timings):
        self.employee.db = mock.Mock()
        self.employee.db.already_booked_status.return_value = True
        assert self.employee.booking_cab(1) == None

        self.employee.db.already_booked_status.return_value = False
        mock_input.side_effect = ("a", "1", "7")
        assert self.employee.booking_cab(1) == None

        self.employee.db.already_booked_status.return_value = False
        mock_input.side_effect = ("1", "2", "00:00")
        assert self.employee.booking_cab(1) == None

        self.employee.db.already_booked_status.return_value = False
        mock_input.side_effect = ("1", "2", "23:59")
        self.employee.db.find_cab.return_value = [(1, 2, 3, 4, 5)]
        mock_filter_cab_by_timings.return_value = []
        assert self.employee.booking_cab(1) == None

        self.employee.db.already_booked_status.return_value = False
        mock_input.side_effect = ("1", "2", "23:59", "a", "1")
        self.employee.db.find_cab.return_value = [(1, 2, 3, 4, 5)]
        mock_filter_cab_by_timings.return_value = [(1, 2, 3, 4, 5)]
        self.employee.db.get_trip_specifc_info.return_value = 1
        self.employee.booking_cab(1)
        self.employee.db.update_seat_availability.assert_called_once()
        self.employee.db.insert_travel_log.assert_called_once()

    def test_filter_cab_by_timings(self):
        self.employee.db = mock.Mock()
        assert self.employee.filter_cab_by_timings([], "12:00") == []

        self.employee.db.find_travel_time.return_value = 30
        assert self.employee.filter_cab_by_timings([(1, 1, 1, "Koramangala:Whitefield", "12:00")], "14:00") == []

        self.employee.db.find_travel_time.return_value = 30
        assert self.employee.filter_cab_by_timings([(1, 1, 1, "Koramangala:Whitefield", "12:00" )], "12:00") == \
               [(1, 1, 1, "Koramangala:Whitefield", "12:00" )]

    def test_booking_history(self):
        self.employee.db = mock.Mock()
        self.employee.db.get_travel_history.return_value = []
        assert self.employee.booking_history(1) == None

        self.employee.db.get_travel_history.return_value = [(1, 2, 3, 4, 5, 6)]
        assert self.employee.booking_history(1) == None

    @mock.patch.object(Employee, 'calculate_minutes')
    def test_cancel_booking(self, mock_calculate_minutes):
        self.employee.db = mock.Mock()
        self.employee.db.already_booked_status.return_value = False
        assert self.employee.cancel_booking(1) == None

        self.employee.db.already_booked_status.return_value = True
        self.employee.db.get_trip_specifc_info.return_value = "12:30"
        mock_calculate_minutes.return_value = True
        assert self.employee.cancel_booking(1) == None

        self.employee.db.already_booked_status.return_value = True
        self.employee.db.get_trip_specifc_info.return_value = "12:30"
        mock_calculate_minutes.return_value = False
        self.employee.cancel_booking(1)
        self.employee.db.update_ride_status.assert_called_once()

    def test_calculate_minutes(self):
        t1 = datetime.strptime("12:45", '%H:%M')
        t2 = datetime.strptime("12:00", '%H:%M')
        assert self.employee.calculate_minutes(t1, t2) == False

        t2 = datetime.strptime("12:30", '%H:%M')
        assert self.employee.calculate_minutes(t1, t2) == True

    @mock.patch.object(Employee, 'input_member_details')
    def test_create_member(self, mock_input_member_details):
        self.employee.db = mock.Mock()
        mock_input_member_details.return_value = 1
        self.employee.create_member()
        self.employee.db.create_employee_record.assert_called_once()

    @mock.patch.object(Employee, 'input_member_details')
    @mock.patch('builtins.input')
    def test_update_member(self, mock_input, mock_input_member_details):
        self.employee.db = mock.Mock()
        mock_input.side_effect = ("a", "1")
        self.employee.db.validate_employee_existence.return_value = False
        assert self.employee.update_member() == None

        mock_input.side_effect = ("a", "1")
        self.employee.db.validate_employee_existence.return_value = True
        mock_input_member_details.return_value = 1
        self.employee.update_member()
        self.employee.db.update_details.assert_called_once()

    @mock.patch('builtins.input')
    def test_input_member_details(self, mock_input):
        mock_input.side_effect = ("1", "2", "3")
        assert self.employee.input_member_details() == {'name': '1', 'username': '2', 'password': '3'}

    @mock.patch('builtins.input')
    def test_delete_member(self, mock_input):
        self.employee.db = mock.Mock()
        mock_input.side_effect = ("a", "1")
        self.employee.db.validate_record_existence.return_value = False
        assert self.employee.delete_member() == None

        mock_input.side_effect = ("a", "1")
        self.employee.db.validate_record_existence.return_value = True
        self.employee.delete_member()
        self.employee.db.update_details.assert_called_once()






if __name__ == '__main__':
    unittest.main()