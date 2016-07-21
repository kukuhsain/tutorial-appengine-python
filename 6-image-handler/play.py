import os
import webapp2
import jinja2

from google.appengine.ext import ndb
from google.appengine.api import images

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

class Photo(ndb.Model):
	title = ndb.StringProperty(required=True)
	image = ndb.BlobProperty()
	datetime_created = ndb.DateTimeProperty(auto_now_add=True)

	@classmethod
	def add_photo(cls, title, image):
		parent = ndb.Key('Admin', 'admin_key')
		note = cls(parent=parent, title=title, image=image)
		note.put()

	@classmethod
	def get_all_photos_data(cls):
		ancestor = ndb.Key('Admin', 'admin_key')
		return cls.query(ancestor=ancestor).order(-cls.datetime_created).fetch()

	@classmethod
	def get_photo(cls, key):
		# ancestor = ndb.Key('Admin', 'admin_key')
		image_key = ndb.Key(urlsafe=key)
		return image_key.get()

	@classmethod
	def delete_single_photo(cls, id):
		parent = ndb.Key('Admin', 'admin_key')
		cls.get_by_id(id=id, parent=parent).key.delete()

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
		photos = Photo.get_all_photos_data()
		self.render("index.html", error=error, previous_value=previous_value, photos=photos)

	def post(self):
		title = self.request.get('title')
		img = self.request.get('img')

		# img = images.resize(img, 32, 32)

		previous_value = {}
		error = {}

		previous_value['title'] = title

		if not title:
			error['title'] = "You need to add title !!!"

		if not img:
			error['img'] = "You need to add image !!!"
		
		if title and img:
			Photo.add_photo(title=title, image=img)

		photos = Photo.get_all_photos_data()
		
		self.render("index.html", error=error, previous_value=previous_value, photos=photos)

class ImageHandler(Handler):
	def get(self):
		img_key = self.request.get('img-id')
		photo = Photo.get_photo(img_key)
		print photo
		if photo:
			self.response.headers['Content-Type'] = 'image/png'
			self.write(photo.image)
			print 'trueeeeeeee'
		else:
			self.response.out.write("No image")
			print 'falseeeeee'

class DeletePage(Handler):
	def get(self):
		self.redirect('/')

	def post(self):
		photo_id = self.request.get('photo-id')
		Photo.delete_single_photo(int(photo_id))
		self.redirect('/')

app = webapp2.WSGIApplication([
	('/', MainPage),
	('/image', ImageHandler),
	('/delete', DeletePage),
	], debug=True)
