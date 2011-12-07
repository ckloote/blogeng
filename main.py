#!/usr/bin/python2

import web, os, sys

sys.path.append("/srv/www/blog/htdocs")
from blogeng import *

urls = (
    '/', 'index',
    '/blog/(.*)', 'blog'
)

rootdir = os.path.abspath(os.path.dirname(__file__)) + '/'
render = web.template.render(rootdir + 'templates/')

class index:
    def GET(self):
        blogs = get_blogs()
        return render.index(blogs)

class blog:
    def GET(self,userid):
        blog = get_blog(userid)
        posts = get_posts(blog.ID)
        return render.blog(blog, posts)

app = web.application(urls, globals(), autoreload=False)
application = app.wsgifunc()
if __name__ == "__main__":
    app.run()

