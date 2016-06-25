import os

import webapp2
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))

def validate_year(year):
	if year.isdigit():
		year = int(year)

	if year>1900 and year<2020:
		return " Correct Year!!! "
	else:
		return " Wrong Year!!! "

def validate_month(month):
	months = ('jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec')
	month = month.lower()
	if month in months:
		return " Correct Month!!! "
	else:
		return " Wrong Month!!! "

def validate_day(day):
	if day.isdigit():
		day = int(day)

	if day>0 and day<=31:
		return " Correct Day!!! "
	else:
		return " Wrong Day!!! "

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
		# self.response.headers['Content-Type'] = 'text/plain'
		self.render("date-of-birth.html")

	def post(self):
		# self.response.out.write("Thanks bro")
		result_year = validate_year(self.request.get('year'))
		result_month = validate_month(self.request.get('month'))
		result_day = validate_day(self.request.get('day'))
		
		self.write(result_year+result_month+result_day)

app = webapp2.WSGIApplication([
	('/', MainPage),
	], debug=True)
