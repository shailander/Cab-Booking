import sqlite3
from sqlite3 import Error
from database.db_model import RECORD_TABLE
# import datetime


class Database:
    def __init__(self):
        """
        #Initializes database instance
        """
        self.conn = None

        #Creates the instance of the database connection
        try:
            self.conn = sqlite3.connect('database.db')
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
