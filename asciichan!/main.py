import webapp2
import jinja2
import urllib2
import os
import re
import sys
from xml.dom import minidom
#from string import letters


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

IP_URL = "http://api.hostip.info/?ip="
def get_coords(ip):
    #ip = "4.2.2.2"
    url = IP_URL + ip
    content = None
    try:
        content = urllib2.urlopen(url).read()
    except URLError:
        return

def gmaps_img(points):
    url = "http://maps.googleapis.com/maps/api/staticmap?size=380x263&sensor=false"
    for p in points:
        lat = p.lat
        lon = p.lon
        url += "&markers=%s,%s" % (lat, lon)
    return url


    if content:
        d = minidom.parseString(content)
        coords = d.getElementsByTagName("gml:coordinates")
        if coords and coords[0].childNodes[0].nodeValue:
            lon, lat = coords[0].childNodes[0].nodeValue.split(',')
            return db.GeoPt(lat, lon)


class Art(db.Model):
    title = db.StringProperty(required = True)
    art = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    coordinates = db.GeoPtProperty(required = False)

class MainPage(Handler):

    def render_front(self, error="", title="", art="", arts=""):
        arts = db.GqlQuery("SELECT * FROM Art ORDER BY created DESC")
        self.render("front.html", error=error, title=title, art=art, arts=arts)

        # prevent the running of multiple queries
        arts = list(arts)
        points = []
        for art in arts:
            if art.coordinates:
                points.append(art.coordinates)


        IMG_URL=gmaps_img(points)
        if IMG_URL:
            self.render("map.html", map_url = IMG_URL)

        #find which arts have coords
        # if we have any arts coords, make an image url
        # display the image url


    def get(self):
        #self.write(repr(get_coords(self.request.remote_addr)))
        #self.write(self.request.remote_addr)
        return self.render_front()

    def post(self):

        title = self.request.get('title')
        art = self.request.get('art')

        if title and art:
            a = Art(title = title, art = art)
            # lookup user's coordinates from IP
            # if we have them, add them to Art
            coords = get_coords(self.request.remote_addr)
            if coords:
                a.coordinates = coords
#
            a.put()

            self.redirect("/")


        else:
            error = "we need both a title and art!"
            self.render_front(error=error, title=title, art=art)




app = webapp2.WSGIApplication([('/', MainPage)], debug=True)
