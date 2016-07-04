import os
import webapp2
import jinja2
import hashlib
import hmac

from google.appengine.ext import db

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

class Handler(webapp2.RequestHandler):
	"""Handler Prototype"""
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))
		

class MainPage(Handler):
	def get(self):
		self.render("login.html")

	def post(self):
		check_username = CREDENTIAL['username'] == self.request.get('username')
		hashed_password = hash_str(self.request.get('password'))
		check_password = CREDENTIAL['hmac_password'] == hashed_password

		if check_username and check_password:
			print make_secure_value(self.request.get('password'))
			self.render("dashboard.html")
		else:
			self.render("login.html")

app = webapp2.WSGIApplication([
	('/', MainPage),
	], debug=True)
