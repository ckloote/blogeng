#!/usr/bin/python2

import web, os, sys

sys.path.append("/srv/www/blog/htdocs")
from blogeng import *

urls = (
    '/', 'index',
    '/post/(\d+)', 'post',
    '/add', 'add',
#    '/edit(\d+)', 'edit',
#    '/delete(\d+)', 'delete'
)

rootdir = os.path.abspath(os.path.dirname(__file__)) + '/'
render = web.template.render(rootdir + 'templates/', base='layout')

class index:
    def GET(self):
        posts = getPosts()
        return render.index(posts)

class post:
    def GET(self,postid):
        post = getPost(postid)
        return render.post(post)

class add:
    form = web.form.Form(
        web.form.Textbox('title', web.form.notnull,
                         size=32,
                         description = "Post Title:"),
        web.form.Textarea('body', web.form.notnull,
                          rows=30, cols=80,
                          description = "Post Body:"),
        web.form.Button("Post Entry")
    )

    def GET(self):
        form = self.form()
        return render.add(form)

    def POST(self):
        form = self.form()
        if not form.validates():
            return render.add(form)
        addPost(form.d.title, form.d.body)
        raise web.seeother('/')

app = web.application(urls, globals(), autoreload=False)
application = app.wsgifunc()
if __name__ == "__main__":
    app.run()
