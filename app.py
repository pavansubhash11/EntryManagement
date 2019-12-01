from flask import Flask, request, render_template, redirect, url_for
import os
from flask_sqlalchemy import SQLAlchemy
from random import randint
from emailing import sendotp
from emailing import sendrequest
from emailing import sendacceptmail
from emailing import sendrejectmail
from emailing import sendSummary
from crypto import genLink
from datetime import datetime
from flask import json
from sqlalchemy import and_


project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "EntryManager.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)

# Models 

# Visitor details Table for storing Visitor Details
class Visitor(db.Model):
	visitor_email = db.Column(db.String(200), unique=True, nullable=False, primary_key=True)
	visitor_name = db.Column(db.String(100), unique=False, nullable=False)
	visitor_phone = db.Column(db.String(20), unique=True, nullable=False)
	def __repr__(self):
		return "<Name: {} Email: {} Phone: {}>".format(self.visitor_name,self.visitor_email,self.visitor_phone)

# Host details Table for storing Host Details
class Host(db.Model):
	host_email = db.Column(db.String(200), unique=True, nullable=False, primary_key=True)
	host_name = db.Column(db.String(100), unique=False, nullable=False)
	host_phone = db.Column(db.String(20), unique=True, nullable=False)
	host_address = db.Column(db.String(100), nullable=False)
	def __repr__(self):
		return "<Name: {} Email: {} Phone: {} Address: {}>".format(self.host_name,self.host_email,self.host_phone,self.host_address)


# VisitorOTP Table stores otp sent to emails of visitors for authentication purposes
class VisitorOTP(db.Model):
	visitor_email = db.Column(db.String(200), unique=True,primary_key=True)
	auth_otp = db.Column(db.String(6), nullable=False)
	def __repr__(self):
		return "<Email: {} OTP: {}>".format(self.visitor_email,self.auth_otp)

# ActiveVisitorRequests Table is for storing details of requests made by visitor for entry
class ActiveVisitorRequests(db.Model):
	request_id = db.Column(db.Integer(),primary_key=True)
	visitor_email = db.Column(db.String(), nullable=False)
	host_email = db.Column(db.String(), nullable=False)
	approval_link = db.Column(db.String(), nullable=False) # This is an unique link for each visitor-host pair in 
														   # requests table useful to host for accepting or rejecting the visitor entry
	def __repr__(self):
		return "<Visitor: {} Host: {}>".format(self.visitor_email,self.host_email)

# VisitorEntry Details Table is for storing summary of visitor's entry
class VisitorEntryDetails(db.Model):
	visit_id = db.Column(db.Integer(),primary_key=True)
	visitor_email = db.Column(db.String(),  nullable=False)
	host_email = db.Column(db.String(),nullable=False)
	status = db.Column(db.Boolean, nullable=False)  # Indicates whether entry approved or not
	checkin = db.Column(db.String(30))
	checkout = db.Column(db.String(30))
	def __repr__(self):
		return "<Visitor: {} Host: {} Status: {} checkin: {} checkout: {}>".format(
				self.visitor_email,self.host_email,self.status,self.checkin,self.checkout)



# Generates otp and sends a mail to provided email for authentication
def GenrateOTP(visitor_email):
	auth_otp = randint(100000,999999)
	
	list1 = VisitorOTP.query.filter_by(visitor_email=visitor_email).all()
	
	if len(list1)!=0:
		VisitorOTP.query.filter_by(visitor_email=visitor_email).delete()
		visitor_otp_record = VisitorOTP(visitor_email = visitor_email, auth_otp=auth_otp)
		db.session.add(visitor_otp_record)
		db.session.commit()
		
	else:
		visitor_otp_record = VisitorOTP(visitor_email = visitor_email, auth_otp=auth_otp)
		db.session.add(visitor_otp_record)
		db.session.commit()
		
	return auth_otp

# Adds visitor details into visitor table
def addVisitorDetails(visitor_name,visitor_email,visitor_phone):

		if len(Visitor.query.filter(and_(Visitor.visitor_email != (visitor_email),Visitor.visitor_phone == (visitor_phone))).all())>0:
			return False
		
		elif len(Visitor.query.filter(and_(Visitor.visitor_email == (visitor_email),Visitor.visitor_phone == (visitor_phone))).all())>0:
			return True
		
		elif len(Visitor.query.filter(and_(Visitor.visitor_email == (visitor_email), Visitor.visitor_phone != (visitor_phone))).all())>0:
			
			Visitor.query.filter(Visitor.visitor_email == (visitor_email)).delete()
			visitor = Visitor(visitor_name=visitor_name,visitor_phone= visitor_phone, visitor_email = visitor_email)
			db.session.add(visitor)
			db.session.commit()
			return True

		else:
			visitor = Visitor(visitor_name=visitor_name,visitor_phone= visitor_phone, visitor_email = visitor_email)
			db.session.add(visitor)
			db.session.commit()
			return True



# Index Page route
@app.route("/")
def home():
    return render_template('visitorIndex.html')


@app.route('/otpform',methods = ['POST', 'GET'])
def otpform():
	if request.method == 'GET':
		return redirect(url_for('home'))
	elif request.method == 'POST':
		visitor_email = request.form.get('visitor_email')
		auth_otp = GenrateOTP(visitor_email)
		sendotp(visitor_email=visitor_email,auth_otp = auth_otp)
		return render_template('OTPForm.html',visitor_email=visitor_email)

@app.route('/resendotp/<visitor_email>')
def resendotp(visitor_email):
	auth_otp = GenrateOTP(visitor_email)
	sendotp(visitor_email=visitor_email,auth_otp = auth_otp)
	return render_template('OTPForm.html',visitor_email=visitor_email)



@app.route('/addcheckout',methods = ['POST', 'GET'])
def addcheckout():
	if request.method == 'GET':
		print("GET Request to otpform page, Redirecting to home page")
		return redirect(url_for('home'))
	elif request.method == 'POST':
		visitor_email = request.form.get('visitor_email')
		x = VisitorEntryDetails.query.filter(and_(VisitorEntryDetails.visitor_email == visitor_email,VisitorEntryDetails.checkin!='NULL')).all()
		y = x[0]
		hostemail = y.host_email
		checkin = y.checkin
		checkout = datetime.now()
		for vis in x:
			vis.checkout = datetime.now()
			db.session.commit()

		vis = Visitor.query.filter_by(visitor_email = visitor_email).all()[0]
		phone = vis.visitor_phone
		name  = vis.visitor_name
		sendSummary(visitor_email,hostemail,name,phone,checkin,checkout)
		return redirect(url_for('home'))


@app.route('/rotpform/<visitor_email>')
def rotpform(visitor_email):
	if visitor_email:
		return render_template('OTPForm.html',message="OTP you entered is Invalid! Please try again",visitor_email=visitor_email)
	else:
		return render_template('visitorIndex.html')


@app.route('/accept_or_reject/<hostemail>/<visitoremail>/<result>')
def accept_or_reject(hostemail,visitoremail,result):
	link = "/accept_or_reject/"+hostemail+'/'+visitoremail

	entry = ActiveVisitorRequests.query.filter_by(approval_link=link).all()

	if(len(entry)==0):
		return render_template('wait.html',message="The Link Is Invalid")
	entry = entry[0]
	if result == 'reject':
		host_email = entry.host_email
		visitor_email = entry.visitor_email
		checkin = datetime.now()
		visentry = VisitorEntryDetails(host_email = host_email,visitor_email = visitor_email,status = False)
		entry = ActiveVisitorRequests.query.filter_by(approval_link=link).delete()
		sendrejectmail(host_email,visitor_email)
		db.session.add(visentry)
		db.session.commit()
		return render_template('successfullydone.html',message="Your Rejection is done")
	else:

		host_email = entry.host_email
		visitor_email = entry.visitor_email
		checkin = datetime.now()
		sendacceptmail(host_email,visitor_email)
		visentry = VisitorEntryDetails(host_email = host_email,visitor_email = visitor_email,status = True,checkin=checkin)
		entry = ActiveVisitorRequests.query.filter_by(approval_link=link).delete()
		db.session.add(visentry)
		db.session.commit()
		return render_template('successfullydone.html',message="Your Acceptance is done")



@app.route('/getdetails',methods = ['POST', 'GET'])
def getdetails():
	if request.method == 'GET':
		return redirect(url_for('home'))
	else:
		auth_otp = request.form.get('auth_otp')
		visitor_email = request.form.get('visitor_email')
		actual_otp = VisitorOTP.query.filter_by(visitor_email=visitor_email).all()[0].auth_otp

		if str(actual_otp) == str(auth_otp):
			VisitorOTP.query.filter(VisitorOTP.visitor_email==visitor_email).delete()
			
			host_names = [host.host_name for host in Host.query.all()]
			host_phones = [host.host_phone for host in Host.query.all()]
			host_emails =  [host.host_email for host in Host.query.all()]
			
			# e2 = []
			# p2 = []
			# n2 = []
			# for i in host_emails:
			# 	e2.append('"' + i + '"')
			# # for j in host_names:
			# 	n2.append('"' + j + '"')
			# for k in host_phones:
			# 	p2.append('"' + k + '"')
			
			# host_emails = "[" + ','.join(e2) + "]"
			# host_phones = "[" + ','.join(p2) + "]"
			# host_names =  "[" + ','.join(n2) + "]"

			print(host_emails,host_phones,host_names)
			list1 = Visitor.query.filter_by(visitor_email=visitor_email).all()
			
			if len(list1)==0:
				return render_template('details.html',visitor_email=visitor_email,host_emails = (host_emails),
								host_phones = (host_phones),host_names=(host_names))
			else:
				visitor = list1[0]
				visitor_phone = visitor.visitor_phone
				visitor_name = visitor.visitor_name
				return render_template('details.html',visitor_email=visitor_email,visitor_phone=visitor_phone,
					visitor_name=visitor_name, host_emails = (host_emails),
					host_phones = (host_phones),host_names=(host_names),exists="YES")
		
		else:
			return redirect(url_for("rotpform",visitor_email = visitor_email))



@app.route('/submit',methods = ['POST', 'GET'])
def submit():
	if request.method == 'GET':
		return redirect(url_for('home'))
	else:
		
		visitor_name = request.form.get('visitor_name')
		visitor_email = request.form.get('visitor_email')
		visitor_phone = request.form.get('visitor_phone')
		host_email = request.form.get('host_details')
		
		Done = addVisitorDetails(visitor_name=visitor_name, visitor_email=visitor_email,visitor_phone=visitor_phone)
		if(not Done):

			host_names = [host.host_name for host in Host.query.all()]
			host_phones = [host.host_phone for host in Host.query.all()]
			host_emails =  [host.host_email for host in Host.query.all()]
			
			# e2 = []
			# p2 = []
			# n2 = []
			# for i in host_emails:
			# 	e2.append('"' + i + '"')
			# for j in host_names:
			# 	n2.append('"' + j + '"')
			# for k in host_phones:
			# 	p2.append('"' + k + '"')
			
			# host_emails = "[" + ','.join(e2) + "]"
			# host_phones = "[" + ','.join(p2) + "]"
			# host_names =  "[" + ','.join(n2) + "]"

			return render_template('details.html',visitor_email=visitor_email,visitor_phone=visitor_phone,
					visitor_name=visitor_name, host_emails = (host_emails),host_phones = (host_phones),
					host_names=(host_names),exists="YES",message=visitor_phone + " is already under use")

		link = url_for("home")+"accept_or_reject/"+(host_email)+"/"+(visitor_email)
		active_requests = ActiveVisitorRequests.query.filter_by(
								approval_link = link).all()
		
		if len(active_requests)>0:
			return render_template('wait.html',
				message="Your request for meeting {} is already in process! Please wait.".format(host_email))
		else:
			sendrequest(host_email,visitor_email,visitor_name,visitor_phone,"http://127.0.0.1:5000"+link)
			active_request = ActiveVisitorRequests(visitor_email = visitor_email,host_email =host_email,approval_link=link)
			db.session.add(active_request)
			db.session.commit()
			return render_template('wait.html')


if __name__ == "__main__":
    app.run(debug=True)