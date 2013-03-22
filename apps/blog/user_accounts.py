import webapp2
import re
import jinja2
import os
from google.appengine.ext import db
from libs.pw_hashing import make_pw_hash, valid_pw
from libs.cookie_hashing import make_secure_val , check_secure_val





USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
	return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
	return password and PASS_RE.match(password)

EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
def valid_email(email):
	return not email or EMAIL_RE.match(email)






template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)
	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)
	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))




class SignupHandler(Handler):
	def get(self):
		self.render('signup-form.html')

	def post(self):
		have_error=False
		username = self.request.get("username")
		password = self.request.get("password") 
		verify = self.request.get("verify")
		email = self.request.get("email")

		params = dict(username = username, email =email)
		
		if not valid_username(username):
			params['error_username'] = "That's not a valid username."
			have_error = True

		if not valid_password(password):
			params['error_password'] = "That wasn't a valid password."
			have_error = True
		elif password != verify:
			params['error_verify'] = "Your passwords didn't match."
			have_error = True

		if not valid_email(email):
			params['error_email'] = "That's not a valid email."
			have_error = True

		if have_error:
			self.render('signup-form.html', **params)
		else:
			self.redirect('/unit2/welcome?username=' + username)





class WelcomeHandler(Handler):
	def get(self):
		username = self.request.get('username')
		que = db.Query(UserDB)
		que.filter("db_user",username)
		current_user=que.get()

		if valid_username(username):
			self.render('welcome.html', username = username, current_user = current_user)
		else:
			self.redirect('/unit2/signup')

############## UNIT 4 SIGN UP ###############

class UserDB(db.Model):
	db_user = db.StringProperty(required = True)
	db_password = db.StringProperty(required = True)
	db_email = db.StringProperty (required = True)


class SignupCookieHandler(Handler):
	def get(self):
		self.render('signup-form.html')
		

	def post(self):
		have_error=False
		username = self.request.get("username")
		password = self.request.get("password")
		pw_hash = make_pw_hash(username , password) 
		verify = self.request.get("verify")
		email = self.request.get("email")

		que = db.Query(UserDB)
		que.filter("db_user",username)
		user_check = que.get()

		params = dict(username = username, email =email)
		
		if not valid_username(username):
			params['error_username'] = "That's not a valid username."
			have_error = True

		if not valid_password(password):
			params['error_password'] = "That wasn't a valid password."
			have_error = True
		elif password != verify:
			params['error_verify'] = "Your passwords didn't match."
			have_error = True

		if not valid_email(email):
			params['error_email'] = "That's not a valid email."
			have_error = True

		if user_check:
			params['error_username'] = "User already exists"
			have_error =True

		if have_error:
			self.render('signup-form.html', **params)
		else:
			if not email:
				email=' '
			new_user=UserDB(db_user = username, db_password = pw_hash, db_email = email)
			new_user.put()
			user_id=new_user.key().id()
			cookie_user=make_secure_val(str(user_id))
			self.response.headers.add_header("Set-Cookie","user_id=%s; Domain=cs253-mrnousek.appspot.com; Path=/" % str(cookie_user)) #Domain=cs253-mrnousek.appspot.com;
			self.redirect('/blog/welcome')




class WelcomeCookieHandler(Handler):
	def get(self):
		cookie_user = self.request.cookies.get("user_id")
		if cookie_user:
			user_id = check_secure_val(cookie_user)
			if not user_id:
				self.redirect('/blog/signup')
			current_user=UserDB.get_by_id(int(user_id))
	
			self.render('welcome.html', current_user = current_user)
		else:
			self.redirect('/blog/signup')

class LoginPage(Handler):
	def get(self):
		self.render("login.html")

	def post(self):

		username = self.request.get("username")
		password = self.request.get("password")

		que = db.Query(UserDB)
		que.filter('db_user =',username)
		current_user = que.get()


		if valid_username(username) and current_user:
			if not valid_pw(username, password, current_user.db_password) :
				error_password = "Password doesn't match our records"
				self.render("login.html", username = username, error_password = error_password)

			else:
				# que_key = UserDB.get()
				# que_key.filer('db_user =', username)
				user_id=current_user.key().id()
				cookie_user=make_secure_val(str(user_id))
				self.response.headers.add_header("Set-Cookie","user_id=%s; Domain=cs253-mrnousek.appspot.com; Path=/" % str(cookie_user)) #Domain=cs253-mrnousek.appspot.com;
				self.redirect("/blog/welcome")
		else:
			if not current_user:
				error_username = "Username doesn't exists"
				self.render("login.html", error_username = error_username)


class LogoutPage(Handler):
	def get(self):
		self.response.headers.add_header("Set-Cookie","user_id=; Domain=cs253-mrnousek.appspot.com; Path=/") #Domain=cs253-mrnousek.appspot.com;
		self.redirect("/blog/signup")







		