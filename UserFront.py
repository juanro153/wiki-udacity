import User
import BaseHandler
import re

class Signup(BaseHandler.Handler):
	def get(self, username=''):
		self.render('signup.html', username=username) 

	def post(self):
		username  = self.request.get('username')
		password = self.request.get('password')
		verify = self.request.get('verify')
		email = self.request.get('email')
		
		valid = True
		
		params=dict(username = username, email = email)
		user = User.User.by_name(username)
		

		user_re = re.compile("^[a-zA-Z0-9_-]{3,20}$")	
		if  not (username and user_re.match(username)):
			valid = False
			params['usererror']="That's not a valid username."
			
		elif user:
			valid = False
			params['usererror']="Username already exists."
		

		password_re = re.compile("^.{3,20}$")
		if  not (password and password_re.match(password)):
			params['pwerror']="That's not a valid password."
			valid = False
		
		elif password != verify:
			params['vererror']="Your passwordds didn't match."
			valid = False
			
		email_re = re.compile("^[\S]+@[\S]+\.[\S]+$")
		if  not (email_re.match(email) or not email):
			params['emailerror']="That's not a valid email."
			validity=False 
		
		if valid:
			
			user = User.User.register(username,password,email)
			user.put()
			self.login(user)
			self.redirect('/')
		else:
			self.render('signup.html', **params) 
	
        		

class Login(BaseHandler.Handler):
	def get(self):
		self.render("login.html")
		
	def post(self):
		username = self.request.get('username')
		password = self.request.get('password')
		
		user = User.User.login(username, password)
		if user:
			self.login(user)
			self.redirect('/')
			
		else:
			self.render('login.html', errorlogin = 'invalid login')
		
class Logout(BaseHandler.Handler):	
	def get(self):
		self.logout()
		self.redirect('/')