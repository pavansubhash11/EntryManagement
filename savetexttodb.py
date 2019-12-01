f = open('host.txt')

from app import db,Host as host

db.create_all()

for line in f:
	try:
		x = line.split(',')
		name, email, phone, address = x[0], x[1], x[2], x[3]
		h = host(host_name=name, host_email=email, host_phone=phone, host_address=address)
		db.session.add(h)
		db.session.commit()
	except:
		continue