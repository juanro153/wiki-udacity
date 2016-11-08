import jinja2
import webapp2
import re
import BaseHandler
import UserFront
from google.appengine.ext import db
import User
import logging
from google.appengine.api import memcache
#https://github.com/cherylcourt/cs253/tree/master/templates

def render_content(content):
    return content.replace('\n', '<br>')

class WikiPosts(db.Model):
  pagename = db.StringProperty(required=True)
  content = db.TextProperty(required=True)
  created = db.DateTimeProperty(auto_now_add=True)
  lastTimeModified = db.DateTimeProperty(auto_now=True)
  writtenBy = db.StringProperty(required=True)
  lastModifiedBy = db.StringProperty(required=True)
  
   
class EditPage(BaseHandler.Handler):
  def get(self, pagename):
    if not self.user:             
      self.redirect("/login")

    page = WikiPosts.all().filter('pagename =', pagename).order('-created').get()
    content = ""
    newpage = True
    if page:
      content = page.content
      newpage = False
    self.renderEdit(content=content, newpage = newpage, editing = True)
    
  def post(self, pagename):
    if not self.user:             
      self.error(400)
      return
		
    content = self.request.get('content')
    #content = render_content(content)
    page = WikiPosts.all().filter('pagename =', pagename).order('-created').get()
		
    if not page:
      writtenBy = self.user.name
    else:
      writtenBy = page.writtenBy
			
    lastModifiedBy = self.user.name

    if content:
      w = WikiPosts(pagename = pagename, content = content, writtenBy = writtenBy, lastModifiedBy = lastModifiedBy)
      w.put()
      self.redirect(w.pagename)
    else:
      self.renderEdit(content=content, error="content please", pagename = pagename)
  

  def renderEdit(self, newpage, editing, content="", error=""):
    self.render("edit.html", content=content, error=error, newpage=newpage, editing = editing)

class WikiPage(BaseHandler.Handler):
    def get(self, pagename):
      page = WikiPosts.all().filter('pagename =', pagename).order('-created').get()


      if page:
		content = page.content

		self.render("wiki.html", content = content, pagename = pagename)

      else:
        edit_url = '/_edit' + pagename
        self.redirect(edit_url)
        
class History(BaseHandler.Handler):
	def get(self, pagename):
		q =  WikiPosts.all().filter('pagename =', pagename).order('-created')
		q.fetch(limit = 100)

		posts = list(q)
		if posts:
			self.render("history.html", pagename = pagename, posts = posts)
		else:
			self.redirect("/_edit" + pagename)

PAGE_RE = r'(/(?:[a-zA-Z0-9_-]+/?)*)'
app = webapp2.WSGIApplication([('/signup', UserFront.Signup),
                              ('/login', UserFront.Login),
                               ('/logout', UserFront.Logout),
                               ('/_edit' + PAGE_RE, EditPage),
                               ('/_history'+ PAGE_RE, History),
                               (PAGE_RE, WikiPage),
								], debug=True)
