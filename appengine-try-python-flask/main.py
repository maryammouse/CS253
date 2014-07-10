import os
import webapp2
import jinja2
import hashlib
import random
import string
import re
from google.appengine.ext import db


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

def make_salt():
    return ''.join(random.choice(string.letters) for x in xrange(5))

def make_pw_hash(name, pw=None, salt=None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s|%s|%s' % (str(name), h, salt)

def valid_pw(name, pw, h):
    salt = h.split('|')[2]
    #test_hash = h.split('|')[1]
    #q = db.Query(User)
    #q= q.filter('user =', name)
    #dataname = q.get()
    if make_pw_hash(name, pw, salt) == h:
        return True
    else:
        return False

class User(db.Model):
    user = db.StringProperty(required=True)
    password = db.TextProperty(required=True)


class SignupHandler(Handler):
    def get(self):
        self.render("signup.html",user_input="",
                                    user_error="",
                                    pass_error="",
                                    verify_error="",
                                    email_error="",
                                    email_input="")


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
            if mail:
                return MAIL_RE.match(mail)

        invalid_user, invalid_pass, invalid_verify, invalid_email = "", "", "", ""

        if not valid_username(username):
            invalid_user = "Invalid username"

        if not valid_password(password):
            invalid_pass = "Invalid password"

        if password != verify:
            invalid_verify = "The passwords do not match"

        if not valid_email(email):
            invalid_email = "Invalid email address"

        if invalid_user or invalid_pass or invalid_verify or not(valid_email):
            self.render("signup.html", user_input=escape_html(username),
                                    user_error=escape_html(invalid_user),
                                    pass_error=escape_html(invalid_pass),
                                    verify_error=escape_html(invalid_verify),
                                    email_error=escape_html(invalid_email),
                                    email_input=escape_html(email))
        else:
            #jself.response.headers['Content-Type'] = 'text/plain'
            #user_cookie_str = self.request.cookies.get('user_cookie')
            #if user_cookie_str:
                #validity = valid_pw(username, password, user_cookie_str)
                #if validity:
                    #self.redirect('/welcome')
                #else:
                    #self.redirect('/signup')
                ##if valid we'll want to redirect, but that's for the signup page.
                # in that case, the welcome page should get the cookie and check if its valid
                # the signup page should create one
            #else:
            hashed = make_pw_hash(username, password)
            #hash_word = hashed.split('|')[1]
            instance = db.Query(User)
            data_check = instance.filter('user =', username)
            data_check = data_check.get()
            if not data_check:
                u = User(user = username, password = password)
                u.put()

            self.response.headers.add_header('Set-Cookie', 'user_cookie=%s' % hashed, path="/")
            self.redirect('/welcome')



class WelcomeHandler(Handler):
      def get(self):
        #self.response.headers['Content-Type'] = 'text/plain'
        user_cookie_str = self.request.cookies.get('user_cookie')
        if user_cookie_str:
            username = str(user_cookie_str.split('|')[0])
            q = db.Query(User)
            q = q.filter('user =', username)
            dataname = q.get()
            validity = valid_pw(username, dataname.password, user_cookie_str)
            if validity:
                self.render("welcome.html", user=username, cookie=user_cookie_str)
                ##if valid we'll want to redirect, but that's for the signup page.
                ## in that case, the welcome page should get the cookie and check if its valid
                ## the signup page should create one
            else:
               self.redirect("/signup")
        else:
            self.redirect("/signup")


class LoginHandler(Handler):
    def get(self):
        self.render("login.html", user_input="",
                                user_error="",
                                pass_error="")


    def post(self):
        username=self.request.get('username')
        password=self.request.get('password')

        search=db.Query(User)
        search = search.filter('user =', username)
        search = search.get()

        if not search:
            self.render("login.html", user_input=username,
                                    user_error="Username does not exist!",
                                    pass_error="")

        else:
            if search.password == password:
                hashed = make_pw_hash(username, password)
                self.response.headers.add_header('Set-Cookie', 'user_cookie=%s' % hashed, path="/")
                self.redirect("/welcome")
            else:
                self.render("login.html", user_input=username,
                                        user_error="",
                                        pass_error="That password is incorrect!")


class LogoutHandler(Handler):
    def get(self):
        current_cookie=self.request.cookies.get('user_cookie')
        if current_cookie:
            self.response.headers.add_header('Set-Cookie', 'user_cookie=%s' % '', path="/")
            self.redirect('/signup')



app = webapp2.WSGIApplication([('/signup', SignupHandler),
                               ('/welcome', WelcomeHandler),
                               ('/login', LoginHandler),
                               ('/logout', LogoutHandler)],
                              debug=True)

