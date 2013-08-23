import cgi
import urllib
import webapp2

from google.appengine.ext import ndb
from google.appengine.api import users

class Greeting(ndb.Model):
	author = ndb.UserProperty()
	content = ndb.StringProperty()
	data = ndb.DateTimeProperty(quto_now_add=True)

	@classmethod
	def query_book(cls, ancestor_key):
		return cls.query(ancestor=ancestor_key).order(-cls.date)

class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.out.write('<html><body>')
		questbook_name = self.request.get('guestbook_name')

		ancestor_key = ndb.Key("Book",guestbook_name or "*notitle*")
		greetings = Greeting.query_book(ancestor_key).fetch(20)

		for greeting in greetings:
			if greeting.author:
				self.response.out.write(
						'<b>%s</b> wrote:' % greeting.author.nickname())
			else:
				self.response.out.write(
						'<blockquote>%s</blockquote>' %
						cgi.escape(greeting.content))
		self.response.out.write("""
				<form action "/sign" method="post">
					<input type="hidden" value="%s" name="guestbook_name">
					<div>
						<textarea name="content" row="3" col="60">
						</textarea>
					</div>
					<div>
						<input type="submit" value="Sign Guestbook">
					</div>
				</form>
				<form>
					Guestbook name:<input value="%s" name="guestbook_name">
					<input type="submit" value="switch">
				</form>
				</body>
				</html>""" % (cgi.escape(guestbook_name), cgi.escape(guestbook_name)))

class GuestBook(webapp2.RequestHandler):
	def post(self)
	guestbook_name = self.request.get('guestbook_name')
	greeting = Greeting(parent=ndb.Key("Book", guestbook_name or "*notitle*"),
			content = self.request.get('content'))

	if users.get_current_user():
		greeting.author = users.get_current_user()
	greeting.put()
	self.redirect('/?' + urllib.urlencode({'guestbook_name':guestbook_name}))


app = webapp2.WSGIApplication([('/', MainPage),('/sign', Guestbook)])
