import os
import webapp2
import jinja2
from google.appengine.api import memcache
from google.appengine.ext import db
from xml.dom import minidom
import urllib2
import logging

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)
	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)
	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))
IP_URL = "http://api.hostip.info/?ip="
def get_coordinates(ip):
	url = IP_URL+ip	
	content = None
	try:
		content = urllib2.urlopen(url).read()
	except URLError:
		return
	if content:
		x = minidom.parseString(content)
		geo= x.getElementsByTagName('gml:coordinates')
		if geo and geo[0].childNodes[0].nodeValue:
			lon,lat = geo[0].childNodes[0].nodeValue.split(",")
			return db.GeoPt(lat,lon)

GMAPS_URL = "http://maps.googleapis.com/maps/api/staticmap?size=380x263&sensor=false&"
key = 'AIzaSyBJG8XVfum9bh_QtmKK6waY_LN95zyHgQI'
def gmaps_img(points):
	markers=''
	for p in points:
		markers = markers+"markers="+str(p.lat)+","+str(p.lon)+"&"
	return GMAPS_URL+markers[:len(markers)-1]+"&"+"key="+key	


class Art(db.Model):
	title=db.StringProperty(required = True)
	art=db.TextProperty(required = True)
	created=db.DateTimeProperty(auto_now_add = True)
	coords=db.GeoPtProperty()


def top_arts(update = False):
	key='top'
	arts = memcache.get(key)
	if arts is None or update:	
		logging.error("DB QUERY")
		arts=db.GqlQuery("SELECT * FROM Art ORDER BY created DESC")
		
		arts = list(arts)
		memcache.set(key, arts)
	return arts

class AsciiPage(Handler):

	def render_front(self, title="",  art="", error=""):
		arts = top_arts()
		img_url = None
		points = filter(None, (a.coords for a in arts))

		if points:
			img_url = gmaps_img(points)


		self.render("front.html", title=title, art=art, error=error, arts = arts, img_url = img_url)
		
	def get(self):
		#self.write(repr(get_coordinates(self.request.remote_addr)))
		self.render_front()

	def post(self):
		title=self.request.get("title")
		art=self.request.get("art")

		if title and art:
			a= Art(title=title, art=art)
			coords = get_coordinates(self.request.remote_addr)
			if coords:
				a.coords = coords

			a.put()
			top_arts(update=True)

			self.redirect("/unit3/ascii_chan")
		else:
			error="We need both title and some art"
			self.render_front(title,art,error)

