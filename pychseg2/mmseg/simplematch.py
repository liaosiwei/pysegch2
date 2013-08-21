# coding=UTF-8
'''
Created on 2013-7-30

@author: siwei
'''

from utils.dbquery import DatabaseQuery, InMemQuery
from utils.decorator import coroutine
import time
import re

class Segmentor(object):
    def __init__(self, db_path):
        self.query = InMemQuery(db_path)
        self.word_len = 8
        self.process_list = []
        
    def filter_punctuation(self, text):
        # TODO: find a better solution for filtering punctuations
        res = re.findall(r'(\w+)[，。“”‘’；：、《》——]*', text)
        return (t for t in res)

    def preprocess(self, text):
        '''to implement'''
        pass
            
    @coroutine
    def recv_text(self, targetalgorithm):
        while True:
            text = (yield)
            self.preprocess(text)
            text_list = self.filter_punctuation(text)
            for t in text_list:
                targetalgorithm.send(t)
        
    @coroutine
    def simple_match(self, targetoutput):
        '''
        for simple max match segmentation algorithm
        '''
        while True:
            pos = 0
            text = (yield)
            chunk = text[pos: pos + self.word_len]
            while chunk:
                if self.query.isbigram(chunk):
                    pos += self.word_len
                    res = chunk
                else:
                    temp_len = len(chunk)
                    for i in range(temp_len-2):
                        if self.query.isbigram(chunk[:-1-i]):
                            pos += temp_len - i - 1
                            res = chunk[:-1-i]
                            break
                    else: 
                        pos += 1
                        res = chunk[0]
                        
                targetoutput.send(res)
                chunk = text[pos: pos + self.word_len]
    
    @coroutine    
    def simple_rmatch(self, targetoutput):
        '''
        for simple reverse max match segmentation algorithm
        '''
        while True:
            text = (yield)
            reslist = []
            pos = len(text) 
            start = pos - self.word_len if pos-self.word_len > 0 else 0
            chunk = text[start:]
            
            while chunk:
                temp_len = len(chunk)
                for i in range(temp_len-1):
                    if self.query.isbigram(chunk[i:]):
                        pos -= temp_len - i
                        res = chunk[i:]
                        break
                else:
                    pos -= 1
                    res = chunk[-1]
                reslist.append(res)
                if pos-self.word_len >= 0:
                    chunk = text[pos-self.word_len: pos]
                elif pos > 0 and pos-self.word_len < 0:
                    chunk = text[:pos]
                    temp_len = pos
                else:
                    break
            reslist.reverse()
            for r in reslist:
                targetoutput.send(r)
        
    def processor(self):
        return self.recv_text(self.simple_rmatch(self.fetch_word()))
    
    def post_process(self, word):
        print(word)
    
    @coroutine
    def fetch_word(self):
        while True:
            word = (yield)
            self.post_process(word)
        
    def exit(self):
        self.query.quit()
        
        

if __name__ == '__main__':
    sample_str = '''习近平指出，要坚决贯彻落实中央和军委有关作风建设规定，持之以恒、锲而不舍，善始善终、善做善成，不断把作风建设引向深入，以良好作风推动部队全面建设。要认真落实标准更高、走在前列的要求，扎扎实实抓好党的群众路线教育实践活动，深入基层、深入官兵，广泛听取意见建议，搞好专项整治。各级党委和领导既是组织者也是参与者，要坚持以上率下，把自己摆进去，从自身严起，从现在改起，从小事抓起，用实际行动为部队做好样子。要组织好团以上领导和机关干部下连当兵、蹲连住班，通过这种方式改进工作作风、密切官兵关系、加强基层建设，把部队基础打得更加牢固。'''
    second_str = '''会议确定以下重点任务：一是加强市政地下管网建设和改造。完善城镇供水设施，提升城市防涝能力。二是加强污水和生活垃圾处理及再生利用设施建设，“十二五”末，城市污水和生活垃圾无害化处理率分别达到85%和90%左右。三是加强燃气、供热老旧管网改造。到2015年，完成8万公里城镇燃气和近10万公里北方采暖地区集中供热老旧管网改造任务。四是加强地铁、轻轨等大容量公共交通系统建设，增强城市路网的衔接连通和可达性、便捷度。加快在全国设市城市建设步行、自行车“绿道”。做好城市桥梁安全检测和加固改造，确保通行安全。五是加强城市配电网建设，推进电网智能化。六是加强生态环境建设，提升城市绿地蓄洪排涝、补充地下水等功能。会议强调，要提高城市建设管理的科学化、规范化、法制化水平。在科学规划和充分论证的基础上，抓紧在建项目施工，加快新项目开工。坚持质量第一，严禁不切实际的“形象工程”、“政绩工程”和滋生腐败的“豆腐渣工程”，真正做到建设为民、惠民，以实际行动取信于民。'''
    test_str = '推进电网智能化'
    s = Segmentor('../utils/ChStatic.sql')
    start_cpu = time.clock()
    start_real = time.time()

    seg = s.processor()
    seg.send(sample_str)
    seg.send(second_str)
#     seg.send(test_str)
#     with open("E:/python/《围城》.txt", 'r', encoding='utf8') as f:
#         seg.send(f.read())
    seg.close()

    end_cpu = time.clock()
    end_real = time.time()
    print("%f real seconds" % (end_real - start_real))
    print("%f CPU seconds" % (end_cpu - start_cpu))
    #print("processing speed is %f KB" % (float(426466)/(end_real - start_real)/1024))
    