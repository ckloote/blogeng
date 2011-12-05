#!/usr/bin/python2

import web, os

urls = (
    '/(.*)', 'index'
)

rootdir = os.path.abspath(os.path.dirname(__file__)) + '/'
render = web.template.render(rootdir + 'templates/')

class index:
    def GET(self, name):
        return render.index(name)


app = web.application(urls, globals(), autoreload=False)
application = app.wsgifunc()
if __name__ == "__main__":
    app.run()

