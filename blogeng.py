#!/usr/bin/python2

import web, os, sys, datetime

rootdir = os.path.abspath(os.path.dirname(__file__)) + '/'
sys.path.append(rootdir)
from config import *
config = config(rootdir)

db = web.database(dbn='mysql', db=config.db, user=config.user, pw=config.pw)

def getPosts():
    return db.select('posts', order='id DESC')

def getPost(postid):
    return db.select('posts', where='id=$postid', vars=locals())[0]

def addPost(title, body):
    db.insert('posts', date=datetime.datetime.utcnow(),
              title=title, body=body)

def delPost(postid):
    commentids = []
    comments = getComments(postid)
    for comment in comments:
        commentids.append(comment.id)
    delComments(commentids)
    db.delete('posts', where='id=$postid', vars=locals())

def editPost(postid, title, body):
    db.update('posts', where='id=$postid', vars=locals(),
              title=title, body=body)

def getComments(postid):
    return db.select('comments', where='post_id=$postid', order='id',
                     vars=locals())

def addComment(postid, author, body):
    db.insert('comments', date=datetime.datetime.utcnow(),
              post_id=postid, author=author, body=body)

def delComments(commentids):
    for commentid in commentids:
        db.delete('comments', where='id=$commentid', vars=locals())

