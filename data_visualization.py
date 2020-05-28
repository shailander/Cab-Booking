import sqlite3
from sqlite3 import Error
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date

class DataVisualization:
    def __init__(self):
        """
        #Initializes database instance
        """
        self.conn = None

        #Creates the instance of the database connection
        try:
            self.conn = sqlite3.connect('/home/nineleaps/PycharmProjects/CabBooking/database.db')
            self.cursor = self.conn.cursor()
            print("Opened database successfully")
        except sqlite3.Error:
            print(Error)

    def get_record(self):
        """
        Getting the data from database and calling function to generate required output
        :return:
        """
        print("Generating required files")
        sql_query = """SELECT * FROM travel_log"""
        self.cursor.execute(sql_query)
        result = self.cursor.fetchall()
        df = pd.DataFrame(result, columns =['id', 'employee_id', 'cab_id', 'trip_date', 'source',
                                            'destination', 'timing', 'status'])
        self.get_per_day_booking_record(df)
        self.get_per_month_booking_record(df)
        self.get_today_booking_count(df)
        self.get_location_wise_booking_count(df)

    def get_per_day_booking_record(self, df):
        """
        Get .png image showing booking count of each day
        :param df:
        :return:
        """
        df1 = df.groupby(['trip_date'])['id'].count().to_frame(name="Booking Count").reset_index()
        df1.plot(kind='bar', x='trip_date', y='Booking Count')
        plt.xlabel("Month")
        plt.xticks(rotation=10)
        plt.savefig('/home/nineleaps/PycharmProjects/CabBooking/output/per-day-booking-count.png')

    def get_per_month_booking_record(self, df):
        """
        Get .png image showing booking count based on month
        :param df:
        :return:
        """
        df['trip_date'] = df['trip_date'].str[3:]
        df2 = df.groupby(['trip_date'])['id'].count().to_frame(name="Booking Count").reset_index()
        df2.plot(kind='bar', x='trip_date', y='Booking Count')
        plt.xlabel("Month")
        plt.xticks(rotation=0)
        plt.savefig('/home/nineleaps/PycharmProjects/CabBooking/output/per-month-booking-count.png')

    def get_today_booking_count(self, df):
        """
        Get .txt file showing the total booking count of today
        :param df:
        :return:
        """
        today = date.today().strftime("%d-%m-%Y")
        sql_query = f"""SELECT id  FROM travel_log WHERE trip_date LIKE '{today}'"""
        self.cursor.execute(sql_query)
        result = self.cursor.fetchall()
        df = pd.DataFrame(result, columns=['Booking ID'])
        f = open(f"/home/nineleaps/PycharmProjects/CabBooking/output/today_booking_count.txt", "w+")
        f.write("The total number of booking on {} = {}".format(today, len(df)))

    def get_location_wise_booking_count(self, df):
        """
        Get .png image showing booking count based on locations(destination)
        :param df:
        :return:
        """
        today = date.today().strftime("%d-%m-%Y")
        sql_query = f"""SELECT destination  FROM travel_log WHERE trip_date LIKE '{today}'"""
        self.cursor.execute(sql_query)
        result = self.cursor.fetchall()
        df = pd.DataFrame(result, columns=['destination'])
        df1 = df.groupby(['destination'])['destination'].count().to_frame(name="Booking Count").reset_index()
        df1.plot(kind='bar', x='destination', y='Booking Count')
        plt.xlabel("Location")
        plt.xticks(rotation=0)
        plt.savefig(f'/home/nineleaps/PycharmProjects/CabBooking/output/location-wise-booking-count.png')

