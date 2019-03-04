#!/usr/bin/env python
import os
import json
import jinja2
import webapp2
from google.appengine.api import users, urlfetch
from models import Message

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))

    def login_user(self):
        anonimous = "Anonimous"
        current_user = users.get_current_user()
        city = "Malaga"
        units = "metric"
        app_key = "43c8c964c71bd02c560bbfa96324a59e"  # enter your own API key from OpenWeatherMap API (openweathermap.org/api)

        url = "http://api.openweathermap.org/data/2.5/weather?q={}&units={}&appid={}".format(city, units, app_key)

        result = urlfetch.fetch(url)

        weather_info = json.loads(result.content)

        # params = {"weather_info": weather_info}

        context = {
            "logged_in": False,
            "login_url": users.create_login_url('/'),
            "user": anonimous,
            "active_tab": None,
            "weather_info": None,
        }

        if current_user:
            context['logged_in'] = True
            context['logout_url'] = users.create_logout_url('/')
            context['user'] = current_user
            context['weather_info'] = weather_info

        return context


class MainHandler(BaseHandler):
    def get(self):
        context = self.login_user()
        return self.render_template("hello.html", params=context)


class MessageReceivedHandler(BaseHandler):
    def get(self):
        context = self.login_user()
        context['active_tab'] = "received"
        return self.render_template("message_list_received.html", params=context)

    def post(self):
        context = self.login_user()
        context['active_tab'] = "received"
        return self.render_template("message_list_received.html", params=context)


class MessageEnviedHandler(BaseHandler):
    def get(self):
        context = self.login_user()
        context['active_tab'] = "envied"
        return self.render_template("message_list_envied.html", params=context)

    def post(self):
        context = self.login_user()
        context['active_tab'] = "envied"
        return self.render_template("message_list_envied.html", params=context)


class MessageDeletedHandler(BaseHandler):
    def get(self):
        context = self.login_user()
        context['active_tab'] = "deleted"
        return self.render_template("message_list_deleted.html", params=context)

    def post(self):
        context = self.login_user()
        context['active_tab'] = "deleted"
        return self.render_template("message_list_deleted.html", params=context)


class HomeListHandler(BaseHandler):
    def get(self):
        return self.render_template("message_list.html")


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/home', HomeListHandler),
    webapp2.Route('/received', MessageReceivedHandler),
    webapp2.Route('/envied', MessageEnviedHandler),
    webapp2.Route('/deleted', MessageDeletedHandler),
], debug=True)
