#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2, re, cgi

header = """
<!DOCTYPE html>
<html>
    <head>
        <title>User Signup</title>
        <style type="text/css">
            .error {
                color: red;
            }
        </style>
    </head>
    <body>
        <h1>Signup</h1>

"""

form = """
    <form method="post">
        <label>Username</label>
            <input type="text" name="username" value="{username}">
            <span class="error">{username_error}</span>
        <br>
        <label>Password</label>
            <input type="password" name="password" value="">
            <span class="error">{password_error}</span>
        <br>
        <label>Verify Password</label>
            <input type="password" name="verify" value="">
            <span class="error">{verify_error}</span>
        <br>
        <label>Email (optional)</label>
            <input type="text" name="email" value="{email}">
            <span class="error">{email_error}</span>
        <br>
            <input type="submit">
    </form>
"""

footer = """
    </body>
</html>
"""

class MainHandler(webapp2.RequestHandler):
     def render(self, **params):
         content = header + form.format(**params) + footer
         self.response.write(content)
         #self.response.write(header + form.format(username="",username_error="",password_error="",verify_error="",email="",email_error="") + footer)
#     def get(self):
#         self.response.write(header + form + footer)

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

#class UserSignup(webapp2.RequestHandler):
class UserSignup(MainHandler):
    def get(self):

        #params = username=username,username_error=error_username,password_error=error_password,verify_error=error_verify,email=email,email_error=error_email
        params = {"username":"","username_error":"","password_error":"","verify_error":"","email":"","email_error":""}
        self.render(**params)

    def post(self):
        #declare variables for the user inputs
        username = cgi.escape(self.request.get("username"))
        password = cgi.escape(self.request.get("password"))
        verify = cgi.escape(self.request.get("verify"))
        email = cgi.escape(self.request.get("email"))

        #set error values to False before user inputs
        error = False

        params = dict(username = username,
                      email = email,
                      username_error = "",
                      password_error = "",
                      verify_error = "",
                      email_error = "")

        #confirm if valid username
        if not valid_username(username):
            params["username_error"] = "That is not a valid username"
            #username_error = "That is not a valid username"
            error = True
        #confirm if valid password
        if not valid_password(password):
            params["password_error"] = "That is not a valid password"
            #password_error = "That is not a valid password"
            error = True
        #confirm if passwords match
        elif password != verify:
            params["verify_error"] = "The passwords do not match"
            #verify_error = "The passwords do not match"
            error = True
        #confirm if valid email
        if not valid_email(email):
            params["email_error"] = "That is not a valid email"
            #email_error = "That is not a valid email"
            error = True

            #params = {"username":cgi.escape(username),"username_error":username_error,"password_error":password_error,"verify_error":verify_error,"email":cgi.escape(email),"email_error":email_error}

        #if there is an error, re-render the page and show the errors
        if error:
                #params = {"username":username,"username_error":username_error,"password_error":password_error,"verify_error":verify_error,"email":email,"email_error":email_error}
            self.render(**params)
                #self.response.write(header + form.format(username=username,username_error=error_username,password_error=error_password,verify_error=error_verify,email=email,email_error=error_email) + footer)
                #self.response.write(header + form.format(username=username) % (error_username,error_password,error_verify,email,error_email) + footer)
        #if no error, navigate to welcome page
        else:
            self.redirect('/welcome?username=' + cgi.escape(username))

#create a Welcome page for successful user signup
class Welcome(webapp2.RequestHandler):
    def get(self):
        username = self.request.get("username")
        self.response.write("<h1>Welcome, " + cgi.escape(username) + "</h1>")

app = webapp2.WSGIApplication([
    #('/', MainHandler),
    ('/signup', UserSignup),
    ('/welcome', Welcome)
], debug=True)
