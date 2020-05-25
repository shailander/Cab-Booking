import time
from model.employee import Employee

class Admin:
    def __init__(self, db, user):
        self.db = db
        self.user = user
        self.employee = Employee(db, user)

    def login(self):
        # username = input("Enter username: ")
        # password = input("Enter password: ")
        username = "admin123"
        password = "password"
        dict = {'username': username, 'password': password}
        access = self.db.validate_credentials(dict, "Admin")
        if not access:
            print("Username/Password not matched")
            return
        name = self.db.get_name(dict, "Admin")
        print(f"\nWelcome {name}\n")
        while True:
            n = input(
                '\n1: Check total booking\n2: Check booking of an employee\n'
                '3: Add a cab\n4: Update cab details\n5: Add/Update/Delete Employee\n'
                '6: Logout\nEnter your choice : ')
            if n == '1':
                self.check_table_booking()
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

    def check_table_booking(self):
        print('Check Table Booking')

    def check_employee_booking(self):
        print('Employee Booking')

    def add_cab(self):
        cab_detail_dict = self.input_cab_details()
        self.db.insert_cab_deatils(cab_detail_dict)
        print('\nNew cab details entered successfully\n')


    def update_cab_details(self):
        while True:
            try:
                cab_id = int(input('Enter the cab ID of the cab you want to update details'))
                break
            except:
                print("\n***Only numbers are allowed***\n")
        if not self.db.validate_record_existence(cab_id, 'cab_details'):
            print(f'No cab found from id -> {cab_id}')
            return
        cab_detail_dict = self.input_cab_details()
        self.db.update_deatils(cab_id, cab_detail_dict, 'cab_details')
        print('\nCab details updated successfully\n')

    def input_cab_details(self):
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
                break
