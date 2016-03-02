#      @@@         @@;                 ,@@@@@@`        ,@@          
#      @@@`       @@@;               ,@@     ,@@       @:@,         
#      @@#@      ,@ @;     ,@@'     .@'        @@     @@ +@         
#      @@ @+     @' @;   @@@  ,@@   @@               ,@   @@        
#      @@ .@    @@  @;  +@`     @@  @@               @+   .@,       
#      @@  @@  `@   @;  @@      ,@` @@              @@@@@@@@@       
#      @@   @; @#   @;  @@      ;@  @@`        @@  ,@.      @@      
#      @@   ,@#@    @;  .@+     @@   @@.      @@   @@       ;@,     
#      @@    @@.    @;   .@@@@@@@     :@@@@@@@@   @@         @@     

# By Valerie Najera and Michael Beach 
# HCDE 310 A: Interactive Systems Design And Technology  
# December 17 2015 - Final Project                                                                   
                                
import urllib, urllib2, webbrowser, json
import webapp2
import jinja2
from google.appengine.ext import db
from google.appengine.ext.db import Key
from google.appengine.api import mail
import os
import logging
import csv 

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class Paper(db.Model):
        title = db.StringProperty()
        CA = db.StringProperty()
        author = db.StringProperty()
        #abstract = db.StringProperty(multiline=True)
        notes = db.StringProperty()
        coordinated_action = db.StringProperty()
        synchronicity = db.StringProperty()
        physical_distribution = db.StringProperty()
        scale = db.StringProperty()
        number_of_communities_of_practice = db.StringProperty()
        nascence_one = db.StringProperty()
        nascence_two = db.StringProperty()
        planned_permanence = db.StringProperty()
        turnover = db.StringProperty()
        pdfURLcode = db.StringProperty()
        pgNum = db.StringProperty()
        institution = db.StringProperty()
        session = db.StringProperty()
        geoLocations = db.ListProperty(str)
        
        def populate(self, dict):
            self.title = unicode(dict["Title"].replace("\n"," "),"latin-1")
            self.CA = unicode(dict["CA"].replace("\n"," "),"latin-1")
            self.author = unicode(dict["Author"].replace("\n"," "),"latin-1")
            #self.abstract = unicode(dict["Abstract"].replace("\n"," "),"latin-1")
            self.notes = unicode(dict["NOTES"].replace("\n"," "),"latin-1")
            self.coordinated_action = unicode(dict["Coordinated Action"].replace("\n"," "),"latin-1")
            self.synchronicity = unicode(dict["Synchronicity"].replace("\n"," "),"latin-1")
            self.physical_distribution = unicode(dict["Physical Distribution"].replace("\n"," "),"latin-1")
            self.scale = unicode(dict["Scale"].replace("\n"," "),"latin-1")
            self.number_of_communities_of_practice = unicode(dict["Number of Communities of Practice"].replace("\n"," "),"latin-1")
            self.nascence_one = unicode(dict["Nascence: routine vs nonroutine"].replace("\n"," "),"latin-1")
            self.nascence_two = unicode(dict["Nascence #2: Product & Process"].replace("\n"," "),"latin-1")
            self.planned_permanence = unicode(dict["Planned Permanence"].replace("\n"," "),"latin-1")
            self.turnover = unicode(dict["Turnover"].replace("\n"," "),"latin-1")
            self.pdfURLcode = unicode(dict["PDF URL"].replace("\n"," "),"latin-1")
            self.pgNum = unicode(dict["Page"].replace("\n"," "),"latin-1")
            self.institution = unicode(dict["Institution"].replace("\n"," "),"latin-1")
            self.session = unicode(dict["Session"].replace("\n"," "),"latin-1")
            geoLocations = unicode(dict["Address"].replace("\n",""),"utf-8")
            geo = geoLocations.split(";") 
            self.geoLocations = geo
                    
class DataHandler(webapp2.RequestHandler):
    def get(self):
        q = Paper.all(keys_only=True)
        db.delete(q.fetch(10000))
        mylist = []
        mydict = {}
        moca = csv.DictReader(open("moca-small-final.csv"))
        
        for row_dicts in moca:
            print row_dicts 
            mylist.append(row_dicts)
        paper_list = []
        
        for dict in mylist:
            research_paper = Paper()
            research_paper.populate(dict)
            research_paper.put()
            paper_list.append(research_paper)

        mydict["Result"] = paper_list
        template = JINJA_ENVIRONMENT.get_template('greetform.html')
        self.response.write(template.render(mydict))
    
class PaperHandler(webapp2.RequestHandler):
    def get(self):
        paperid = self.request.get("pgNum")
        q = Paper.all() 
        q.order('title')
        qNum = Paper.all() 
        qNum.order('pgNum')
        template_values = {}
        template_values["papers"] = q
        template_values["papersNum"] = qNum
        template_values["paper"] = paperid
        template = JINJA_ENVIRONMENT.get_template('paper.html')
        self.response.write(template.render(template_values))
 
def send_email(to = "mwb8@uw.edu", subject = "test", body = "see attached file " ):
    mail.send_mail(sender="themichaelbeach@gmail.com",
                    to = to,
                    subject = subject,
                    body = body
                    )

class sendEmail(webapp2.RequestHandler):
    def get(self):
        paperid = self.request.get("pgN")
        message = "http://uw-moca.appspot.com/paper?pgNum=" + paperid
        send_email(subject = "Please take a look at this link, for approval", body = message, to = self.request.get("to"))
        self.response.write('{"message":"Email sent!"}')
        
class MainHandler(webapp2.RequestHandler):
    def get(self):
        q = Paper.all()
        q.order('title') 
        template_values = {}
        template_values["papers"] = q
        template = JINJA_ENVIRONMENT.get_template('greetform.html')
        self.response.write(template.render(template_values))

# for all URLs except alt.html, use MainHandler
application = webapp2.WSGIApplication([ \
                                      ('/loadData', DataHandler),
                                      ('/paper.*', PaperHandler),
                                      ('/sendemail.*', sendEmail),
                                      ('/.*', MainHandler)
                                      ],
                                     debug=True)
