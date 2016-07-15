import os
import webapp2
import jinja2

from google.appengine.ext import ndb

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

class User(ndb.Model):
	username = ndb.StringProperty(required=True)
	datetime_created = ndb.DateTimeProperty(auto_now_add=True)

	@classmethod
	def get_first_user(cls):
		return cls.query().order(cls.datetime_created).fetch()[0]

class Note(ndb.Model):
	title = ndb.StringProperty(required=True)
	content = ndb.TextProperty(required=True)
	datetime_created = ndb.DateTimeProperty(auto_now_add=True)

	@classmethod
	def add_note(cls, title, content):
		note = cls(parent=User.get_first_user().key, title=title, content=content)
		note.put()

	@classmethod
	def get_all_notes(cls):
		return cls.query(ancestor=User.get_first_user().key).order(-cls.datetime_created).fetch()

	@classmethod
	def delete_single_note(cls, id):
		cls.get_by_id(id=id, parent=User.get_first_user().key).key.delete()

class Handler(webapp2.RequestHandler):
	"""Handler Prototype"""
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))
		
class RegisterPage(Handler):
	def get(self):
		self.render("register.html")

	def post(self):
		inputed_username = self.request.get('username')
		new_user = User(username=inputed_username)
		new_user.put()
		self.redirect('/')

class MainPage(Handler):
	def get(self):
		print User.get_first_user()

		previous_value = {}
		error = {}
		notes = Note.get_all_notes()

		self.render("note.html", error=error, previous_value=previous_value, notes=notes)

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
			Note.add_note(title=title, content=content)

		notes = Note.get_all_notes()
		
		self.render("note.html", error=error, previous_value=previous_value, notes=notes)

class DeletePage(Handler):
	def get(self):
		self.redirect('/')

	def post(self):
		note_id = self.request.get('note-id')
		Note.delete_single_note(int(note_id))
		self.redirect('/')

app = webapp2.WSGIApplication([
	('/register', RegisterPage),
	('/', MainPage),
	('/delete', DeletePage),
	], debug=True)
