#!/usr/bin/env python3
import os
import tornado.ioloop
import tornado.web
import tornado.log
import json

import requests

from jinja2 import \
  Environment, PackageLoader, select_autoescape

ENV = Environment(
  loader=PackageLoader('weather', 'templates'),
  autoescape=select_autoescape(['html', 'xml'])
)

class TemplateHandler(tornado.web.RequestHandler):
  def render_template (self, tpl, context):
    template = ENV.get_template(tpl)
    self.write(template.render(**context))

class MainHandler(TemplateHandler):
  def get (self):
    self.render_template('weatherForm.html', {})

  def post (self):
    pass
    # get city name
    city = self.get_body_argument('city')
    # lookup the weather
    r = requests.get('http://api.openweathermap.org/data/2.5/weather?q={}&APPID=472c94261251d797427becfeecbcefae'.format(city))
    print(r)
    data = json.loads(r.text)
    print(data)
    # render the weather data
    self.render_template("weatherForm.html", {'data': data})

def make_app():
  return tornado.web.Application([
    (r"/", MainHandler),
    (r"/static/(.*)",
      tornado.web.StaticFileHandler, {'path': 'static'}),
  ], autoreload=True)

if __name__ == "__main__":
    tornado.log.enable_pretty_logging()
    app = make_app()
    app.listen(int(os.environ.get('PORT', '8080')))
    tornado.ioloop.IOLoop.current().start()
