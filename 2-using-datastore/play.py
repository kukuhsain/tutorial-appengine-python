import os
import webapp2
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)


def validate_year(year):
	if year.isdigit():
		year = int(year)

	if year>1900 and year<2020:
		return True
	else:
		return False

class Validation():
	def validate_year(self, year):
		if year.isdigit():
			year = int(year)

		if year>1900 and year<2020:
			return year
		else:
			return False

	def validate_month(self, month):
		months = ('jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec')
		month = month.lower()
		if month in months:
			return month
		else:
			return False

	def validate_day(self, day):
		if day.isdigit():
			day = int(day)

		if day>0 and day<=31:
			return day
		else:
			return False

class People(db.Model):
	name = db.StringProperty(required=True)
	day_birth = db.IntegerProperty(required=True)
	month_birth = db.StringProperty(required=True)
	year_birth = db.IntegerProperty(required=True)

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
		self.render("date-of-birth.html")

	def post(self):
		name = self.request.get('name')
		year = self.request.get('year')
		month = self.request.get('month')
		day = self.request.get('day')

		validated_year = Validation().validate_year(year)
		validated_month = Validation().validate_month(month)
		validated_day = Validation().validate_day(day)

		if validate_year and validated_month and validated_day:
			person = People(name=name, day_birth=validated_day, month_birth=validated_month, year_birth=validated_year)
			person.put()
			self.write("Successful!!!")
		else:
			self.write("Failed!!!")

app = webapp2.WSGIApplication([
	('/', MainPage),
	], debug=True)
