import time
from tabulate import tabulate
from datetime import date, datetime

class Employee():
    def __init__(self, db, user):
        self.db = db
        self.user = user

    def login(self):
        username = "rohit123"
        password = "123"
        dict = {'username': username, 'password': password}
        access = self.db.validate_credentials(dict, "employee_details")
        if not access:
            print("Username/Password not matched")
            return
        name = self.db.get_name(dict, "employee_details")
        id = self.db.get_id(dict, "employee_details")
        print(f"\nWelcome {name}\n")
        while True:
            n = input(
                '\n1: Book a cab\n2: See booking history\n3: Cancel a booking'
                '\n4: Logout\nEnter your choice : ')
            if n == '1':
                self.booking_cab(id)
            elif n == '2':
                self.booking_history(id)
            elif n == '3':
                self.cancel_booking(id)
            elif n == '4':
                break
            else:
                print('\nWrong Choice!! Try again\n')
        print("\nLogging out!!\n")
        time.sleep(.5)

    def booking_cab(self, id):
        already_booked_status = self.db.already_booked_status(id)
        if already_booked_status :
            print('\nAlready Booked or in a ride\n')
            return
        locations = {1: "Koramangala", 2: "HSR", 3: "Bellandur", 4: "Electronic City", 5: "Sarjapur"}
        for item, value in locations.items():
            print(f"{item} : {value}")
        while True:
            try:
                source_input = int(input('Enter your location: '))
                destination_input = int(input('Enter your destination: '))
                break
            except:
                print('\n*Only numbers is allowed*\n')
        if source_input and destination_input not in locations.keys():
            print('\nWrong Location input\n')
            return
        source = locations[source_input]
        destination = locations[destination_input]
        time_input = input('Enter time: ')
        available_cabs = self.db.find_cab(source, destination)
        available_cabs = self.filter_cab_by_timings(available_cabs, time_input)
        if available_cabs == []:
            print('\nNo cabs found\n')
            return
        print('\n' + tabulate(available_cabs, headers=['Cab ID', 'Cab Number', 'Seat Available',
                                                       'Route', 'timing'], tablefmt='orgtbl') + '\n')
        while True:
            try:
                cab_id_input = int(input('Choose the Cab ID: '))

                break
            except:
                print('\n*Only numbers is allowed*\n')
        self.db.update_seat_availability(cab_id_input, -1)
        date_object = date.today()
        date_str = date_object.strftime("%d-%m-%Y")

        travel_info_dict = {'emp_id': id, 'cab_id': cab_id_input, 'trip_date': date_str,
                            'source': source, 'destination': destination,
                            'timing': time_input, 'status': 'upcoming'}
        self.db.insert_travel_log(travel_info_dict)
        booking_id = self.db.get_trip_specifc_info(id, 'id')
        print(f'\nYour ride is confirmed from {source} to {destination} at {time_input}\n')
        #Function waiting for trip to start
        t1 = datetime.strptime(time_input, '%H:%M')
        current_time = datetime.now()
        current_time_string = current_time.strftime("%H:%M")
        t2 = datetime.strptime(current_time_string, '%H:%M')
        trip_start_time = (t1 - t2).total_seconds()
        self.db.schedule_trip(trip_start_time, id, source, destination, booking_id)

    def filter_cab_by_timings(self, cabs_list, time_input) :
        if cabs_list == [] :
            return []
        updated_list = []
        for i in cabs_list:
            routes = i[3]
            routes = routes.split(':')
            total_time = (self.db.find_travel_time(routes[0], routes[-1]))*2
            time_str = i[4]
            time_str = time_str.split('-')
            count = 0
            for time in time_str:
                t1 = datetime.strptime(time_input, '%H:%M')
                t2 = datetime.strptime(time, '%H:%M')
                if t1 < t2 or ((t1 - t2).total_seconds() / 60) > total_time:
                    count += 1
            if count != len(time_str):
                updated_list.append(i)

        return updated_list


    def booking_history(self, id):
        travel_history = self.db.get_travel_history(id)
        if travel_history == [] :
            print('\nNo Travel History Found\n')
            return
        print('\n' + tabulate(travel_history, headers=['Cab Number', 'Trip Date', 'Time',
                        'Source Location', 'Destination','Status'], tablefmt='orgtbl') + '\n')

    def cancel_booking(self, id):
        already_booked_status = self.db.already_booked_status(id)
        if not already_booked_status:
            print('\nYou have no upcoming ride to cancel\n')
            return
        trip_start_time = self.db.get_trip_specifc_info(id, 'timing')
        t1 = datetime.strptime(trip_start_time, '%H:%M')
        current_time = datetime.now()
        current_time_string = current_time.strftime("%H:%M")
        t2 = datetime.strptime(current_time_string, '%H:%M')
        if (t1 - t2).total_seconds() / 60 < 30 :
            print('\n**You can only cancel the booking prior 30 minutes of the scheduled time**\n')
            return
        self.db.update_ride_status(id, 'upcoming', 'cancelled')
        print('\nBooking cancelled successfully\n')


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
        if not self.db.validate_employee_existence(employee_id):
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
