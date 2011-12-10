#!/usr/bin/python2

import web, datetime

db = web.database(dbn='mysql', db='blogeng', user='blogeng', pw='bl0g3ng')

def getPosts():
    return db.select('posts', order='id DESC')

def getPost(postid):
    return db.select('posts', where='id=$postid', vars=locals())[0]

def addPost(title, body):
    db.insert('posts', date=datetime.datetime.utcnow(),
              title=title, body=body)

def delPost(postid):
    db.delete('posts', where='id=$postid', vars=locals())

def editPost(postid, title, body):
    db.update('posts', where='id=$postid', vars=locals(),
              title=title, body=body)

