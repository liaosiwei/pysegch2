'''
Created on 2013-7-27

@author: siwei
'''
import sqlite3

class FormatData(object):
    '''
    classdocs
    '''


    def __init__(self, db_name):
        '''
        Constructor
        '''
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()
        