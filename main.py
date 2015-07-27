import cgi
#from google.appengine.api import users
from google.appengine.ext import ndb
import os
import webapp2
import jinja2

# STUDENT_CREATE_HTML_FORM = """\
# <html>
#     <body>
#         <form action="/student/create" method="post"
#             <div><input type="text" name="firstname" placeholder="First Name"</div>
#             <div><input type="text" name="lastname" placeholder="Last Name"</div>
#             <div><input type="text" name="age" placeholder="Age"</div> 
#             <div><input type="text" name="student numbber" placeholder="Student Number"</div> 
#             <div><input type="text" name="course" placeholder="Course"</div> 
#             <div><input type="submit" value="create student"></div>
#         </form>
#     </body>
# </html>
#"""

jinja_env = jinja2.Environment(
    loader =  jinja2.FileSystemLoader(os.path.dirname(__file__)))

class AddStudent(ndb.Model):
    firstname = ndb.TextProperty(required=True)
    lastname = ndb.TextProperty(required=True)
    age = ndb.StringProperty()
    st_no = ndb.TextProperty(required=True)
    course = ndb.TextProperty(required=True)
    date_created = ndb.DateTimeProperty(auto_now_add=True)



class MainPage(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template('index.html')
        self.response.out.write(
            template.render())

class ActionSuccess(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template('success.html')
        self.response.out.write(
            template.render())

class StudentCreate(webapp2.RequestHandler):
    def get(self):
        #self.response.write(STUDENT_CREATE_HTML_FORM)

        template = jinja_env.get_template('create.html')
        self.response.out.write(
            template.render())

    def post(self):
        add = AddStudent(
            firstname=cgi.escape(self.request.get('firstname')),
            lastname=cgi.escape(self.request.get('lastname')),
            age=cgi.escape(self.request.get('age')),
            st_no=cgi.escape(self.request.get('student numbber')),
            course=cgi.escape(self.request.get('course')),
            )
        add.put()
        self.redirect('/success')

class StudentList(webapp2.RequestHandler):
    def post(self):

        students = AddStudent.query()

        self.response.write('<html><body><h1>List of students</h1>')
        self.response.write('<table border="2" style="width:80%">')
        self.response.write('<tr>')
        self.response.write('<td><b> FIRSTNAME </b></td>')
        self.response.write('<td><b> LASTNAME </b></td>')
        self.response.write('<td><b> AGE </b></td>')
        self.response.write('<td><b> STUDENT NUMBER </b></td>')
        self.response.write('<td><b> COURSE </b></td>')
        self.response.write('</tr>')
        
        for student in students:
            self.response.write('<tr>')
            self.response.write('<td> %s </td>' % cgi.escape(student.firstname))
            self.response.write('<td> %s </td>' % cgi.escape(student.lastname))
            self.response.write('<td> %s </td>' % cgi.escape(student.age))
            self.response.write('<td> %s </td>' % cgi.escape(student.st_no))
            self.response.write('<td> %s </td>' % cgi.escape(student.course))
            self.response.write('</tr>')
        self.response.write('</table>')
        self.response.write('</body></html>')




app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/student/create', StudentCreate),
    ('/student/list', StudentList),
    ('/success', ActionSuccess),
], debug=True)