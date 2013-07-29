'''
Created on 2013-7-27

@author: siwei
'''
import sqlite3
        

# class Field(object):
#     '''
#     represent the fields in the database
#     TODO: add error-checking codes
#     '''
#     def __init__(self, typename, default=None):
#         self.name = None
#         self.type = typename
#         if default:
#             self.default = default
#         else:
#             self.default = typename()
#     
#     def __get__(self, instance, cls):
#         return getattr(instance, self.name, self.default)
#     
#     def __set__(self, instance, value):
#         if not isinstance(value, self.type):
#             raise TypeError("Must be a %s" % self.type)
#         setattr(instance, self.name, value)
#     
#     def __delete__(self, instance):
#         raise AttributeError("Can't delete attribute")
# 
# 
# class TypeMeta(type):
#     '''
#     define meta class
#     '''
#     def __new__(cls, name, bases, dicts):
#         slots = []
#         for key, value in dicts.items():
#             if isinstance(value, Field):
#                 value.name = "_" + key
#                 slots.append(value.name)
#         dict['__slots__'] = slots
#             
#         return type.__new__(cls, name, bases, dicts)
# 
# 
# class Model(metaclass=TypeMeta):
#     '''
#     define the base class from the meta class
#     '''
#     pass
# 
# class WFreqModel(Model):
#     pass

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

    def create_charfreq_table(self):
        """
        use sql language to create table
        """
        self.cur.execute('''create table charfreq(Text text, Freqency real)''')
    
    def create_bigram_table(self):
        self.cur.execute('''create table bigram(Text text)''')
    
    def read_charfreq(self):
        with open('../dict/CharFreq.txt', 'r', encoding='utf-8') as file:
                accum_freq = 0.
                for line in file:
                    if line.startswith("/*"):
                        continue
                    words = line.split()
                    char = words[1]
                    freq = float(words[3]) - accum_freq
                    accum_freq = float(words[3])
                    yield char, freq
    
    def read_bigram(self):
        with open('../dict/SogouLabDic.dic', 'r', encoding='utf-8') as file:
            for line in file:
                yield (line.split()[0],)
                
    def fill_charfreq_table(self):
        charfreq_iter = self.read_charfreq()
        self.cur.executemany("insert into charfreq(Text, Freqency) values (?, ?)", charfreq_iter)
    
    def fill_bigram_table(self):
        bigram = self.read_bigram()
        self.cur.executemany("insert into bigram(Text) values (?)", bigram)
        
    def save(self):
        self.conn.commit()
        
    def exit(self):
        self.cur.close()
                
if __name__ == '__main__':
    print ('Beginning formating data...')
    t = FormatData('ChStatic.sql')
    t.create_charfreq_table()
    t.fill_charfreq_table()
    t.create_bigram_table()
    t.fill_bigram_table()
    t.save()
    t.exit()
    print ('done!')
    
    
    