import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def sendotp(receiver_address, otp):
	mail_content = "Your OTP is {}. This OTP is valid for 5 minutes.\nThank you\nTeam Innovaccer".format(otp)
	#The mail addresses and password
	sender_address = 'pwnsubhash@gmail.com'
	sender_pass = 'Pawan2016@'
	receiver_address = 'manchesumanth1@gmail.com'
	#Setup the MIME
	message = MIMEMultipart()
	message['From'] = sender_address
	message['To'] = receiver_address
	message['Subject'] = 'Email Verification Code.'   #The subject line
	#The body and the attachments for the mail
	message.attach(MIMEText(mail_content, 'plain'))
	#Create SMTP session for sending the mail
	session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
	session.starttls() #enable security
	session.login(sender_address, sender_pass) #login with mail_id and password
	text = message.as_string()
	session.sendmail(sender_address, receiver_address, text)
	session.quit()
	print('Mail Sent')

sendotp('manchesumanth1@gmail.com',123654)