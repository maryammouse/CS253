#!/usr/bin/env python


#from flask import Flask
#app = Flask(__name__)
#app.config['DEBUG'] = True

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

import webapp2
import re
#import codecs

form = """
<form method="post">
<textarea name="text">%(text)s
</textarea>
<br>
<br>
<input type="submit">
"""

tester = """
<form method="post">
    <label>
    Try something!
    </label>
    <input type="text" name="test">
    <input type="submit">
</form>
"""

signup = """
<form method="post">
    <label>
    Username
    </label>
    <input type="text" name="username" value="%(user_input)s"><font color="red">
    %(user_error)s</font>
    <br>
    <label>
    Password
    </label>
    <input type="text" name="password"><font color="red">
    %(pass_error)s</font>
    <br>
    <label>
    Verify Password
    </label>
    <input type="text" name="verify"><font color="red">
    %(verify_error)s</font>
    <br>
    <label>
    Email (optional)
    </label>
    <input type="text" name="email" value="%(email_input)s"><font color="red">
    %(email_error)s</font>
    <br>
    <input type="submit">
</form>
"""
greeting = """
Welcome, %s !
"""

#@app.route('/')

class MainHandler(webapp2.RequestHandler):
    def write_form(self, text=""):
        self.response.out.write(form % {'text': text})


    def get(self):
        self.write_form()


    def post(self):
        written = self.request.get("text")
        self.write_form(written.encode("rot13"))

class TestHandler (webapp2.RequestHandler):
    def post(self):
        self.redirect("/thanks")

    def get(self):
        self.response.out.write(tester)


class ThanksHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("Thanks! If this works, I'm getting somewhere.")


class SignupHandler(webapp2.RequestHandler):

    def write_form(self, user_input="", user_error="", pass_error="", verify_error="", email_error="", email_input=""):
        self.response.out.write(signup % {'user_input' : user_input,
                                          'user_error': user_error,
                                        'pass_error' : pass_error,
                                        'verify_error' : verify_error,
                                        'email_error' : email_error,
                                          'email_input' : email_input})

    def get(self):
        self.write_form()

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')


        def escape_html(s):
            to_replace = ['&', '>', '<', '"']
            replacement = {'>' : '&gt;', '<' : '&lt;', '"' : '&quot;', '&': '&amp;'}
            for stuff in to_replace:
                if stuff in s:
                    s = s.replace(stuff, replacement[stuff])
            return s

        USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")

        PASS_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")

        MAIL_RE = re.compile(r"[^@]+@[^@]+\.[^@]+")


        def valid_username(un):
            return USER_RE.match(un)

        def valid_password(pw):
            return PASS_RE.match(pw)

        def valid_email(mail):
            if email:
                return MAIL_RE.match(mail)
            else:
                return True

        invalid_user, invalid_pass, invalid_verify, invalid_email = "", "", "", ""

        if not valid_username(username):
            invalid_user = "Invalid username"

        if not valid_password(password):
            invalid_pass = "Invalid password"

        if password != verify:
            invalid_verify = "The passwords do not match"

        if not valid_email(email) and not "":
            invalid_email = "Invalid email address"

        if invalid_user or invalid_pass or invalid_verify or (invalid_email):
            self.write_form(escape_html(username), escape_html(invalid_user), escape_html(invalid_pass), escape_html(invalid_verify), escape_html(invalid_email), escape_html(email))
        else:
            url = '/welcome?user=' + username
            self.redirect(url)

class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        username = self.request.get('user')
        self.response.out.write(greeting % username)

#def hello():
    #"""Return a friendly HTTP greeting."""
    #return 'Hello Udacity! Hello all! Connichiwa! Hola! Salaam!'
#

app = webapp2.WSGIApplication([
    ('/', MainHandler), ('/test', TestHandler), ('/thanks', ThanksHandler), ('/signup', SignupHandler), ('/welcome', WelcomeHandler)], debug=True)
#@app.errorhandler(404)
#def page_not_found(e):
#    """Return a custom 404 error."""
#    return 'Sorry, nothing at this URL.', 404
