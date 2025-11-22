import spacy
import NLPExtract
import NLPLSMT
import EnterpriseBase
from collections import Counter
import re
import sys
import os
import time
import numpy as np
from operator import itemgetter
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, './Utils'))
sys.path.append(os.path.join(current_dir, './STOCK'))
sys.path.append(os.path.join(current_dir, './COMPANY'))
from DataBase import getMysqlDataCursor,execute_query
import NLPConstant
import SQLUtil
import stockLine
import stockPrice
import stockHode
import PromptTool
import equityStructure
sys.path.append(os.path.join(current_dir, './MARKET'))
import demostic,globalInfo,industryInfo,mainRank,stockRankC,stockRankM

def judge_question_intention(inputData):
 sentence = re.sub(r'[,，。;；\s]', ' ', inputData)
 words = sentence.split()
 arrSen = []
 i=0;
 if len(inputData)<=20:
    arrSen.append(NLPExtract.text_array_find_order(inputData))
 else:
  for temp in words:
   if i==0:
    tempstr = words[0]
   if i>1 and len(tempstr)<=20:
      tempstr=tempstr+temp
   if len(tempstr)>20:
    arrSen.append(NLPExtract.text_array_find_order(tempstr))
    tempstr=""
   i=i+1
 print(arrSen)
 arrPrediction = NLPLSMT.LSTM_Prediction(arrSen)
 print("=========================")
 print("识别的标签:",arrPrediction)
 return arrPrediction
def contains_string(list_of_strings, target_string):
    return target_string in list_of_strings
def AI_intention_judge(inputData):
    arrList = []
    arrInfo = []
    promptTag=""
    ###判别分析上市公司的基础分析
    companyName = revise_question_CompanyName(inputData)
    if len(companyName) > 0:
        # 判断是不是大类分析
        promptTag = PromptTool.find_tag_prompt(inputData)
        if len(promptTag) > 0:
            arrList.append(-1)
    if len(arrList)<1:
     try:
      arrPrediction=judge_question_intention(inputData)
      arrList = list(dict.fromkeys(arrPrediction))
     except Exception as e:
      print(arrList)
      arrInfo=[]
    current_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
    if 5 in arrList: #个股 找股票代码
      stock_Code,stock_Name=revise_question_stockcode(inputData)
      if len(stock_Code)>0:
       fileName='ST'+current_time+'.png'
       stockLine.StockLine(NLPConstant.OUT_FILE_PATH+fileName, stock_Code, stock_Name, '0');
       arrInfo.append('5' + '|' + NLPConstant.OUT_FILE_PATH+fileName + '||0|||')
       fileName ='ST'+current_time+'.html'
       stockPrice.draw_Kline(NLPConstant.OUT_FILE_PATH+fileName, stock_Code, stock_Name, 0);
       arrInfo.append('1' + '|' + NLPConstant.OUT_FILE_PATH+fileName + '||0|||')
    if 4 in arrList or inputData.find("持仓")>=0: #识别持仓情况
        #用户名称
       user_name=revise_question_customerName(inputData)
        #股票代码
       stock_Code, stock_Name = revise_question_stockcode(inputData)
       bars, values=revise_question_stockhode(inputData)
       print('持仓产品',bars)
       print('持仓金额', values)
       if len(values) > 0:
           fileName = 'SH' + current_time + '.png'
           stockHode.stockHodeBar(NLPConstant.OUT_FILE_PATH + fileName,  bars, values, '0');
           arrInfo.append('5' + '|' + NLPConstant.OUT_FILE_PATH + fileName + '||0|||')
       if len(user_name)>0:
           fileName = 'SH' + current_time + '.pdf'
           arrInfo.append('6' + '|' + NLPConstant.OUT_FILE_PATH + fileName + '|'+user_name+'|0|'+stock_Code+'|1|')
    if 2 in arrList :  # 市场分析
       #市场监测
       fileName =  current_time + '.png'
       globalInfo.GloablInfo(NLPConstant.OUT_FILE_PATH +'1SM'+ fileName, '0');
       arrInfo.append('8' + '|' + NLPConstant.OUT_FILE_PATH +'1SM'+ fileName + '||0|||')
       demostic.StockDemostic(NLPConstant.OUT_FILE_PATH + '2SM' + fileName, '0');
       arrInfo.append('8' + '|' + NLPConstant.OUT_FILE_PATH + '2SM' + fileName + '||0|||')
       industryInfo.StockIndustry(NLPConstant.OUT_FILE_PATH + '3SM' + fileName, '0');
       arrInfo.append('8' + '|' + NLPConstant.OUT_FILE_PATH + '3SM' + fileName + '||0|||')
       mainRank.MainRank(NLPConstant.OUT_FILE_PATH + '4SM' + fileName, '0');
       arrInfo.append('8' + '|' + NLPConstant.OUT_FILE_PATH + '4SM' + fileName + '||0|||')
       stockRankC.stockRankC(NLPConstant.OUT_FILE_PATH + '5SM' + fileName, '0');
       arrInfo.append('8' + '|' + NLPConstant.OUT_FILE_PATH + '5SM' + fileName + '||0|||')
       stockRankM.stockRankM(NLPConstant.OUT_FILE_PATH + '6SM' + fileName, '0');
       arrInfo.append('8' + '|' + NLPConstant.OUT_FILE_PATH + '6SM' + fileName + '||0|||')
       fileName = 'SM' + current_time + '.pdf'
       arrInfo.append('6' + '|' + NLPConstant.OUT_FILE_PATH + fileName + '||0||2|')
    if 0 in arrList : #上市公司分析
        #企业名称
       #companyName=revise_question_CompanyName(inputData)
       if len(companyName)>0:
           fileName = 'EN' + current_time + '.png'
           equityStructure.equityStructure(NLPConstant.OUT_FILE_PATH + fileName,"",companyName, '0');
           #stockHode.stockHodeBar(NLPConstant.OUT_FILE_PATH + fileName, bars, values, '0');
           arrInfo.append('5' + '|' + NLPConstant.OUT_FILE_PATH + fileName + '|'+companyName+'|0|||')
           fileName = 'EN' + current_time + '.pdf'
           arrInfo.append('8' + '|' + NLPConstant.OUT_FILE_PATH + fileName + '|'+companyName+'|0|'+'|1|')
       else:
           arrInfo.append('当前知识库中未找到相关企业信息，请核对输入的企业名称是否正确。若问题仍未解决，请联系管理员补充或更新企业信息，以拓展知识库内容。这将帮助我更好地进行分析和推理，为您提供更准确的服务。')
    if -1 in arrList : #上市公司8大类分析
           strU='-1' + '|'+promptTag+'|'+companyName+'|0|'+'|1|'
           arrInfo.append(strU)
    print('arrInfo:'+str(arrInfo))
    return arrInfo
def find_most_frequent_element(arr):
    counter = Counter(arr)
    most_frequent_element, _ = max(counter.items(), key=lambda item: item[1])
    return most_frequent_element
def revise_question_stockcode(inputData):
 pattern=r'\d+'
 matchArr=re.findall(pattern,inputData)
 findArr=[]
 findArrCode=[]
 findArrName = []
 for one in matchArr:
    if len(one)==6:
        findArr.append(one)
 print('检索的股票代码',findArr)
 data = execute_query(SQLUtil.STOCK_NAME_LIST)
 for row in data:
     if inputData.find(str(row[0]))>=0:
         findArrName.append(row[0])
         findArrCode.append(row[1])
     for one in findArr:
         if str(row[1]).find(one) >= 0:
             findArrName.append(row[0])
             findArrCode.append(row[1])
 stock_Code =""
 stock_Name =""
 if len(findArrCode)>0:
  counts = Counter(findArrCode)
  print(counts)
  stock_Code=find_most_frequent_element(findArrCode)
  stock_Name=find_most_frequent_element(findArrName)
  print('识别最多的那个股票：',find_most_frequent_element(findArrCode))
 return stock_Code,stock_Name
#识别客户持仓
def revise_question_stockhode(inputData):
 # 提取持仓信息
 textHode=NLPExtract.text_find_holder(inputData)
 print('持仓话术：',textHode)
 lisNumber=[]
 lisStocks =[]
 # 提取文字和数字
 if len(textHode)>0:
  lisNumber,lisStocks=NLPExtract.text_array_Number(textHode)
 return lisNumber,lisStocks

#识别客户名称
def revise_question_customerName(inputData):
    user_name=NLPExtract.text_find_name(inputData)
    print('username',user_name)
    if len(user_name)>0 :
      return user_name[0]
    else:
      return ''
#识别企业名称
def revise_question_CompanyName(inputData):
    print('companyname1')
    data = execute_query(SQLUtil.COMPANY_LIST)
    print('companyname12')
    company_name=EnterpriseBase.find_companyName(inputData)
    print('companyname2',company_name)
     #识别是不是别名
    for one in data:
         if inputData.find(one[1]) >=0 or inputData.find(one[2]) >=0 or inputData.find(one[3]) >=0 :
            return one[1]
    if len(company_name) > 0:
          if one[1].find(company_name) >=0  or one[3].find(company_name) >=0:
              return one[1]
          nameList=NLPExtract.cut_word(company_name).split()
          print('companyname3', company_name)
          companyList={}
          company_=''
          companycount=[]
          count=0
          dataComapny=EnterpriseBase.find_simility_string(company_name,data)
          print('companyname4', company_name)
          n=0
          list_o=['公司','有限公司']
          while (n < len(nameList)):
            print("名称此", nameList)
            if dataComapny.find(nameList[n]) >= 0 and nameList[n] not in list_o:
              company_=dataComapny
              count = count + 1;
            n=n+1;
          if count>0:
            return company_
    else :
          return ""
    return ""

# print('Predicted class:', prediction[0])
#AI_intention_judge("最新股票600570恒生电子行情怎么样,最新行情数据,我想看下最新的股票，帮我分析下现有的持仓，你能帮我分析下吗,请全面分析")
#AI_intention_judge('华创客户曾小程,女,28岁,硕士学历，年收入50万，投资经验:3年,投资风险偏好：积极型，投资金额2608104.02；持仓情况：内地股票15.1%,混合型基金:1.8%，银杏可转债65.4%,债券型基金:6.2%,红宝石产品:11.5%,想投资恒生电子股票600570，请帮她分析一下')
#revise_question_stockcode('恒生电子600570,的最新行情')
#AI_intention_judge("请帮我分析光线传媒的股权情况")
#revise_question_CompanyName("福建软件有限公司成立于1987年，华创公司是一家全球领先的信息通信技术华创公司（ICT）解决方案供应商。")
#AI_intention_judge("华创客户曾小程,女,28岁,硕士学历，年收入50万，投资经验:3年,投资风险偏好：积极型，投资金额2608104.02；持仓情况：内地股票15.1%,混合型基金:1.8%，银杏可转债65.4%,债券型基金:6.2%,红宝石产品:11.5%,想投资恒生电子股票600570，请帮她分析一下")
