import os
import webapp2
import jinja2
import hashlib
import hmac

from google.appengine.ext import ndb

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

# 'user_id': 123,
# 'username': 'kukuh',
# 'password': 'hunterpass',
# 'secret': 'secretpass',

SECRET = 'secretpass'

CREDENTIAL = {
				'user_id': 123,
				'username': 'kukuh',
				'hmac_password': 'f8e72b971aced103b676af2f95affb08',
			}

class Hashing():
	def hash_str(s):
		# return hashlib.md5(s).hexdigest()
		return hmac.new(SECRET, s).hexdigest()

	def make_secure_value(s):
		return "%s|%s" % (s, hash_str(s))

	def check_secure_value(s):
		value = s.split('|')[0]
		if s == make_secure_value(value):
			return value
		else:
			return '0'

class User(ndb.Model):
	userid = ndb.IntegerProperty(required=True)
	username = ndb.StringProperty(required=True)
	password = ndb.StringProperty(required=True)
	email = ndb.StringProperty()
	created_date = ndb.DateTimeProperty(auto_now_add=True)


class Handler(webapp2.RequestHandler):
	"""Handler Prototype"""
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))
		

class HomePage(Handler):
	def get(self):
		self.render("home.html")

	def post(self):
		check_username = CREDENTIAL['username'] == self.request.get('username')
		hashed_password = hash_str(self.request.get('password'))
		check_password = CREDENTIAL['hmac_password'] == hashed_password

		if check_username and check_password:
			self.render("dashboard.html")
		else:
			self.render("login.html")

class LoginPage(Handler):
	def get(self):
		self.render("login.html")

	def post(self):
		pass

class LogoutPage(Handler):
	def get(self):
		self.redirect('/')

	def post(self):
		self.redirect('/')

class RegisterPage(Handler):
	def get(self):
		self.render("register.html")

	def post(self):
		pass

class DashboardPage(Handler):
	def get(self):
		self.render("dashboard.html")

app = webapp2.WSGIApplication([
	('/', HomePage),
	('/login', LoginPage),
	('/logout', LogoutPage),
	('/register', RegisterPage),
	('/dashboard', DashboardPage),
	], debug=True)
