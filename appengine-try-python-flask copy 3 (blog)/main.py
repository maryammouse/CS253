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
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class MainPage(Handler):

    def get(self):
        blogs = db.Query(Blog)
        blogs = blogs.order('-created')
        blogs = blogs.fetch(10)
        self.render("homepage.html", blogs=blogs)

class NewBlog(Handler):

    def render_form(self, subject="", content="", error=""):
        self.render("newpost.html", subject=subject, content=content, error=error)

    def get(self):
        self.render_form()

    def post(self):
        subject = self.request.get('subject')
        content = self.request.get('content')

        if subject and content:
            b = Blog(subject=subject, content=content)
            b.put()

            self.redirect("/blog/specific?entry=" + str(b.key()))

        else:
            error = "We need both a title and content!"
            self.render_form(subject=subject, content=content, error=error)


class SpecificEntry(Handler):
    def get(self):
        blog_id = self.request.get('entry')
        blog = Blog.get(blog_id)

        self.render("entry.html", blog=blog)



app = webapp2.WSGIApplication([('/blog', MainPage),
                               ('/blog/newpost', NewBlog),
                               ('/blog/specific', SpecificEntry)],
                              debug=True)
