import sqlite3
from sqlite3 import Error
from database.db_model import RECORD_TABLE
from threading import Timer
from database.db_queries import *
import sys

DATABASE_PATH = "/home/nineleaps/PycharmProjects/CabBooking/database.db"

class Database:
    def __init__(self):
        """
        #Initializes database instance
        """
        self.conn = None

        #Creates the instance of the database connection
        try:
            self.conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
            self.cursor = self.conn.cursor()
            print("Opened database successfully")
        except sqlite3.Error:
            print(Error)

        # Creates the database tables if not created
        if self.conn is not None:
            self.cursor.executescript(RECORD_TABLE)
        else:
            print("Error! cannot create the database connection.")

    def validate_credentials(self, dict, table_name):
        sql_query = query_validate_credentials(dict, table_name)
        self.cursor.execute(sql_query)
        result = self.cursor.fetchall()
        if not result:
            return False
        else :
            return True

    def get_name(self, dict, table_name):
        sql_query = query_validate_credentials(dict, table_name)
        self.cursor.execute(sql_query)
        result = self.cursor.fetchall()
        name = [value[0] for value in result]
        return name[0]

    def get_id(self, dict, table_name):
        sql_query = query_get_id(dict, table_name)
        self.cursor.execute(sql_query)
        result = self.cursor.fetchall()
        name = [value[0] for value in result]
        return name[0]

    def insert_cab_details(self, dict):
        sql_query = query_insert_cab_details(dict)
        self.cursor.execute(sql_query)
        self.conn.commit()

    def update_details(self, id, dict, table_name):
        for item in dict.items():
            if item[1] != '':
                sql_query = query_update_details(id, item, table_name)
                self.cursor.execute(sql_query)
                self.conn.commit()

    def validate_record_existence(self,id,table_name):
        sql_query = query_validate_record_existence(id, table_name)
        self.cursor.execute(sql_query)
        result = self.cursor.fetchall()
        if not result:
            return False
        else :
            return True

    def create_employee_record(self, dict):
        sql_query = query_create_employee_record(dict)
        self.cursor.execute(sql_query)
        self.conn.commit()

    def validate_employee_existence(self, id):
        sql_query = query_validate_employee_existence(id)
        self.cursor.execute(sql_query)
        self.conn.commit()

    def find_cab(self, source, destination):
        sql_query = query_find_cab(source, destination)
        self.cursor.execute(sql_query)
        result = self.cursor.fetchall()
        return result

    def update_seat_availability(self, id, num):
        sql_query = query_get_seat_availability(id)
        self.cursor.execute(sql_query)
        result = self.cursor.fetchall()
        seat_count = [value[0] for value in result]
        seat_count_updated = seat_count[0] + num
        sql_query2 = query_update_seat_availability(id, seat_count_updated)
        self.cursor.execute(sql_query2)
        self.conn.commit()

    def insert_travel_log(self, dict):
        sql_query = query_insert_travel_log(dict)
        self.cursor.execute(sql_query)
        self.conn.commit()

    def find_travel_time(self, loc1, loc2):
        sql_query = query_find_travel_time(loc1, loc2)
        self.cursor.execute(sql_query)
        result = self.cursor.fetchall()
        time = [value[0] for value in result]
        return time[0]

    def get_travel_history(self, id):
        sql_query = query_get_travel_history(id)
        self.cursor.execute(sql_query)
        result = self.cursor.fetchall()
        return result

    def update_ride_status(self, id, prev_status, current_status):
        sql_query = query_update_ride_status(id, prev_status, current_status)
        self.cursor.execute(sql_query)
        self.conn.commit()

    def already_booked_status(self, id):
        sql_query = query_already_booked_status(id)
        self.cursor.execute(sql_query)
        result = self.cursor.fetchall()
        if not result:
            return False
        else:
            return True

    def get_trip_specifc_info(self, id, info):
        sql_query = query_get_trip_specifc_info(id, info)
        self.cursor.execute(sql_query)
        result = self.cursor.fetchall()
        required_data = [value[0] for value in result]
        return required_data[0]

    def check_cancelled_status(self, booking_id):
        sql_query = query_check_cancelled_status(booking_id)
        self.cursor.execute(sql_query)
        result = self.cursor.fetchall()
        if not result:
            return False
        else:
            return True

    def get_record_datewise(self, date):
        sql_query = query_get_record_datewise(date)
        self.cursor.execute(sql_query)
        result = self.cursor.fetchall()
        return result

    def get_record_weekwise(self, date, week_list):
        sql_query = query_get_record_weekwise(date, week_list)
        self.cursor.execute(sql_query)
        result = self.cursor.fetchall()
        return result

    def get_record_monthwise(self, date):
        sql_query = query_get_record_monthwise(date)
        self.cursor.execute(sql_query)
        result = self.cursor.fetchall()
        return result

    def schedule_trip(self, trip_start_time, id, source, destination, booking_id):
        # start_trip_task = Timer(trip_start_time, self.start_trip, [str(id), source, destination,booking_id])
        # For demonstration purpose using 10 seconds till the trip start
        start_trip_task = Timer(10, self.start_trip, [id, source, destination, booking_id])
        start_trip_task.start()
        # start_trip_task.cancel()

    def start_trip(self, cab_id, source, destination, booking_id):
        cancelled_status = self.check_cancelled_status(booking_id)
        if cancelled_status:
            return
        self.update_ride_status(booking_id, "upcoming", "started")
        trip_time_seconds = self.find_travel_time(source, destination) * 60
        # end_trip_task = Timer(trip_time_seconds, self.start_trip, [str(id), source, destination])
        # For demonstration purpose using 10 seconds till the trip ends
        end_trip_task = Timer(10, self.end_trip, [booking_id, cab_id])
        end_trip_task.start()

    def end_trip(self, booking_id, cab_id):
        self.update_ride_status(booking_id, "started", "ended")
        self.update_seat_availability(cab_id, 1)





