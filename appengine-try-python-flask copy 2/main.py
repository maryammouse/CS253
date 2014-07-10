import os
import webapp2
import jinja2

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


class Blog(db.Model):
    title = db.StringProperty(required = True)
    blog = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class MainPage(Handler):

    def render_front(self, title="", created="", blog=""):
        self.render("homepage.html", title = title, created = created, blog = blog)

    def get(self):
        self.render_front()

class NewBlog(Handler):

    def render_form(self, title="", blog="", error=""):
        self.render("newblog.html", title = title, blog = blog, error = error)

    def get(self):
        self.render_front()

    def post(self):
        title = self.request.get("title")
        blog = self.request.get("blog")

        if not (title and blog):
            self.render_form(title = title, blog = blog, error="We need both a title and blog content!")
        else:
            a = Blog(title = title, blog = blog)
            a.put()

            self.redirect("/blog")








app = webapp2.WSGIApplication([('/blog', MainPage), ('/newpost', NewBlog)], debug=True)
