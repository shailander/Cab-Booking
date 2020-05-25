
class Admin():
    def __init__(self, db, user):
        self.db = db
        self.user = user

    def login(self):
        # username = input("Enter username: ")
        # password = input("Enter password: ")
        # dict = {'username': username, 'password': password}
        # access = self.db.validate_credentials(dict, "Admin")
        # if not access:
        #     print("Username/Password not matched")
        #     return
        # name = self.db.get_name(dict, "Admin")
        # print(f"Welcome {name}")
        while True:
            n = input(
                '1: Check total booking\n2: Check booking of an employee\n'
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
        print("\nThanks for visiting AIMS!!\n")

    def check_table_booking(self):
        print('Check Table Booking')

    def check_employee_booking(self):
        print('Employee Booking')

    def add_cab(self):
        cab_number = input('Enter cab number')
        while True:
            try:
                seats_available = int(input('Enter the seats capacity: '))
                break
            except:
                print("\n***Only numbers are allowed***\n")
        locations={1 :"Koramangala", 2:"HSR", 3:"Bellandur", 4:"Electronic City", 5:"Sarjapur"}
        for item, value in locations.items():
            print(f"{item} : {value}")
        while True:
            try :
                n = int(input('Enter the routes as in the number specified by them'))
                break
            except :
                print('\n*Only numbers is alllowed*\n')
        route_num_list = [int(d) for d in str(n)]
        route = ""
        for item in route_num_list :
            route += ":"+locations[item]
        print(route[1:])
        time = input('Enter the running time(24hrs, HH:mm format) of the cab comma(,) seperated: ')
        time_list = time.split(',')
        timing = ""
        for item in time_list :
            timing += "-"+item
        print(timing[1:])






    def update_cab_details(self):
        print('update cab details')

    def crud_employee(self):
        print('crud employee')