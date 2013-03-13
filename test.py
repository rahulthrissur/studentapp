import webapp2
from google.appengine.ext import db
from google.appengine.ext.webapp import template

class student(db.Model):
	Name = db.StringProperty()
	Age = db.StringProperty()
	Sex = db.StringProperty()
	Mark = db.StringProperty()

class MainPage(webapp2.RequestHandler):
	def get(self):
      		self.response.headers['Content-Type'] = 'html'
      		self.response.write("""<html>
					<body>
					<p><a href="/details"> Add a student details</a></p>
					<p><a href="/sort1"> Details of All students sorted by age </a></p>
					<p><a href="/sort2"> Details of All students sorted by mark</a></p>
					<p><a href="/remove"> Remove details of a student </a></p>
					<p><a href="/search"> Search details of a student </a></p>
					<body>
			      	       </html>""")

class details(webapp2.RequestHandler):
	def get(self):
		self.response.out.write(template.render("test.html",{}));
	def post(self):
		name=self.request.get('student_name')
		sex=self.request.get('sex')
		age=self.request.get('age')
		mark=self.request.get('mark')
		data=student(key_name =name, Name=name, Sex=sex, Age=age, Mark=mark)
		data.put()
		self.redirect("/")

class sort1(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text'
		self.response.write("Details of all student sorted by Age")
		data = db.GqlQuery('SELECT * FROM student ORDER BY Age ASC')

		self.response.headers['Content-Type'] = 'text/plain'			
		for i in data:
      			self.response.write('\n'+i.Name +' '+i.Sex+' '+i.Age+' '+i.Mark+ '\n')

class sort2(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text'
		self.response.write("Details of all student sorted by Marks  ")
		data = db.GqlQuery('SELECT * FROM student ORDER BY Mark DESC')

		self.response.headers['Content-Type'] = 'text/plain'			
		for i in data:
      			self.response.write('\n'+i.Name +' '+i.Sex+' '+i.Age+' '+i.Mark+ '\n')


class remove(webapp2.RequestHandler):
	def get(self):
      		self.response.headers['Content-Type'] = 'html'
      		self.response.write("""<html>
					<body>
					<form action='/remove' method="post">	
					<div> Student Name <input type="text" name = "remove" ></input></div>
					<div><input type="submit" value="submit"></div>
					</form>		
					</body></html>""")
	def post(self):
		remove=self.request.get('remove')
		address_k = db.Key.from_path('student', remove)
		db.delete(address_k)

class search(webapp2.RequestHandler):		
	def get(self):
		self.response.headers['Content-Type'] = 'html'
      		self.response.write("""<html>
					<body>
					<form action='/searchresult' method="post">	
					<div> Student Name <input type="text" name = "search" ></input></div>
					<div><input type="submit" value="submit"></div>
					</form>		
					</body></html>""")
      		
		
class searchresult(webapp2.RequestHandler):
	def post(self):
		search=self.request.get('search')
		data = db.GqlQuery("""SELECT * FROM student WHERE Name = :1 """, search)
		self.response.headers['Content-Type'] = 'text/plain'			
		for i in data:
      			self.response.write(i.Name +' '+i.Sex+' '+i.Age+' '+i.Mark+ '\n')	

app = webapp2.WSGIApplication([('/', MainPage),('/details', details), ('/sort1', sort1), ('/sort2', sort2), ('/search', search), ('/remove', remove), ('/searchresult', searchresult)],
                              debug=True)
