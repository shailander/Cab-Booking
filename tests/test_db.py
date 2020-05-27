import _sqlite3
import unittest
import mock
from database.db import Database
class DatabaseTest(unittest.TestCase):
    @mock.patch('sqlite3.connect')
    def setUp(self, mock_sql_connect):
        mock_connection = mock.Mock()
        mock_sql_connect.return_value = mock_connection
        self.mock_cursor = mock.Mock()
        mock_connection.cursor.return_value = self.mock_cursor
        self.db = Database()

    @mock.patch('sqlite3.connect')
    def test_exception(self, mockConnect):
        mockConnect.side_effect = _sqlite3.Error
        result = Database()
        assert result

    def test_validate_credentials(self):
        self.mock_cursor.fetchall.return_value = [(1,), (2,)]
        assert self.db.validate_credentials({'username': "a", 'password': '123'}, "table name") == True
        self.mock_cursor.fetchall.return_value = []
        assert self.db.validate_credentials({'username': "a", 'password': '123'}, "table name") == False

    def test_get_name(self):
        self.mock_cursor.fetchall.return_value = [('Shailander',)]
        assert self.db.get_name({'username':'u','password':'p'},'table name') == 'Shailander'

    def test_get_id(self):
        self.mock_cursor.fetchall.return_value = [(1,)]
        assert self.db.get_id({'username': "a", 'password': '123'}, "table name") == 1
    def test_insert_cab_details(self):
        self.db.insert_cab_details({'cab_number': 'cab1', 'seat_capacity': 5, 'seat_available': 5, 'route': 'a:c:b',
                                    'timing': '5:00-4:00-8:00'})
        self.mock_cursor.execute.assert_called_once()
    def test_validate_record_existence(self):
        self.mock_cursor.fetchall.return_value = [(1,)]
        assert self.db.validate_record_existence(1, "table name") == True
        self.mock_cursor.fetchall.return_value = []
        assert self.db.validate_record_existence(1, "table name") == False

    def test_validate_employee_existence(self):
        self.mock_cursor.fetchall.return_value = [(1,)]
        assert self.db.validate_employee_existence(1) is None
        self.mock_cursor.fetchall.return_value = []
        assert self.db.validate_employee_existence(1) is None

    def test_find_cab(self):
        self.mock_cursor.fetchall.return_value = [(1,)]
        assert self.db.find_cab('Koramangala', 'HSR') == [(1,)]
        self.mock_cursor.fetchall.return_value = []
        assert self.db.find_cab('Koramangala', 'HSR') == []

    def test_update_details(self):
        self.db.update_details(2, {'username': '2', 'password': '3'}, "table name")
        assert self.mock_cursor.execute.call_count == 2

    def test_update_seat_availability(self):
        self.mock_cursor.fetchall.return_value = [(4,5)]
        self.db.update_seat_availability(1, 1)
        assert self.mock_cursor.execute.call_count == 2

    def test_create_employee_record(self):
        self.db.create_employee_record({'username': 'a123', 'password': 'p', 'name' : 'S'})
        self.mock_cursor.execute.assert_called_once()

    def test_insert_travel_log(self):
        self.db.insert_travel_log({'emp_id':1,'cab_id':1,'trip_date':'09-01-2020','source':'Koramangala',
                        'destination':'HSR','timing':"20:00",'status': 'upcoming'})
        self.mock_cursor.execute.assert_called_once()

    def test_find_travel_time(self):
        self.mock_cursor.fetchall.return_value = [(60,90)]
        assert self.db.find_travel_time('Koramangala','HSR') == 60

    def test_get_travel_history(self):
        self.db.get_travel_history(1)
        self.mock_cursor.execute.assert_called_once()

    def test_update_ride_status(self):
        self.db.update_ride_status(1, "upcoming", "started")
        self.mock_cursor.execute.assert_called_once()

    def test_already_booked_status(self):
        self.mock_cursor.fetchall.return_value = [(1,), (2,)]
        assert self.db.already_booked_status(1) == True
        self.mock_cursor.fetchall.return_value = []
        assert self.db.already_booked_status(1) == False

    def test_get_trip_specifc_info(self):
        self.mock_cursor.fetchall.return_value = [(1,), (2,)]
        assert self.db.get_trip_specifc_info(1, "info") == 1

    def test_check_cancelled_status(self):
        self.mock_cursor.fetchall.return_value = [(1,), (2,)]
        assert self.db.check_cancelled_status(1) == True
        self.mock_cursor.fetchall.return_value = []
        assert self.db.check_cancelled_status(1) == False

    def test_get_record_datewise(self):
        self.mock_cursor.fetchall.return_value = [('cabxyz', '27-05-2020', '21:00', 'Koramangala', 'HSR', 'ended')]
        assert self.db.get_record_datewise('01-01-2020') == [('cabxyz', '27-05-2020', '21:00', 'Koramangala', 'HSR', 'ended')]
        self.mock_cursor.fetchall.return_value = []
        assert self.db.get_record_datewise('01-01-2020') == []

    def test_get_record_weekwise(self):
        self.mock_cursor.fetchall.return_value = [('cabxyz', '27-05-2020', '21:00', 'Koramangala', 'HSR', 'ended')]
        assert self.db.get_record_weekwise('01-01-2020',2) == [('cabxyz', '27-05-2020', '21:00', 'Koramangala', 'HSR', 'ended')]
        self.mock_cursor.fetchall.return_value = []
        assert self.db.get_record_weekwise('01-01-2020',2) == []

    def test_get_record_monthwise(self):
        self.mock_cursor.fetchall.return_value = [('cabxyz', '27-05-2020', '21:00', 'Koramangala', 'HSR', 'ended')]
        assert self.db.get_record_monthwise('01-01-2020') == [('cabxyz', '27-05-2020', '21:00', 'Koramangala', 'HSR', 'ended')]
        self.mock_cursor.fetchall.return_value = []
        assert self.db.get_record_monthwise('01-01-2020') == []

    def test_schedule_trip(self):
        self.db.schedule_trip(1, 1, "Koramangala", "HSR", 1)


    @mock.patch.object(Database, 'check_cancelled_status')
    @mock.patch.object(Database, 'update_ride_status')
    @mock.patch.object(Database, 'find_travel_time')
    def test_start_trip(self, mock_find_travel_time, mock_update_ride_status, mock_check_cancelled_status):
        mock_check_cancelled_status.return_value = True
        assert self.db.start_trip(1,"Koramangala","HSR",1) == None

        mock_check_cancelled_status.return_value = False
        mock_find_travel_time.return_value = 30
        self.db.start_trip(1,"Koramangala","HSR",1)
        mock_update_ride_status.assert_called_once()
        mock_find_travel_time.assert_called_once()


    @mock.patch.object(Database, 'update_ride_status')
    @mock.patch.object(Database, 'update_seat_availability')
    def test_end_trip(self,mock_update_seat_availability,mock_update_ride_status):
        self.db.end_trip(1,1)
        mock_update_seat_availability.assert_called_once()
        mock_update_ride_status.assert_called_once()

if __name__ == '__main__':
    unittest.main()