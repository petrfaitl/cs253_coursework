import webapp2
from apps.birthday.verify_date_month import valid_month 
from apps.birthday.verify_date_year import valid_year 
from apps.birthday.verify_date_day import valid_day
from libs.escaping_chars import escape_chars





form = """
<form method="post">
  What is your birthday
  <br>
  <label>Month
  <input type='text' name="month" value="%(month)s"> 
  </label>

  <label>Day
  <input type='text' name="day" value="%(day)s">
  </label>

  <label>Year
  <input type='text' name="year" value="%(year)s">
  </label>

  <div style="color:red">%(error)s</div>

  
  <br>

  <input type="submit">
</form>
"""

class BirthdayHandler(webapp2.RequestHandler):
  def write_form(self, error="", month="", day="", year=""):
    self.response.out.write(form % {"error":error, "month":escape_chars(month), "day":escape_chars(day), "year":escape_chars(year)})

  def get(self):  
      
      self.write_form()

  def post(self):
      user_month = self.request.get('month')
      user_day = self.request.get('day')
      user_year = self.request.get('year')

      month=valid_month(user_month)
      day=valid_day(user_day)
      year=valid_year(user_year)

      if not (month and day and year):
        self.write_form("That doesn't look right to me",
                        user_month,user_day,user_year)
      else:
        self.redirect("/unit2/birthday/thanks")

class ThanksHandler(webapp2.RequestHandler):
  def get(self):
      self.response.out.write("Thanks that's great!")