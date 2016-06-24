import webapp2

form = """
<form method="post">
	<h1>Date of Birth</h1>
	<p>Day: <input name="day"></p>
	<p>Month: <input name="month"></p>
	<p>Year: <input name="year"></p>
	<input type="submit">
</form>
"""

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

class MainPage(webapp2.RequestHandler):
	def get(self):
		# self.response.headers['Content-Type'] = 'text/plain'
		self.response.out.write(form)

	def post(self):
		# self.response.out.write("Thanks bro")
		result_year = validate_year(self.request.get('year'))
		result_month = validate_month(self.request.get('month'))
		result_day = validate_day(self.request.get('day'))
		
		self.response.out.write(result_year+result_month+result_day)

app = webapp2.WSGIApplication([
	('/', MainPage),
	], debug=True)
