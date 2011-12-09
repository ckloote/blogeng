#!/usr/bin/python2

import web, datetime

db = web.database(dbn='mysql', db='blogeng', user='blogeng', pw='bl0g3ng')

def getPosts():
    return db.select('post', order='ID DESC')

def getPost(postid):
    return db.select('post', where='ID=$postid', vars=locals())[0]

def addPost(title, body):
    db.insert('post', date=datetime.datetime.utcnow(),
              title=title, body=body)

def delPost(postid):
    db.delete('post', where='ID=$postid', vars=locals())

def editPost(postid, title, body):
    db.update('post', where='ID=$postid', vars=locals(),
              title=title, body=body)

