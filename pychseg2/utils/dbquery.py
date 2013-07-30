# coding=UTF-8
'''
Created on 2013-7-29

@author: siwei
'''
import sqlite3

class DatabaseQuery(object):
    '''
    use this class to query the database and search for the bigram and character freqency
    '''


    def __init__(self, db_name):
        '''
        Constructor
        '''
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()
        
    def filter(self, table, field):
        res = None
        if table == 'bigram':
            res = self.cur.execute("select * from bigram where Text=:word", {"word": field})
        if table == 'charfreq':
            res = self.cur.execute("select * from charfreq where Text=:char", {"char": field})      
        return res
    
    def isbigram(self, field):
        res = self.filter('bigram', field)
        return True if res.fetchone() else False

    def maxlengthbigram(self):
        res = self.cur.execute("select max(length(Text)) from bigram")
        return res.fetchone()[0]
    
    def quit(self):
        self.conn.close()
            

if __name__ == '__main__':
    t = DatabaseQuery('ChStatic.sql')
    res = t.filter('bigram', '无论如何')
    for row in res:
        print (row) 
    print (t.isbigram("三后"))
    print (t.maxlengthbigram())
    t.quit()