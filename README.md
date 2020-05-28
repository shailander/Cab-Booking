Cab Booking System
====
Introduction
----
Cab Booking System is a Simple Console Application where a user can book a cab between different client locations. Multiple employees can book the same cab to travel to client locations or in between stops. Each cab will have a dedicated route and will travel to and fro at different timings. 
Assumptions
----
```
1.This project consists of a single Admin.
2.The time between two locations is provided beforehand for an employee to book a cab.
3.If a employee source, destination and cab time lies in between a route and trip time of a cab respectively, the cab will pick it up irrespective of it's current location.
4. For demonstaration process all the accepted ride will start in 10 seconds and will also end in 10 seconds. The real time required code is commented.
```
ADMIN LOGIN
----
### Login configuration parameters
The following credentials are required for ADMIN login:
```
name : Big Boss
username : admin123
password : password
```
These credentials should be provided to get access inside the Admin panel.

EMPLOYEE LOGIN
----
### Login configuration parameters
The following credentials are required for Employee login:
```
name : Rohit Sharma
username : rohit123
password : 123rohit
```
```
name : Adarsh Pundir
username : adarsh123
password : 123adarsh
```
```
name : Sharad Goyal
username : sharad123
password : 123sharad
```
These credentials should be provided to get access inside the Employee panel.
### STEPS to Setup and Run the Project 
```
1. Open the terminal,and enter the path containing the project
2. Execute the command: python3 Main.py
3. You will see a message "Connection is established: Database Created!" You will be directed to the login page.
4. Now choose the user you want to get logged in as.
5. Enter the credentials
6. You will be redirected to the display panel of the desired user persona.
```
### STEPS to Setup and Run the Unit Tests
```
1. Open the terminal,and enter the path containing the project
2. Execute the following command:
        a. `pip install mock`
        b. `pip install coverage`
3. Now execute the command : `coverage run --source=. -m unittest discover`
4. Then execute : `coverage html`
5. These command will successfully run the unit tests and generate coverage report
6. Right click htmlcov folder and click on show in files option
7. Double click on index.html file
8. A coverage report will be displayed on the browser page.
9. Run the following command for testing a specific file
     `python -m unittest test_case_directory/test_case_file_name.py`
```
### Setup CRON job to send daily update at 11:00 PM to the Admin
```
1. Add your email id and passowrd in `email_user` and `email_password`, email id of the receiver in `email_send` in the send_daily_mail.py file.
2. If your 2-step verification is on, use application passowrd instead of mail password.
3. Run `crontab -e` in the terminal
4. Add command `0 23 * * * python3 [path to the project]/CabBooking/send_daily_mail.py` to the bottom of the file.

```
###Key Entities in Code
```
+-- cab
|  +--htmlcov
|  +--model
   |  +-- admin.py
   |  +-- employee.py
|  +--database
   |  +-- db.py
   |  +-- db_model.py
|  +--tests
   |  +-- test_admin.py
   |  +-- test_employee.py
   |  +-- test_db.py
   |  +-- test_main.py
|  +--main.py
|  +--database.db
|  +--.coveragerc
|  +--data_visualization.py
|  +--send_daily_mail.py
```