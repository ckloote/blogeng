"""
config.py - Fairly straighforward class for pulling values
from a YAML config file
"""

import yaml

class config(object):
    # Constructor pulls all values from the file
    def __init__(self, rootdir):
        object.__init__(self)
        stream = file(rootdir + 'conf/blogeng.yaml', 'r')
        config = yaml.load(stream)
        stream.close()
        self.__title    = config['title']
        self.__author   = config['author']
        self.__authpass = config['authpass']
        self.__tz       = config['tz']
        self.__db       = config['db']
        self.__user     = config['user']
        self.__pw       = config['pw']

    # Getters for config values
    def getTitle(self):
        return self.__title

    def getAuthor(self):
        return self.__author

    def getAuthpass(self):
        return self.__authpass

    def getTZ(self):
        return self.__tz

    def getDB(self):
        return self.__db

    def getUser(self):
        return self.__user

    def getPW(self):
        return self.__pw

    # Declare as properties 
    title    = property(fget = getTitle)
    author   = property(fget = getAuthor)
    authpass = property(fget = getAuthpass) 
    tz       = property(fget = getTZ)
    db       = property(fget = getDB)
    user     = property(fget = getUser)
    pw       = property(fget = getPW)

