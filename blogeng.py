"""
blogeng.py - Model functions for MVC Blog Engine
"""

import web, os, sys, datetime

# Set path to custom modules, get the config
rootdir = os.path.abspath(os.path.dirname(__file__)) + '/'
sys.path.append(rootdir)
from config import *
config = config(rootdir)

# Set up database object
db = web.database(dbn='mysql', db=config.db, user=config.user, pw=config.pw)

# Get all posts
def getPosts():
    return db.select('posts', order='id DESC')

# Get specified post
def getPost(postid):
    return db.select('posts', where='id=$postid', vars=locals())[0]

# Add new post 
def addPost(title, body):
    db.insert('posts', date=datetime.datetime.utcnow(),
              title=title, body=body)

# Delete specified post
def delPost(postid):
    # Better delete attached comments too
    commentids = []
    comments = getComments(postid)
    for comment in comments:
        commentids.append(comment.id)
    delComments(commentids)
    db.delete('posts', where='id=$postid', vars=locals())

# Update specified post
def editPost(postid, title, body):
    db.update('posts', where='id=$postid', vars=locals(),
              title=title, body=body)

# Get comments attached to specified post
def getComments(postid):
    return db.select('comments', where='post_id=$postid', order='id',
                     vars=locals())

# Add comment to a specified post
def addComment(postid, author, body):
    db.insert('comments', date=datetime.datetime.utcnow(),
              post_id=postid, author=author, body=body)

# delete one or more comments
def delComments(commentids):
    for commentid in commentids:
        db.delete('comments', where='id=$commentid', vars=locals())

