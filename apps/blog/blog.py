import os
import webapp2
import jinja2
from google.appengine.ext import db
from google.appengine.api import memcache
import json
import logging
import time

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

class Post(db.Model):
	subject=db.StringProperty(required = True)
	content=db.TextProperty(required = True)
	created=db.DateTimeProperty(auto_now_add = True)


	def html_content(self):
	# Escape, then convert newlines to br tags, then wrap with Markup object
	# so that the <br> tags don't get escaped.
		def escape(s):
			# unicode() forces the conversion to happen immediately,
			# instead of at substitution time (else <br> would get escaped too)
			return unicode(jinja2.escape(s))
		return jinja2.Markup(escape(self.content).replace('\n', '<br>'))


class NewPostPage(Handler):
	def render_front(self, subject="",  content="", error=""):
		self.render("newpost.html", subject=subject, content=content, error=error)
		
	def get(self):
		self.render_front()

	def post(self):
		subject=self.request.get("subject")
		content=self.request.get("content")

		if subject and content:
			p= Post(subject=subject, content=content)
			p.put()
			blog_id = p.key().id()
			blog_cache(update = True)
			qry_timer(update = True)

			self.redirect("/blog/%d" % blog_id)
		else:
			error="Please fill both Subject and Content"
			self.render_front(subject,content,error)

def blog_cache(source = 'blog_front', update=False, blog_id=0):
	key = source
	blog = memcache.get(key)
	if blog and not update:
		return blog
	elif source =='blog_front':
		logging.error("DB QUERY")
		blog=db.GqlQuery("SELECT * FROM Post ORDER BY created DESC limit 10")
		blog = list(blog)
		memcache.set(key,blog)

	else:
		logging.error("DB QUERY")
		blog = Post.get_by_id(int(blog_id))
		memcache.set(key,blog)
	return blog	

def qry_timer(source = 'blog_front_tmr', update = False):
	key = source
	start_time = memcache.get(key)
	if not start_time or update:
		start_time = time.time()
		memcache.set(key,start_time)
	time_since_qry = time.time() - start_time
	return str(int(time_since_qry))
	


class BlogPage(Handler):
	def get(self):
		blog= blog_cache(source='blog_front' )
		time_since_qry = qry_timer(source='blog_front_tmr')

		self.render("blog.html", blog=blog, time_since_qry = time_since_qry)



class PermaPage(Handler):
	def get(self, blog_id):
		
		blog= blog_cache(source=str('perma_'+blog_id), blog_id = blog_id)
		time_since_qry = qry_timer(source=str('perma_'+blog_id+'_tmr'))
		if not blog:
			self.error(404)
			return

		self.render("permalink.html", blog=blog, time_since_qry = time_since_qry)

def json_writer(blog):
	post=[]

	for record in blog:
		title = record.subject
		content = record.content
		created = record.created.strftime('%a %b %d %H:%M:%S %Y')

		post.append({"subject":title, "content":content,"created":created})

	b = json.dumps(post)
	return b



class JsonHandler(Handler):
	def get(self):
		self.response.headers.add_header("Content-Type","application/json ; charset-UTF-8" )
		blog = db.Query(Post).run(limit=10)
		self.write(json_writer(blog))

class JsonPerma(Handler):
	def get(self, blog_id):
		self.response.headers.add_header("Content-Type","application/json ; charset-UTF-8" )
		blog = Post.get_by_id(int(blog_id))
		if blog:
			self.write(json.dumps({"subject":blog.subject,"content":blog.content,"created":blog.created.strftime('%a %b %d %H:%M:%S %Y')}))
		else:
			self.error(404)
			return
			


class FlushPage(Handler):
	def get(self):
		memcache.flush_all()
		self.redirect('/blog')




