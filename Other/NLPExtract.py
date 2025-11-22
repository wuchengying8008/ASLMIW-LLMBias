import jieba
import re
import string
import numpy as np
from LAC import LAC
from ltp import LTP
from sklearn.feature_extraction.text import CountVectorizer
def cut_word(sent):
    return " ".join(list(jieba.cut(sent)))

def text_array_find_disorder(inputData):
 # with open("test.txt", "r",encoding='utf-8') as f:
 #   data = [line.replace("\n", "") for line in f.readlines()]
  sentence = re.sub(r'[,，。：:;；\s]', ' ', inputData)
  words = sentence.split()
 # print(words)
  #words = [words.strip() for one in words]
 # print(len(words))
  lis = []
  for temp in words:
    lis.append(cut_word(temp))
  transfer = CountVectorizer()
  trans_data = transfer.fit_transform(lis)
 # print(transfer.get_feature_names())
  return transfer.get_feature_names()
# 输出sparse
#print(trans_data)
# 转为ndarray数组
#print(trans_data.toarray())
def text_array_find_order(inputData):
  sentence = re.sub(r'[,，。：:;；\s]', ' ', inputData)
  words = sentence.split()
  lis =""
  for temp in words:
    lis=lis+" "+cut_word(temp)
  return lis;
def text_judge_type(inputData):
  array_data=text_array_find(inputData)
  #for one in array_data:
def text_array_Number(inputData):
    sentence = re.sub(r'[,，。;；\s]', ' ', inputData)
    words = sentence.split()
    lisNumber = []
    lisStocks = []
    for temp in words:
     pattern = r'\d+\.\d+'
    # print(temp)
     strNumber =""
     if len(re.findall(pattern, temp))>0:
      strNumber =re.findall(pattern, temp)[0]
     if len(strNumber)>0 :
      lisNumber.append(float(strNumber))
      pattern = r"[\u4e00-\u9fa5]+"  # 匹配中文字符的正则表达式
      strText=re.findall(pattern, temp)
      if len(strText)>0 :
        if temp.find("持仓")>=0:
           lisStocks.append(strText[1])
        else:
           lisStocks.append(strText[0])
      else:
        lisStocks.append("其他")
     print(lisNumber)
     print(lisStocks)
    return lisNumber,lisStocks
def find_first_punctuation(s):
    for i, char in enumerate(s):
        if char in string.punctuation:
            return i
def text_find_holder(inputData):
    strFind=""
    numFind=inputData.find("持仓")
    if numFind>=0:
        strFind=inputData[numFind:]
        print(strFind)
        sentence = re.sub(r'[,，。;；\s]', ' ', strFind)
        words = sentence.split()
        for temp in words:
            strNotNumber = ""
            pattern = r'\d+\.\d+'
            if len(re.findall(pattern, temp)) <= 0:
                strNotNumber=temp
                numEndFind = strFind.find(strNotNumber)
                strFind = strFind[:numEndFind]
    return strFind
def extract_name(sentence: str, type='lac'):
    user_name_lis = []
    lac = LAC(mode='lac')
    if type == 'lac':
        _result = lac.run(sentence)
        for _index, _label in enumerate(_result[1]):
            if _label == "PER":
                user_name_lis.append(_result[0][_index])
    elif type == 'ltp':
        _seg, _hidden = ltp.seg([sentence])
        _pos_hidden = ltp.pos(_hidden)
        for _seg_i, _seg_v in enumerate(_seg):
            _hidden_v = _pos_hidden[_seg_i]
            for _h_i, _h_v in enumerate(_hidden_v):
                if _h_v == "nh":
                    user_name_lis.append(_seg_v[_h_i])
    else:
        raise Exception('type not suppose')
    return user_name_lis
def text_find_name(inputData):
    user_name_lis=extract_name(inputData,'lac')
    print('识别的客户姓名为：',user_name_lis)
    return user_name_lis

#text_array_find_order("行业内部企业之间存在较大的竞争差距。我们是不是认识 你是哪里来的")
#text_array_Number("持仓情况：内地股票15.1%,混合型基金:1.8%，银杏可转债65.4%,债券型基金:6.2%,红宝石产品:11.5%")
#text_find_name("华创客户吴小程,女,28岁,硕士学历，年收入50万，投资经验:3年,投资风险偏好：积极型，投资金额2608104.02；持仓情况：内地股票15.1%,混合型基金:1.8%，银杏可转债65.4%,债券型基金:6.2%,红宝石产品:11.5%，帮我分析一下")
#text_find_name("客户庄明，女,28岁,硕士学历，年收入50万，投资经验:3年,投资风险偏好：积极型，投资金额2608104.02；持仓情况：内地股票15.1%,混合型基金:1.8%，银杏可转债65.4%,债券型基金:6.2%,红宝石产品:11.5%，帮我分析一下")
