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
import webapp2

from apps.rot13 import rot13
from apps.blog import user_accounts
from apps.birthday import birthday
from apps.ascii_chan import ascii_chan
from apps.blog import blog








class MainHandler(webapp2.RequestHandler):
		def get(self):
				self.response.write('Hello Udacity!')






app = webapp2.WSGIApplication([('/', MainHandler),
															 ('/main/main/main/main', MainHandler),
															 ('/unit2/rot13', rot13.Rot13Handler),
															 ('/unit2/signup', user_accounts.SignupHandler),
															 ('/unit2/welcome', user_accounts.WelcomeHandler),
															 ('/unit2/birthday', birthday.BirthdayHandler),
															 ('/unit2/birthday/thanks', birthday.ThanksHandler),
															 ('/unit3/ascii_chan', ascii_chan.AsciiPage),
															 ('/blog', blog.BlogPage),
															 ('/blog/newpost', blog.NewPostPage),
															 ('/blog/(\d+)', blog.PermaPage),
															 ('/blog/signup', user_accounts.SignupCookieHandler),
															 ('/blog/welcome', user_accounts.WelcomeCookieHandler),
															 ('/blog/login', user_accounts.LoginPage),
															 ('/blog/logout', user_accounts.LogoutPage),
															 ('/blog/.json', blog.JsonHandler),
															 ('/blog/(\d+).json', blog.JsonPerma),
															 ('/blog/flush', blog.FlushPage)
															 ],
															debug=True)
