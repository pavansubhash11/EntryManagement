import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from crypto import genLink
from datetime import datetime


date = datetime.now()
sendotpmessage = open('sendotp.html').read()

sendrequestmessage = open('request.html').read()

def sendotp(visitor_email, auth_otp):
	mail_content = sendotpmessage.format(auth_otp,datetime.now())

	now = datetime.now()

	date = now.strftime("%d-%m-%Y")
	time = now.strftime("%I:%M %p")
	
	sender_address = 'pwnsubhash@gmail.com'
	sender_pass = 'Pawan2016@'
	
	message = MIMEMultipart()
	message['From'] = sender_address
	message['To'] = visitor_email
	
	message['Subject'] = '{} Email Verification Code.'.format(date)   #The subject line
	
	message.attach(MIMEText(mail_content, 'html'))
	
	session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
	session.starttls() #enable security
	session.login(sender_address, sender_pass) #login with mail_id and password
	text = message.as_string()
	session.sendmail(sender_address, visitor_email, text)
	session.quit()

def sendrequest(host_email,visitor_email,visitor_name,visitor_phone,link):
	now = datetime.now()

	date = now.strftime("%d-%m-%Y")
	time = now.strftime("%I:%M %p")

	mail_content = sendrequestmessage.format(visitor_name,visitor_email,visitor_phone,time,date,link+"/accept",link+"/reject",datetime.now())
	sender_address = 'pwnsubhash@gmail.com'
	sender_pass = 'Pawan2016@'
	
	
	message = MIMEMultipart()
	message['From'] = sender_address
	message['To'] = host_email
	message['Subject'] = '{} : Visitor Request.'.format(date)   #The subject line

	message.attach(MIMEText(mail_content, 'html'))

	session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
	session.starttls() #enable security
	session.login(sender_address, sender_pass) #login with mail_id and password
	text = message.as_string()
	session.sendmail(sender_address, host_email, text)
	session.quit()
	print('Mail Sent')


def sendrejectmail(host_email,visitor_email):
	
	mail_content = "Your meeting with {} is rejected".format(host_email,datetime.now())
	sender_address = 'pwnsubhash@gmail.com'
	sender_pass = 'Pawan2016@'
	receiver_address = visitor_email
	
	message = MIMEMultipart()
	message['From'] = sender_address
	message['To'] = visitor_email
	message['Subject'] = '{} : Rejected Visitor Request.'.format(date)   #The subject line

	message.attach(MIMEText(mail_content, 'html'))

	session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
	session.starttls() #enable security
	session.login(sender_address, sender_pass) #login with mail_id and password
	text = message.as_string()
	session.sendmail(sender_address, receiver_address, text)
	session.quit()
	print('Mail Sent')

def sendacceptmail(host_email,visitor_email):
	
	mail_content = "Your meeting with {} is accepted<br>{}".format(host_email,datetime.now())
	sender_address = 'pwnsubhash@gmail.com'
	sender_pass = 'Pawan2016@'
	receiver_address = visitor_email
	
	message = MIMEMultipart()
	message['From'] = sender_address
	message['To'] = visitor_email
	message['Subject'] = '{} : Accepted Visitor Request.'.format(date)   #The subject line

	message.attach(MIMEText(mail_content, 'html'))

	session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
	session.starttls() #enable security
	session.login(sender_address, sender_pass) #login with mail_id and password
	text = message.as_string()
	session.sendmail(sender_address, receiver_address, text)
	session.quit()
	print('Mail Sent')

def sendSummary(visitoremail,hostemail,name,phone,checkin,checkout):

	
	mail_content = "Your Visit ended<br>Details<br>Visitor Name: {}\
				<br>Visitor Phone: {}<br>CheckIn : {}<br>CheckOut: {}\
				<br>{}".format(name,phone,checkin,checkout,datetime.now())
	sender_address = 'pwnsubhash@gmail.com'
	sender_pass = 'Pawan2016@'
	receiver_address = visitoremail
	
	message = MIMEMultipart()
	message['From'] = sender_address
	message['To'] = visitoremail
	message['Subject'] = '{} : Visit Ended.'.format(date)   #The subject line

	message.attach(MIMEText(mail_content, 'html'))

	session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
	session.starttls() #enable security
	session.login(sender_address, sender_pass) #login with mail_id and password
	text = message.as_string()
	session.sendmail(sender_address, receiver_address, text)
	session.quit()
	print('Mail Sent')


link = 'http://127.0.0.1:5000/accept/manche@gmail.com/roy@gmail.com'
#link = "hello.com"
#sendrequest('manchesumanth1@gmail.com','manchesumanth1@gmail.com','sumanth','1234',link)