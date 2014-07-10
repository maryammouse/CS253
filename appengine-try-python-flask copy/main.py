#!/usr/bin/env python


from flask import Flask
app = Flask(__name__)
app.config['DEBUG'] = True

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

import webapp2
import codecs

form = """
<form method="post">
<textarea name="text">
</textarea>
<br>
<br>
<input type="submit">
"""

@app.route('/')

class MainHandler(webapp2.RequestHandler):
    def write_form(self, text=""):
        self.response.out.write(form)


    def get(self):
        self.write_form(self)


    def post(self):
        text = self.request.get("text")
        self.write_form(self, text.encode("rot13"))



#def hello():
    #"""Return a friendly HTTP greeting."""
    #return 'Hello Udacity! Hello all! Connichiwa! Hola! Salaam!'
#


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
