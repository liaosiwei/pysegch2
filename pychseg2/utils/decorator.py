'''
Created on 2013-8-1

@author: siwei
'''
import functools

def coroutine(func):
    @functools.wraps(func)
    def start(*args, **kwargs):
        g = func(*args, **kwargs)
        g.__next__()
        return g
    return start

if __name__ == '__main__':
    pass