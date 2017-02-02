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
import webapp2, re

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
            <input type="text" name="username" value="%s">
            <span class="error">%s</span>
        <br>
        <label>Password</label>
            <input type="password" name="password">
            <span class="error">%s</span>
        <br>
        <label>Verify Password</label>
            <input type="password" name="verify">
            <span class="error">%s</span>
        <br>
        <label>Email (optional)</label>
            <input type="text" name="email" value="%s">
            <span class="error">%s</span>
        <br>
            <input type="submit">
    </form>
"""

footer = """
    </body>
</html>
"""

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

# class MainHandler(webapp2.RequestHandler):
#     def render(self, **params):
#         self.response.out.write(render_str(**params))
#
#     def get(self):
#         self.response.write(header + form + footer)
#
#     #def post(self):
#     #    self.response.write("Hello, World!")

class UserSignup(webapp2.RequestHandler):
    def get(self):
        #set values to blank while page loads
        username = ""
        email = ""
        error_username = ""
        error_password = ""
        error_verify = ""
        error_email = ""
        self.response.write(header + form % (username, error_username, error_password, error_verify, email, error_email) + footer)

    def post(self):
        #declare variables for the user inputs
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        #set error values to False and blank before user inputs
        error = False
        error_username = ""
        error_password = ""
        error_verify = ""
        error_email = ""

        #confirm if valid username
        if not valid_username(username):
            error_username = "That is not a valid username"
            error = True
        #confirm if valid password
        if not valid_password(password):
            error_password = "That is not a valid password"
            error = True
        #confirm if passwords match
        elif password != verify:
            error_verify = "The passwords do not match"
            error = True
        #confirm if valid email
        if not valid_email(email):
            error_email = "That is not a valid email"
            error = True

        #if there is an error, re-render the page and show the errors
        if error:
            self.response.write(header + form % (username,error_username,error_password,error_verify,email,error_email) + footer)
        #if no error, navigate to welcome page
        else:
            self.redirect('/welcome?username=' + username)

#create a Welcome page for successful user signup
class Welcome(webapp2.RequestHandler):
    def get(self):
        username = self.request.get("username")
        self.response.write("<h1>Welcome, " + username + "</h1>")

app = webapp2.WSGIApplication([
    #('/', MainHandler),
    ('/signup', UserSignup),
    ('/welcome', Welcome)
], debug=True)
