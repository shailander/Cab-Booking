import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import date
from data_visualization import DataVisualization

dv = DataVisualization()
dv.get_record()

email_user = 'shailander.singh@nineleaps.com' #Enter your email
email_password = 'sample_password'           #Enter your password
email_send = 'shailander.singh@nineleaps.com' #Enter receiver email
today = date.today().strftime("%d-%m-%Y")

subject = 'Booking Status for {}'.format(today)
msg = MIMEMultipart()
msg['From'] = email_user
msg['To'] = email_send
msg['Subject'] = subject

body = 'Hi there, the booking details of today is attach hereby'
msg.attach(MIMEText(body, 'plain'))

filenames=['/home/nineleaps/PycharmProjects/CabBooking/output/location-wise-booking-count.png',
           '/home/nineleaps/PycharmProjects/CabBooking/output/per-day-booking-count.png',
           '/home/nineleaps/PycharmProjects/CabBooking/output/per-month-booking-count.png',
           '/home/nineleaps/PycharmProjects/CabBooking/output/today_booking_count.txt']

for filename in filenames :
    attachment = open(filename, 'rb')

    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= " + filename)
    msg.attach(part)

text = msg.as_string()
server = smtplib.SMTP('smtp.gmail.com',587)
server.starttls()
server.login(email_user,email_password)


server.sendmail(email_user,email_send,text)
server.quit()