import hmac

SECRET="Try_me_you_son_of_a"
from google.appengine.ext import db

import hashlib

def hash_str(s):
	return hmac.new(SECRET, s).hexdigest()



def make_secure_val(s):
	return  "%s|%s" %(s, hash_str(s))

def check_secure_val(h):
	s,HASH =h.split("|")
	if make_secure_val(s)==h:
		return s
	else:
		None