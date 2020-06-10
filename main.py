from database.db import Database
from model.admin import Admin
from model.employee import Employee
import sys

class User() :
    def main_dashboard(self, db, user):
        """
        Main Dashboard
        :param db:
        :param user:
        :return:
        """
        print('Welcome to Cab Booking Service!!\nLogin as :\n1 : Admin\n2 : Employee\nAny Number : Exit')
        while True:
            try:
                n = int(input('Enter your choice : '))
                break
            except:
                print('\n***Only numbers is allowed***\n')
        if n == 1:
            admin = Admin(db, user)
            admin.login()
        elif n == 2:
            employee = Employee(db, user)
            employee.login()
        else:
            sys.exit(1)


if __name__ == "__main__":

    #Initiate the database
    db = Database()

    user = User()
    while(True) :
        user.main_dashboard(db, user)
