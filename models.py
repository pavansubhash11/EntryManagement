from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)




class Visitor(db.Model):
	email = db.Column(db.String(200), unique=True, nullable=False, primary_key=True)
	name = db.Column(db.String(100), unique=False, nullable=False)
	phone = db.Column(db.String(20), unique=True, nullable=False)
	def __repr__(self):
		return "<Name: {} Email: {}>".format(self.name,self.email)

class Host(db.Model):
	email = db.Column(db.String(200), unique=True, nullable=False, primary_key=True)
	name = db.Column(db.String(100), unique=False, nullable=False)
	phone = db.Column(db.String(20), unique=True, nullable=False)
	address = db.Column(db.String(20), nullable=False)
	def __repr__(self):
		return "<Name: {} Email: {}>".format(self.name,self.email)


class VisitorEntryDetails(db.Model):
	entryid = db.Column(db.Integer(),primary_key=True)
	visitorid = db.Column(db.Integer(), unique=True, nullable=False)
	hostid = db.Column(db.Integer(), unique=True, nullable=False)
	entryallowed = db.Column(db.Boolean, nullable=False)
	checkin = db.Column(db.String(30))
	checkout = db.Column(db.String(30))
	def __repr__(self):
		return "<Name: {} Email: {} Host: {}>".format(self.name,self.email,self.host)


class ActiveVisitorRequests(db.Model):
	entryid = db.Column(db.Integer(),primary_key=True)
	visitor_email = db.Column(db.String(), nullable=False)
	host_email = db.Column(db.String(), nullable=False)
	link = db.Column(db.String(), nullable=False)
	def __repr__(self):
		return "<Name: {} Email: {} Host: {}>".format(self.name,self.email,self.host)


class VisitorOTP(db.Model):
	email = db.Column(db.String(200), primary_key=True)
	otp = db.Column(db.String(6), nullable=False)
	def __repr__(self):
		return "<Email: {}>".format(self.email)


