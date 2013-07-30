# coding=UTF-8
'''
Created on 2013-7-30

@author: siwei
'''

from utils.dbquery import DatabaseQuery

def get_chunk(file, num):
    return file.read(num)

def simple_match(file):
    '''
    @param file: file-objects
    '''
    query = DatabaseQuery('../utils/ChStatic.sql')
    word_len = query.maxlengthbigram()
    word_read_len = word_len
    res = get_chunk(file, word_read_len)
    chunk = res
    while chunk:
        if query.isbigram(chunk):
            word_read_len = word_len
            yield chunk
        else:
            for i in range(len(chunk)-1):
                if query.isbigram(chunk[:-1-i]):
                    word_read_len = word_len - i - 1
                    yield chunk[:-1-i]
                    break
            else: 
                word_read_len = 1
                yield chunk[0]
        if res:
            res = get_chunk(file, word_read_len)
        chunk = chunk[word_read_len:] + res
        word_len = len(chunk)
        
    query.quit()
        
        

if __name__ == '__main__':
    import io
    sample_str = '''习近平指出，要坚决贯彻落实中央和军委有关作风建设规定，持之以恒、锲而不舍，善始善终、善做善成，不断把作风建设引向深入，以良好作风推动部队全面建设。要认真落实标准更高、走在前列的要求，扎扎实实抓好党的群众路线教育实践活动，深入基层、深入官兵，广泛听取意见建议，搞好专项整治。各级党委和领导既是组织者也是参与者，要坚持以上率下，把自己摆进去，从自身严起，从现在改起，从小事抓起，用实际行动为部队做好样子。要组织好团以上领导和机关干部下连当兵、蹲连住班，通过这种方式改进工作作风、密切官兵关系、加强基层建设，把部队基础打得更加牢固。'''
    strs = io.StringIO(sample_str)

    res = simple_match(strs)
    for word in res:
        print (word)
    strs.close()
    