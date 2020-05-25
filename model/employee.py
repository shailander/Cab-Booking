class Employee():
    def __init__(self, db, user):
        self.db = db
        self.user = user

    def login(self):
        print("Hello Employee HERE")

    def create_member(self):
        member_dict = self.input_member_details()
        self.db.create_employee_record(member_dict)
        print('\nEmployee created successfully\n')

    def update_member(self):
        while True:
            try:
                employee_id = int(input('\nEnter the employee id of the employee you want to update: '))
                break
            except:
                print("\n***Only numbers are allowed***\n")
        if not self.db.validate_record_existence(employee_id, 'employee_details'):
            print(f'\nNo employee found from id -> {employee_id}\n')
            return
        member_dict = self.input_member_details()
        self.db.update_details(employee_id, member_dict, 'employee_details')
        print('\nEmployee created successfully\n')

    def input_member_details(self):
        name = input('Enter employee name: ')
        username = input('Enter employee username: ')
        password = input('Enter employee password: ')
        return {'name': name, 'username': username, 'password': password}

    def delete_member(self):
        while True:
            try:
                employee_id = int(input('\nEnter the employee id of the employee you want to delete: '))
                break
            except:
                print("\n***Only numbers are allowed***\n")
        if not self.db.validate_record_existence(employee_id, 'employee_details'):
            print(f'\nNo employee found from id -> {employee_id}\n')
            return
        self.db.update_details(employee_id, {'active': 0}, 'employee_details')
        print('\nEmployee Record deleted successfully\n')
