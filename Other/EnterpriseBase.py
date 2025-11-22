import spacy
import re
import time
from collections import Counter
from Levenshtein import distance

class ChineseNLP:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            start = time.time()
            cls._instance = spacy.load('zh_core_web_sm', disable=['parser', 'ner', 'lemmatizer', 'textcat'])
            print(f"time：{time.time() - start:.4f}s")
        return cls._instance

# 首次加载
nlp = ChineseNLP()

def find_companyName(text):
 doc = nlp(text, disable=['tok2vec', 'tagger'])
 arrList = []
 company=''
 for ent in doc.ents:
    print(ent.text)
    if ent.label_ == 'ORG':  
        arrList.append(ent.text)
 if len(arrList)>0:
     company=arrList[0]
 else:
     pattern = r'[\u4e00-\u9fff]+公司'
     companyL = re.findall(pattern, text)
     if len(companyL)>0:
         company=companyL[0]

 print(company)
 return company

def find_most_frequent_element(arr):
    counter = Counter(arr)
    most_frequent_element, _ = max(counter.items(), key=lambda item: item[1])
    return most_frequent_element

def find_simility_string(string1,data):
   resultStr=""
   similarityOri=100
   string2=[]
   for one in data:
       string2.append(one[1])
   if len(string2)>1:
    for str2 in string2:
     similarity = distance(string1, str2)
     if similarity<similarityOri:
       resultStr=str2
       print("Levenshtein:", similarity)
       print("resultStr:", resultStr)
   similarity2 = distance(string1, string2[0])
   if len(string2) == 1 and similarity2<15:
        resultStr=string2[0]
   return resultStr;



