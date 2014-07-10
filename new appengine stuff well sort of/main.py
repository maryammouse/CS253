#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import webapp2

form = """
<form method="post">
    What is your birthday?
    <br>
    <label>
        Month
        <input type="text" name="month" value="%(month)s">
    </label>
    <label>
        Day
        <input type="text" name="day" value="%(day)s">
    </label>
    <label>
        Year
        <input type="text" name="year" value="%(year)s">
    </label>
    <div style="color: red">%(error)s</div>
    <br>
    <br>
    <input type="submit">
</form>
"""
def valid_day(self, day):
    if day.isdigit() and int(day) in range(1,32):
        return int(day)
    else:
        return None

months = ['January',
          'February',
          'March',
          'April',
          'May',
          'June',
          'July',
          'August',
          'September',
          'October',
          'November',
          'December']

def valid_month(self, month):
    if month in months:
        return month
    elif month.title() in months:
        return month.title()
    else:
        return None


def valid_year(self, year):
    if year.isdigit() and int(year) in range(1900,2021):
        return int(year)
    else:
        return None





class MainHandler(webapp2.RequestHandler):
    def valid_day(self, day):
        if day.isdigit() and int(day) in range(1,32):
            return int(day)
        else:
            return None

    months = ['January',
            'February',
            'March',
            'April',
            'May',
            'June',
            'July',
            'August',
            'September',
            'October',
            'November',
            'December']

    def valid_month(self, month):
        if month in months:
            return month
        elif month.title() in months:
            return month.title()
        else:
            return None


    def valid_year(self, year):
        if year.isdigit() and int(year) in range(1900,2021):
            return int(year)
        else:
            return None


    def write_form(self, error="", month="", day="", year=""):
        self.response.out.write(form % {'error' : error, 'month' : month, 'day' : day, 'year' : year})
i

    def get(self):
        self.write_form()

    def post(self):
        def escape_html(s):
            to_replace = ['&', '>', '<', '"']
            replacement = {'>' : '&gt;', '<' : '&lt;', '"' : '&quot;', '&': '&amp;'}
            for stuff in to_replace:
                if stuff in s:
                    s = s.replace(stuff, replacement[stuff])
            return s

        user_month = self.request.get('month')
        user_day = self.request.get('day')
        user_year = self.request.get('year')

        month = self.valid_month(user_month)
        day = self.valid_day(user_day)
        year = self.valid_year(user_year)




        if not (month and day and year):
            self.write_form("The text you've entered is invalid.", escape_html(user_month), escape_html(user_day), escape_html(user_year))
            #self.invalid()

        else:
            self.redirect("/thanks")
        #self.response.write("Thanks! That's a totally valid day!")


class ThanksHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("Thanks! That's a totally valid day!")


#class TestHandler(webapp2.RequestHandler):
#    def post(self):
#        q = self.request.get("q")
#        self.response.out.write(q)
#
#        #self.response.headers['Content-Type'] = 'text/plain'
#        #self.response.out.write(self.request)

app = webapp2.WSGIApplication([
    ('/', MainHandler), ('/thanks', ThanksHandler)], debug=True)
