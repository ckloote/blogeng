#!/usr/bin/python2

import web, datetime

db = web.database(dbn='mysql', db='blogeng', user='blogeng', pw='bl0g3ng')

def get_blogs():
    return db.select('blog')

def get_blog(userid):
    return db.select('blog', where='userid=$userid', vars=locals())[0]

def new_blog(userid, password, name):
    db.insert('blog', userid=userid, password=password, name=name)

def get_posts(id):
    try:
        return db.select('post', where='blog=$id', vars=locals())
    except IndexError:
        return None

def new_post(blog, title, body):
    db.insert('post', date=datetime.datetime.utcnow(),
              title=title, blog=blog, body=body)
