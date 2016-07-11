import os
import webapp2
import jinja2
import hashlib
import hmac
import random
from string import letters

from google.appengine.ext import ndb

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

# 'user_id': 123,
# 'username': 'kukuh',
# 'password': 'hunterpass',
# 'secret': 'secretpass',

SECRET = 'secretpass'

class HashingCookie():
	def hash_str(self, s):
		# return hashlib.md5(s).hexdigest()
		return hmac.new(SECRET, s).hexdigest()

	def make_secure_value(self, s):
		return "%s|%s" % (s, self.hash_str(s))

	def check_secure_value(self, s):
		value = s.split('|')[0]
		if s == self.make_secure_value(value):
			return value
		else:
			return False

class HashingPassword():
	def make_salt(self, length=5):
		return ''.join(random.choice(letters) for x in xrange(length))
		
	def make_hashing_password(self, name, password, salt=None):
		if not salt:
			salt = self.make_salt()
			print 'salt: '+salt
		h = hashlib.sha256(str(name)+str(password)+str(salt)).hexdigest()
		return '%s,%s' % (salt, h)

	def validate_password(self, name, password, h):
		salt = h.split(',')[0]
		return h == self.make_hashing_password(name, password, salt)
		

class User(ndb.Model):
	# userid = ndb.IntegerProperty(required=True)
	username = ndb.StringProperty(required=True)
	password = ndb.StringProperty(required=True)
	email = ndb.StringProperty()
	created_date = ndb.DateTimeProperty(auto_now_add=True)

	@classmethod
	def register(cls, username, password, email=None):
		hashed_password = HashingPassword().make_hashing_password(username, password)
		new_user = User(username=username, password=hashed_password, email=email)
		new_user.put()
		return new_user.key.id()

	@classmethod
	def login(cls, username, password):
		pass
		

class Handler(webapp2.RequestHandler):
	"""Handler Prototype"""
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

	def set_secure_cookie(self, name, value):
		if value:
			cookie_value = HashingCookie().make_secure_value(str(value))
		else:
			cookie_value = ''
		self.response.headers.add_header('Set-Cookie', '%s=%s' % (name, cookie_value))
		
	def read_secure_cookie(self, name):
		cookie_value = self.request.cookies.get(name)
		if cookie_value:
			return HashingCookie().check_secure_value(cookie_value)
		else:
			return False

	def whatisthis(self, s):
	    if isinstance(s, str):
	        print "ordinary string"
	    elif isinstance(s, unicode):
	        print "unicode string"
	    else:
	        print "not a string"

class HomePage(Handler):
	def get(self):
		self.render("home.html")

	def post(self):
		self.render("home.html")

class LoginPage(Handler):
	def get(self):
		userid = self.read_secure_cookie('id')
		if userid:
			self.redirect('/dashboard')
		else:
			self.render("login.html")

	def post(self):
		username = self.request.get('username')
		password = self.request.get('password')


		# validate_user()

class LogoutPage(Handler):
	def get(self):
		self.set_secure_cookie('id', '')
		self.redirect('/')

	def post(self):
		self.set_secure_cookie('id', '')
		self.redirect('/')

class RegisterPage(Handler):
	def get(self):
		self.render("register.html")

	def post(self):
		username = self.request.get('username')
		password = self.request.get('password')
		password_again = self.request.get('password-again')
		email = self.request.get('email')

		if password != password_again:
			error = 'Password should be same with Password Again'
			self.render("register.html", error=error)
		else:
			userid = User.register(username, password, email)
			self.set_secure_cookie('id', userid)
			self.redirect('/dashboard')

class DashboardPage(Handler):
	def get(self):
		userid = self.read_secure_cookie('id')
		if userid:
			self.render("dashboard.html")
		else:
			self.redirect('/')

app = webapp2.WSGIApplication([
	('/', HomePage),
	('/login', LoginPage),
	('/logout', LogoutPage),
	('/register', RegisterPage),
	('/dashboard', DashboardPage),
	], debug=True)
