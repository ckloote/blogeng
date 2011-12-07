#!/usr/bin/python2

import web

db = web.database(dbn='mysql', db='blogeng', user='blogeng', pw='bl0g3ng')

def get_blogs():
    return db.select('blog')

def get_blog(userid):
    return db.select('blog', where='userid=$userid', vars=locals())[0]

def get_posts(id):
    try:
        return db.select('post', where='ID=$id', vars=locals())
    except IndexError:
        return None

