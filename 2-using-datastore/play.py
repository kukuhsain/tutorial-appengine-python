import os
import webapp2
import jinja2

from google.appengine.ext import ndb

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

class Note(ndb.Model):
	title = ndb.StringProperty(required=True)
	content = ndb.TextProperty(required=True)
	datetime_created = ndb.DateTimeProperty(auto_now_add=True)

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
		previous_value = {}
		error = {}
		self.render("note.html", error=error, previous_value=previous_value)

	def post(self):
		title = self.request.get('title')
		content = self.request.get('content')

		previous_value = {}
		error = {}

		previous_value['title'] = title
		previous_value['content'] = content

		if not title:
			error['title'] = "You need to add title !!!"

		if not content:
			error['content'] = "You need to add content !!!"

		if title and content:
			note = Note(title=title, content=content)
			note.put()
			previous_value = {}

		self.render("note.html", error=error, previous_value=previous_value)

app = webapp2.WSGIApplication([
	('/', MainPage),
	], debug=True)
