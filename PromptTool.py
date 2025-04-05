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
#import uuid
from operator import itemgetter
from elasticsearch.exceptions import NotFoundError
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, './Utils'))
sys.path.append(os.path.join(current_dir, './STOCK'))
sys.path.append(os.path.join(current_dir, './COMPANY'))
sys.path.append(os.path.join(current_dir, './Agent/company'))
from DataBase import getMysqlDataCursor,execute_query
import NLPConstant
import SQLUtil
import stockLine
import stockPrice
import stockHode
import equityStructure
from ESUtil import get_elasticsearch_client, index_document, search_elasticsearch, get_document
sys.path.append(os.path.join(current_dir, './MARKET'))
import demostic,globalInfo,industryInfo,mainRank,stockRankC,stockRankM
from SerialBase import textSerial
import stockTool

def cerateDoc(companyName, content):
    return {
        "companyName": companyName,
        "content": content
    }
def ceratePrompt(tag, content, prompt, picList):
    return {
        "tag": tag,
        "prompt": content,
        "instruct": prompt,
        "picList": picList
    }

def getDocByCompanyName(companyName):
    arrList = []
    try:
        for i in range(1, 9):
            dataType = "{:02d}".format(i)
            # promptText = generateEnterprisePrompt(dataType, companyName)
            res = generateCompanyPrompt(dataType, companyName)
            arrList.append(res)
        # summary = "总体客观评价"+companyName+'在治理结构、净资产、商业模式和产品数据方面的表现，以及它的市场竞争力和未来的发展潜力。字数要求在150字左右。'
        # arrList.append(summary)
    except Exception as e:
        print(f"搜索文档时出错：{e}")
    return arrList

def generateAbstract(companyName):
    data = '请给'+companyName+'做一份上市公司分析报告，要求只写提纲，一、治理结构分析 （一）股权数据 （二）治理结构数据 二、净资产数据  （一）资产数据' \
                              '（二）负债数据 三、商业模式数据  （一）盈利能力数据 （二）客户与供应商数据 四、产品数据 （一）产品构成与市场数据 ' \
                              ' （二）生产与研发数据 按照字数在1000字以内'
    return  data;

def generateEnterprisePrompt(tag,companyName):
    data = execute_query(SQLUtil.COMPANY_QUERY.replace("%s", companyName))
    dataPrompt = execute_query(SQLUtil.COMPANY_PROMPT.replace("%s", tag))
    dataContent=queryES("company_analysis", tag, str(data[0][0]))
    promptText=companyName+", "+dataContent+str(dataPrompt[0][0]).replace("%s", companyName)
    return promptText

def generateCompanyPrompt(tag,companyName):
    data = execute_query(SQLUtil.COMPANY_QUERY.replace("%s", companyName))
    dataPrompt = execute_query(SQLUtil.PROMPT_INSTRUCT.replace("%s", tag))
    promptText = [item for sub in dataPrompt for item in sub]
    promptData = [f"{item.replace('%s', companyName)}" for item in promptText]
    dataContent=queryES("company_analysis", tag, str(data[0][0]))
    picList = generatePic(tag, companyName)
    res = ceratePrompt(tag, dataContent, promptData, picList)
    # promptText=companyName+", "+dataContent+str(dataPrompt[0][0]).replace("%s", companyName)
    return res

def generatePic(tag, companyName):
    picNo = execute_query(SQLUtil.PIC_NO.replace("%s", tag)) or []
    picNoStr = ""
    if picNo and len(picNo[0]) > 0:
        picValue = picNo[0][0]
        if picValue is not None:
            picNoStr = str(picValue)
    picNoList = [item.strip() for item in picNoStr.split(',') if item.strip()]
    # 生成图片
    picList = []
    if picNoList:
        for one in picNoList:
            current_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
            fileName = one + current_time + '.png'
            methodName = f"getPic{one}"
            method = getattr(stockTool, methodName, None)
            if method:
                res = method(companyName, fileName)
                if res:
                    picList.append(NLPConstant.OUT_FILE_PATH + fileName)
    return picList

def find_tag_prompt(inputtext):
    data = execute_query(SQLUtil.TAG_QUERY)
    strTag=""
    for one in data:
        if inputtext.find(str(one[0])) >=0:
            strTag=one[1]
            break;
    return strTag

def queryES(indexName, dataType, companyId):
    queryBody = {
        "query": {"bool": {"must": [{"match": {"data_type": dataType}}, {"match": {"company_id": companyId}}]}}
    }
    try:
        res = search_elasticsearch(indexName, queryBody)
        hits = res['hits']['hits']
        all_results = []
        for hit in hits:
            source = hit.get('_source')
            if source:
                try:
                    fieldsToExclude = ["company_name", "company_id", "data_type", "type", "@version", "@timestamp"]
                    result = textSerial(source, fieldsToExclude)
                    all_results.append(result)
                except (TypeError, ValueError) as e:
                    print(f"处理文档时出现错误: {e}")
        # 将每个文档处理后的结果用换行符拼接起来
        contents = "\n".join(all_results)
    except Exception as e:
        print(f"查询过程中出现错误: {e}")
        return ""
    return contents

"""def getDeepSeek(arrList):
    retList=[]
    i=0
    #for one in arrList:0
    i=i+1;
    response=DeepSeekAPI.api_chat_completions("https://hczqai.hctest.tech/api/chat/completions", "sk-3d8c2d9d2d8a4c29a7d6f1b6d7c1a9b",
                         "qwen2.5:0.5b", str(uuid.uuid4()), arrList[0])
    retList.append(response)
    return retList"""
#print(generateNo1("北京光线传媒股份有限公司"))
# queryES("company_analysis", "01", "003")
