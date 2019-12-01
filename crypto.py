from passlib.hash import sha256_crypt

def genLink(host_email,visitor_email):
	return sha256_crypt.encrypt(host_email+visitor_email)
