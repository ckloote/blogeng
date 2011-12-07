#!/usr/bin/python2

import web, os, sys

sys.path.append("/srv/www/blog/htdocs")
from blogeng import *

urls = (
    '/', 'index',
    '/blog/(.*)', 'blog',
    '/register', 'register'
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

class register:
    form = web.form.Form(
        web.form.Textbox('userid', web.form.notnull,
                         size=15,
                         description = "User ID:"),
        web.form.Textbox('password', web.form.notnull,
                         size = 15,
                         description = "Password:"),
        web.form.Textbox('name', web.form.notnull,
                         size=32,
                         description = "Blog Title:"),
        web.form.Button('Register')
    )

    def GET(self):
        form = self.form()
        return render.register(form)

    def POST(self):
        form = self.form()
        if not form.validates():
            return render.new(form)
        new_blog(form.d.userid, form.d.password, form.d.name)
        raise web.seeother('/')

app = web.application(urls, globals(), autoreload=False)
application = app.wsgifunc()
if __name__ == "__main__":
    app.run()

