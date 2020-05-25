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