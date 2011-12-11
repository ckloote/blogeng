#!/usr/bin/python2

import web, os, sys, base64, datetime

rootdir = os.path.abspath(os.path.dirname(__file__)) + '/'
sys.path.append(rootdir)
from blogeng import *
from config import *

config = config(rootdir)

def adjTZ(date):
    return date + datetime.timedelta(hours=config.tz)

render = web.template.render(rootdir + 'templates/', base='layout',
                             globals={'adj': adjTZ})

def checkAuth(auth_header):
    if auth_header is None:
        return False
    else:
        auth = auth_header.split(" ")[1]
        user, password = base64.decodestring(auth).split(':')
        if (user == config.author) and (password == config.authpass):
            return True
        else:
            return False

urls = (
    '/', 'index',
    '/post/(\d+)', 'post',
    '/add', 'add',
    '/delete/(\d+)', 'delete',
    '/edit/(\d+)', 'edit',
    '/addcomment/(\d+)', 'addcomment',
    '/delcomments/(\d+)', 'delcomments',
    '/login', 'login'
)

class index:
    def GET(self):
        posts = getPosts()
        return render.index(config.title, config.author, posts)

class post:
    def GET(self,postid):
        post = getPost(postid)
        comments = getComments(postid)
        return render.post(post, comments)

class addcomment:
    form = web.form.Form(
        web.form.Textbox('author', web.form.notnull,
                         size=32,
                         description = "Name:"),
        web.form.Textarea('body', web.form.notnull,
                          rows=15, cols=80,
                          description = "Comment:"),
        web.form.Button("Post Comment")
    )

    def GET(self, postid):
        form = self.form()
        return render.addcomment(form)

    def POST(self, postid):
        form = self.form()
        if not form.validates():
            return render.addcomment(form)
        addComment(postid, form.d.author, form.d.body)
        url = '/post/' + postid
        raise web.seeother(url)

class delcomments:
    def POST(self, postid):
        if (checkAuth(web.ctx.env.get('HTTP_AUTHORIZATION'))) is True:
            comments = web.input(ids=[])
            delComments(comments.ids)
            url = "/edit/" + postid
            raise web.seeother(url)
        else:
            raise web.seeother('/login')

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
        if (checkAuth(web.ctx.env.get('HTTP_AUTHORIZATION'))) is True:
            form = self.form()
            return render.add(form)
        else:
            raise web.seeother('/login')

    def POST(self):
        if (checkAuth(web.ctx.env.get('HTTP_AUTHORIZATION'))) is True:
            form = self.form()
            if not form.validates():
                return render.add(form)
            addPost(form.d.title, form.d.body)
            raise web.seeother('/')
        else:
            raise web.seeother('/login')

class delete:
    def POST(self,postid):
        if (checkAuth(web.ctx.env.get('HTTP_AUTHORIZATION'))) is True:
            delPost(postid)
            raise web.seeother('/')
        else:
            raise web.seeother('/login')

class edit:
    def GET(self,postid):
        if (checkAuth(web.ctx.env.get('HTTP_AUTHORIZATION'))) is True:
            post = getPost(postid)
            comments = getComments(postid)
            form = add.form()
            form.fill(post)
            return render.edit(post, form, comments)
        else:
            raise web.seeother('/login')

    def POST(self,postid):
        if (checkAuth(web.ctx.env.get('HTTP_AUTHORIZATION'))) is True:
            form = add.form()
            post = getPost(postid)
            if not form.validates():
                return render.edit(post, form)
            editPost(postid, form.d.title, form.d.body)
            raise web.seeother('/')
        else:
            raise web.seeother('/login')

class login:
    def GET(self):
        if (checkAuth(web.ctx.env.get('HTTP_AUTHORIZATION'))) is True:
            raise web.seeother('/')
        else:
            realm = "Basic realm=" + config.title
            web.header('WWW-Authenticate', realm)
            web.ctx.status = '401 Unauthorized'
            return
        
app = web.application(urls, globals(), autoreload=False)
application = app.wsgifunc()
if __name__ == "__main__":
    app.run()

