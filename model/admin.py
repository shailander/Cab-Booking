import time
from model.employee import Employee
from tabulate import tabulate


class Admin:
    def __init__(self, db, user):
        """
        Initialising database and User
        :param db:
        :param user:
        """
        self.db = db
        self.user = user
        self.employee = Employee(db, user)

    def login(self):
        """
        Login validation and homescreen for Admin
        :return:
        """
        username = input("Enter username: ")
        password = input("Enter password: ")
        dict = {'username': username, 'password': password}
        access = self.db.validate_credentials(dict, "Admin")
        if not access:
            print("Username/Password not matched")
            return
        name = self.db.get_name(dict, "Admin")
        print("\nWelcome {}\n".format(name))
        while True:
            n = input(
                '\n1: Check total booking\n2: Check booking of an employee\n'
                '3: Add a cab\n4: Update cab details\n5: Add/Update/Delete Employee\n'
                '6: Logout\nEnter your choice : ')
            if n == '1':
                self.check_total_booking()
            elif n == '2':
                self.check_employee_booking()
            elif n == '3':
                self.add_cab()
            elif n == '4':
                self.update_cab_details()
            elif n == '5':
                self.crud_employee()
            elif n == '6':
                break
            else:
                print('\nWrong Choice!! Try again\n')
        print("\nLogging out!!\n")
        time.sleep(.5)

    def check_total_booking(self):
        """
        Showing total booking record based on date, week, month
        :return:
        """
        date = input('\nEnter the date in DD-MM-YYYY format: ')
        while True:
            try:
                n = int(input('\n1: See booking records date-wise\n2: See booking records week-wise'
                              '\n3: See booking records month-wise\nEnter your choice: '))
                break
            except:
                print("\n***Only numbers are allowed***\n")
        if n == 1 :
            record = self.db.get_record_datewise(date)
        elif n == 2 :
            week_dict = {1: ('01', '02', '03', '04', '05', '06', '07'),
                         2: ('08', '09', '10', '11', '12', '13', '14'),
                         3: ('15', '16', '17', '18', '19', '20', '21'),
                         4: ('22', '23', '24', '25', '27', '28', '29'),
                         5: ('30', '31')}
            week_number = int(int(date[:2]) / 7) + 1
            week_list = week_dict[week_number]
            record = self.db.get_record_weekwise(date[3:], week_list)
        elif n == 3 :
            record = self.db.get_record_monthwise(date[3:])

        if record == []:
            print('\nNo Travel History Found\n')
            return
        print('\n' + tabulate(record, headers=['Employee ID','Cab Number', 'Trip Date', 'Time',
                                                       'Source Location', 'Destination', 'Status'],
                              tablefmt='orgtbl') + '\n')

    def check_employee_booking(self):
        """
        Check total booking record of a employee
        :return:
        """
        while True:
            try:
                employee_id = int(input('\nEnter the employee ID: '))
                break
            except:
                print("\n***Only numbers are allowed***\n")
        if not self.db.validate_record_existence(employee_id, 'employee_details'):
            print(f'\nNo employee found from id -> {employee_id}\n')
            return
        travel_history = self.db.get_travel_history(employee_id)
        if travel_history == []:
            print('\nNo Travel History Found\n')
            return
        print('\n' + tabulate(travel_history, headers=['Cab Number', 'Trip Date', 'Time',
                                                       'Source Location', 'Destination', 'Status'],
                              tablefmt='orgtbl') + '\n')

    def add_cab(self):
        """
        Adding a new cab
        :return:
        """
        cab_detail_dict = self.input_cab_details()
        self.db.insert_cab_details(cab_detail_dict)
        print('\nNew cab details entered successfully\n')


    def update_cab_details(self):
        """
        Updating a cab details
        :return:
        """
        while True:
            try:
                cab_id = int(input('Enter the cab ID of the cab you want to update details: '))
                break
            except:
                print("\n***Only numbers are allowed***\n")
        if not self.db.validate_record_existence(cab_id, 'cab_details'):
            print(f'No cab found from id -> {cab_id}')
            return
        cab_detail_dict = self.input_cab_details()
        self.db.update_details(cab_id, cab_detail_dict, 'cab_details')
        print('\nCab details updated successfully\n')

    def input_cab_details(self):
        """
        Common function for getting the cab details from user
        :return:
        """
        cab_number = input('Enter cab number: ')
        while True:
            try:
                seat_capacity = int(input('Enter the seats capacity: '))
                break
            except:
                print("\n***Only numbers are allowed***\n")
        locations = {1: "Koramangala", 2: "HSR", 3: "Bellandur", 4: "Electronic City", 5: "Sarjapur"}
        for item, value in locations.items():
            print(f"{item} : {value}")
        n = 0
        while True:
            try:
                n = int(input('Enter the routes as in the number specified by them: '))
                break
            except:
                print('\n*Only numbers is alllowed*\n')
        route_num_list = [int(d) for d in str(n)]
        route = ""
        for item in route_num_list:
            route += ":" + locations[item]
        print(route[1:])
        time = input('Enter the running time(24hrs, HH:mm format) of the cab comma(,) seperated: ')
        time_list = time.split(',')
        timing = ""
        for item in time_list:
            timing += "-" + item
        print(timing[1:])
        return {'cab_number': cab_number, 'seat_capacity': seat_capacity,
                           'seat_available': seat_capacity, 'route': route[1:],
                           'timing': timing[1:]}

    def crud_employee(self):
        """
        CRUD operations on employee
        :return:
        """
        while True:
            user_choice = input('\n1: Create Employee\n2: Update Employee\n3: Delete Employee\n'
                  'Any Other key to Exit\nEnter your choice: ')
            if user_choice == '1' :
                self.employee.create_member()
            elif user_choice == '2' :
                self.employee.update_member()
            elif user_choice == '3' :
                self.employee.delete_member()
            else :
                print('')
                break
