import os
import webapp2
import jinja2
import hashlib

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

CREDENTIAL = {
				'username': 'kukuh',
				'password': 'hunterpass'
			}

def hash_str(s):
	return hashlib.md5(s).hexdigest()

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
		check_password = CREDENTIAL['password'] == self.request.get('password')

		if check_username and check_password:
			self.render("dashboard.html")
		else:
			self.render("login.html")

app = webapp2.WSGIApplication([
	('/', MainPage),
	], debug=True)
