# -*- coding: utf-8 -*-
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import os
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.ext.db import GeoPt

class Entry(db.Model):
    title = db.StringProperty()
    latlng = db.GeoPtProperty()
    author = db.UserProperty()
    content = db.StringProperty(multiline=True)
    created = db.DateTimeProperty(auto_now_add=True)
    updated = db.DateTimeProperty(auto_now=True)
    schema_version = db.IntegerProperty()


class MainPage(webapp.RequestHandler):
    
    def get(self):
        template_values = {}
        path = os.path.join(os.path.dirname(__file__),'index.html')
        self.response.out.write(template.render(path,template_values))


class EditMarkerPage(webapp.RequestHandler):
    
    def get(self):
        template_values = {}
        path = os.path.join(os.path.dirname(__file__),'edit_marker.html')
        self.response.out.write(template.render(path,template_values))


class UpdateMarkerPage(webapp.RequestHandler):
    
    def get(self):
        self.redirect('/editmarker')
        
    def post(self):
        key = self.request.get('key')
        try:
            entry = Entry.get(key)
        except:
            entry = Entry()

        entry.title = self.request.get('title');
        lat_str = self.request.get('lat');
        lng_str = self.request.get('lng');
        entry.latlng = GeoPt(float(lat_str), float(lng_str))
        entry.content = self.request.get('content');
        
        entry.put()
        
        self.redirect('/editmarker')


class DeleteMarkerPage(webapp.RequestHandler):
    
    def get(self):
        self.redirect('/editmarker')
        
    def post(self):
        key = self.request.get('key');
        try:
            entry = Entry.get(key)
            entry.delete()
        except:
            pass
        
        self.redirect('/editmarker')



class JsonPage(webapp.RequestHandler):
    
    def get(self):

#        entry1 = Entry(title='エントリ１', latlng=GeoPt(35.680655,139.767036), author=None, 
#                       content='コンテンツHTML', schema_version=1) 
#        entry2 = Entry(title='エントリ２', latlng=GeoPt(35.690625,139.699788), author=None, 
#                       content='コンテンツHTML2', schema_version=1) 
#
#        entries = [entry1, entry2]
        entries = Entry.all()

        template_values = {}
        template_values['entries'] = entries
        path = os.path.join(os.path.dirname(__file__),'json.html')
        self.response.out.write(template.render(path,template_values))
        

application = webapp.WSGIApplication([('/', MainPage),
                                      ('/editmarker', EditMarkerPage),
                                      ('/updatemarker', UpdateMarkerPage),
                                      ('/deletemarker', DeleteMarkerPage),
                                      ('/json', JsonPage),
                                      ], debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
