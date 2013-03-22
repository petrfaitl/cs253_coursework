import random
import string
import hashlib

def make_salt():
    return ''.join(random.choice(string.letters) for x in xrange(5))

# implement the function make_pw_hash(name, pw) that returns a hashed password 
# of the format: 
# HASH(name + pw + salt),salt
# use sha256

def make_pw_hash(name, pw):
	salt=make_salt()
	h= hashlib.sha256(name+pw+salt).hexdigest()
	return '%s|%s' % (h,salt)

# Implement the function valid_pw() that returns True if a user's password 
# matches its hash. You will need to modify make_pw_hash.

def valid_pw(name,pw,h):
	h,salt=h.split("|")
	validate_h=hashlib.sha256(name+pw+salt).hexdigest()
	if h == validate_h:
		return True
	else:
		return False


    
#h = make_pw_hash('spez', 'hunter2')
#print valid_pw('spez', 'hunter2', h)
