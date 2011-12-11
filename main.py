"""
main.py - Controller for MVC Blog Engine using web.py
"""

import web, os, sys, base64, datetime

# Set path to our custom modules and import them
rootdir = os.path.abspath(os.path.dirname(__file__)) + '/'
sys.path.append(rootdir)
from blogeng import *
from config import *

# Get the config
config = config(rootdir)

# Time zone conversion
def adjTZ(date):
    return date + datetime.timedelta(hours=config.tz)

# Define location of templates, base template, and
# export time zone function to templates for use
render = web.template.render(rootdir + 'templates/', base='layout',
                             globals={'adj': adjTZ})

# Checks for valid auth
def checkAuth(auth_header):
    # If no auth info is sent, fail
    if auth_header is None:
        return False
    else:
        # Pulls user/pass from auth header
        auth = auth_header.split(" ")[1]
        user, password = base64.decodestring(auth).split(':')

        # Pass if auth matches config, else fail
        if (user == config.author) and (password == config.authpass):
            return True
        else:
            return False

# Tell browser to ask for auth
def forceAuth():
    realm = "Basic realm=" + config.title
    web.header('WWW-Authenticate', realm)
    web.ctx.status = '401 Unauthorized'
    return

# Set up hash of valid application URLs
urls = (
    '/', 'index',
    '/post/(\d+)', 'post',
    '/add', 'add',
    '/delete/(\d+)', 'delete',
    '/edit/(\d+)', 'edit',
    '/addcomment/(\d+)', 'addcomment',
    '/delcomments/(\d+)', 'delcomments'
)

# Main Index Page
class index:
    def GET(self):
        # Get all posts, sent to index view
        posts = getPosts()
        return render.index(config.title, config.author, posts)

# Individual Post Page
class post:
    def GET(self,postid):
        # Get specific post, all attached comments,
        # send to post view
        post = getPost(postid)
        comments = getComments(postid)
        return render.post(post, comments)

# Add comment page
class addcomment:
    # Define "add comment" form
    form = web.form.Form(
        web.form.Textbox('author', web.form.notnull,
                         size=32,
                         description = "Name:"),
        web.form.Textarea('body', web.form.notnull,
                          rows=15, cols=80,
                          description = "Comment:"),
        web.form.Button("Post Comment")
    )

    # Send form to addcomment view
    def GET(self, postid):
        form = self.form()
        return render.addcomment(form)

    # Process input, add new comment to DB
    def POST(self, postid):
        form = self.form()
        if not form.validates():
            return render.addcomment(form)
        addComment(postid, form.d.author, form.d.body)
        url = '/post/' + postid
        raise web.seeother(url)

# Delete Comments action
class delcomments:
    def POST(self, postid):
        # Admin action - check for auth
        if (checkAuth(web.ctx.env.get('HTTP_AUTHORIZATION'))) is True:
            # Delete all checked comments
            comments = web.input(ids=[])
            delComments(comments.ids)
            url = "/edit/" + postid
            raise web.seeother(url)
        else:
            forceAuth()

# Add Post
class add:
    # Define add post form
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
        # Admin page - Check for auth - send form to add view 
        if (checkAuth(web.ctx.env.get('HTTP_AUTHORIZATION'))) is True:
            form = self.form()
            return render.add(form)
        else:
            forceAuth()

    def POST(self):
        # Check for auth, process form, add post to DB
        if (checkAuth(web.ctx.env.get('HTTP_AUTHORIZATION'))) is True:
            form = self.form()
            if not form.validates():
                return render.add(form)
            addPost(form.d.title, form.d.body)
            raise web.seeother('/')
        else:
            forceAuth()

# Delete post action
class delete:
    def POST(self,postid):
        # Admin action - check for auth, delete post 
        if (checkAuth(web.ctx.env.get('HTTP_AUTHORIZATION'))) is True:
            delPost(postid)
            raise web.seeother('/')
        else:
            forceAuth()

# Edit post 
class edit:
    def GET(self,postid):
        # Check for auth, send edit form to edit view 
        if (checkAuth(web.ctx.env.get('HTTP_AUTHORIZATION'))) is True:
            post = getPost(postid)
            comments = getComments(postid)
            form = add.form()
            form.fill(post)
            return render.edit(post, form, comments)
        else:
            forceAuth()

    def POST(self,postid):
        # Check for auth, update edited post
        if (checkAuth(web.ctx.env.get('HTTP_AUTHORIZATION'))) is True:
            form = add.form()
            post = getPost(postid)
            if not form.validates():
                return render.edit(post, form)
            editPost(postid, form.d.title, form.d.body)
            raise web.seeother('/')
        else:
            forceAuth()

# Create application object
app = web.application(urls, globals(), autoreload=False)

# Required for mod_wsgi
application = app.wsgifunc()

# Run app
if __name__ == "__main__":
    app.run()

