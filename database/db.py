import sqlite3
from sqlite3 import Error
from database.db_model import RECORD_TABLE
from threading import Timer
import sys

class Database:
    def __init__(self):
        """
        #Initializes database instance
        """
        self.conn = None

        #Creates the instance of the database connection
        try:
            self.conn = sqlite3.connect('database.db', check_same_thread=False)
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
        sql_query = f"SELECT * FROM {table_name} WHERE username='{dict['username']}'" \
                    f" AND password='{dict['password']}' "
        self.cursor.execute(sql_query)
        result = self.cursor.fetchall()
        if not result:
            return False
        else :
            return True

    def get_name(self, dict, table_name):
        sql_query = f"SELECT name FROM {table_name} WHERE username='{dict['username']}'" \
                    f" AND password='{dict['password']}' "
        self.cursor.execute(sql_query)
        result = self.cursor.fetchall()
        name = [value[0] for value in result]
        return name[0]

    def get_id(self, dict, table_name):
        sql_query = f"SELECT id FROM {table_name} WHERE username='{dict['username']}'" \
                    f" AND password='{dict['password']}' "
        self.cursor.execute(sql_query)
        result = self.cursor.fetchall()
        name = [value[0] for value in result]
        return name[0]

    def insert_cab_deatils(self, dict):
        sql_query = f"INSERT INTO cab_details ('cab_number','seat_capacity','seat_available','route'," \
                    f"'timing') VALUES ('{dict['cab_number']}','{dict['seat_capacity']}'," \
                    f"'{dict['seat_available']}','{dict['route']}','{dict['timing']}')"
        self.cursor.execute(sql_query)
        self.conn.commit()

    def update_details(self, id, dict, table_name):
        for item in dict.items():
            if item[1] != '':
                sql_query = f"UPDATE '{table_name}' SET '{item[0]}' = '{item[1]}' WHERE id = '{id}'"
                self.cursor.execute(sql_query)
                self.conn.commit()

    def validate_record_existence(self,id,table_name):
        sql_query = f"SELECT * FROM {table_name} WHERE id={id}"
        self.cursor.execute(sql_query)
        result = self.cursor.fetchall()
        if not result:
            return False
        else :
            return True

    def create_employee_record(self, dict):
        sql_query = f"INSERT INTO employee_details ('name','username','password')" \
                    f"VALUES ('{dict['name']}','{dict['username']}','{dict['password']}')"
        self.cursor.execute(sql_query)
        self.conn.commit()

    def validate_employee_existence(self, id):
        sql_query=f"SELECT * FROM employee_details WHERE id = {id} AND active = 1"
        self.cursor.execute(sql_query)
        self.conn.commit()

    def find_cab(self, source, destination):
        sql_query = f"""SELECT id,cab_number,seat_available,route,timing FROM cab_details
                        WHERE route LIKE '%{source}%' AND route LIKE '%{destination}%'
                        AND seat_available > 0
                    """
        self.cursor.execute(sql_query)
        result = self.cursor.fetchall()
        return result

    def update_seat_availability(self, id, num):
        sql_query = f"""SELECT seat_available FROM cab_details
                        WHERE id = '{id}'"""
        self.cursor.execute(sql_query)
        result = self.cursor.fetchall()
        seat_count = [value[0] for value in result]
        seat_count_updated = seat_count[0] + num
        sql_query2 = f"""UPDATE cab_details SET seat_available = '{seat_count_updated}'
                        WHERE id = '{id}'"""
        self.cursor.execute(sql_query2)
        self.conn.commit()

    def insert_travel_log(self, dict):
        sql_query = f"""INSERT INTO travel_log ('employee_id','cab_id','trip_date','source',
                        'destination','timing','status') VALUES ('{dict['emp_id']}','{dict['cab_id']}',
                        '{dict['trip_date']}','{dict['source']}','{dict['destination']}',
                        '{dict['timing']}','{dict['status']}')"""
        self.cursor.execute(sql_query)
        self.conn.commit()

    def find_travel_time(self, loc1, loc2):
        sql_query = f"""SELECT time FROM trip_time WHERE
                        source LIKE '{loc1}' AND destination LIKE '{loc2}' OR
                        source LIKE '{loc2}' AND destination LIKE '{loc1}'"""
        self.cursor.execute(sql_query)
        result = self.cursor.fetchall()
        time = [value[0] for value in result]
        return time[0]

    def get_travel_history(self, id):
        sql_query = f"""SELECT cab_number,trip_date,x.timing,source,destination,status 
                        FROM travel_log x JOIN cab_details y ON x.cab_id = y.id
                        WHERE employee_id = '{id}'"""
        self.cursor.execute(sql_query)
        result = self.cursor.fetchall()
        return result

    def update_ride_status(self, id, prev_status, current_status):
        sql_query = f"""UPDATE travel_log SET status = '{current_status}' WHERE
                        id = '{id}' AND status LIKE '{prev_status}'"""
        self.cursor.execute(sql_query)
        self.conn.commit()

    def already_booked_status(self, id):
        sql_query = f"""SELECT * FROM travel_log WHERE employee_id = '{id}' AND
                        status LIKE 'upcoming' OR status LIKE 'started'"""
        self.cursor.execute(sql_query)
        result = self.cursor.fetchall()
        if not result:
            return False
        else:
            return True

    def get_trip_specifc_info(self, id, info):
        sql_query = f"""SELECT {info} FROM travel_log WHERE employee_id='{id}' 
                        AND status LIKE 'upcoming'"""
        self.cursor.execute(sql_query)
        result = self.cursor.fetchall()
        required_data = [value[0] for value in result]
        return required_data[0]

    def check_cancelled_status(self, booking_id):
        sql_query = f"""SELECT * FROM travel_log WHERE id='{booking_id}' AND status LIKE 'cancelled'"""
        self.cursor.execute(sql_query)
        result = self.cursor.fetchall()
        if not result:
            return False
        else:
            return True

    def get_record_datewise(self, date):
        sql_query = f"""SELECT employee_id,cab_number,trip_date,x.timing,source,destination,status 
                        FROM travel_log x JOIN cab_details y ON x.cab_id = y.id
                        WHERE x.trip_date = '{date}'"""
        self.cursor.execute(sql_query)
        result = self.cursor.fetchall()
        return result

    def get_record_weekwise(self, date, week_list):
        sql_query = f"""SELECT employee_id,trip_date,x.timing,source,destination,status 
                                FROM travel_log x JOIN cab_details y ON x.cab_id = y.id
                                WHERE SUBSTR(trip_date,4,7) LIKE '{date}' AND SUBSTR(trip_date,1,2) IN {week_list}"""
        self.cursor.execute(sql_query)
        result = self.cursor.fetchall()
        return result

    def get_record_monthwise(self, date):
        sql_query = f"""SELECT employee_id,cab_number,trip_date,x.timing,source,destination,status 
                                        FROM travel_log x JOIN cab_details y ON x.cab_id = y.id
                                        WHERE SUBSTR(trip_date,4,7) LIKE '{date}'"""
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





