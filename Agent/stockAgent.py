import spacy
from collections import Counter
import re
import sys
import os
import time

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, '../../Utils'))
sys.path.append(os.path.join(current_dir, '../../COMPANY'))
from DataBase import getMysqlDataCursor, execute_query
import NLPConstant
import SQLUtil
from barLine import barLine
from barList import barList
from stockRatio import stockRatio
from lineList import lineList
from barArea import barArea
from groupedBar import groupedBar
from ringBar import ringBar


# 实控人持股比例
def getPic01(companyName, fileName):
    stockName = execute_query(SQLUtil.STOCK_NAME.replace("%s", companyName))
    data = execute_query(SQLUtil.STOCK_RATIO.replace("%s", companyName))
    dataInput = {
        '时间': [],
        '实控人持股比例': []
    }
    if data:
        for row in data:
            dataInput['时间'].append(row[0])
            dataInput['实控人持股比例'].append(row[1])
        barArea(NLPConstant.OUT_FILE_PATH + fileName, dataInput,
                [stockName[0][0] + '实控人持股比例', '时间', '持股比例'], '0')
        return True
    return False


# 董监高薪酬增长率
def getPic02(companyName, fileName):
    stockName = execute_query(SQLUtil.STOCK_NAME.replace("%s", companyName))
    data = execute_query(SQLUtil.MANAGER_SALARY.replace("%s", companyName))
    if data:
        time_list = []
        category_list = []
        category_growth = {}
        for row in data:
            manager_type = row[1]  # 董监高类别
            period = row[2]  # 时间
            growth_rate = row[3]  # 薪酬增长率
            if period not in time_list:
                time_list.append(period)
            if manager_type not in category_list:
                category_list.append(manager_type)
                category_growth[manager_type] = []
            category_growth[manager_type].append(growth_rate)

        # 整理成目标格式
        dataInput = {
            '时间': time_list,
            '薪酬增长率（%）': [category_growth[cat] for cat in category_list],
            '董监高类别': category_list
        }
        lineList(NLPConstant.OUT_FILE_PATH + fileName, dataInput,
                 [stockName[0][0] + '十大股东股权比例', '时间', '薪酬增长率（%）'], '0')
        return True
    return False


# 盈利能力-收入占比
def getPic03(companyName, fileName):
    stockName = execute_query(SQLUtil.STOCK_NAME.replace("%s", companyName))
    data = execute_query(SQLUtil.PROFIT_INCOME.replace("%s", companyName))
    dataInput = {
        '收入来源': [],
        '收入占比（%）': []
    }
    if data:
        for row in data:
            dataInput['收入来源'].append(row[0])
            dataInput['收入占比（%）'].append(row[2])
        stockRatio(NLPConstant.OUT_FILE_PATH + fileName, dataInput, stockName[0][0] + '收入来源占比', '0')
        return True
    return False


# 盈利能力-近五年成本支出
def getPic04(companyName, fileName):
    stockName = execute_query(SQLUtil.STOCK_NAME.replace("%s", companyName))
    data = execute_query(SQLUtil.COST_RATIO.replace("%s", companyName))
    if data:
        yearList = []
        costTypeList = []
        costRatioDict = {}
        for row in data:
            costName = row[0]  # 成本名称
            period = row[1]  # 年份
            costRatio = row[2]  # 成本比例
            if period not in yearList:
                yearList.append(period)
            if costName not in costTypeList:
                costTypeList.append(costName)
                costRatioDict[costName] = []
            costRatioDict[costName].append(costRatio)
        dataInput = {
            '年份': yearList,
            '生产成本（%）': costRatioDict.get('生产成本', []),
            '运营支出（%）': costRatioDict.get('运营支出', []),
            '偶然性支出（%）': costRatioDict.get('偶然性支出', [])
        }
        groupedBar(NLPConstant.OUT_FILE_PATH + fileName, dataInput, stockName[0][0] + '近五年成本支出占比', '0')
        return True
    return False

# 研发能力-研发团队学历占比
def getPic05(companyName, fileName):
    stockName = execute_query(SQLUtil.STOCK_NAME.replace("%s", companyName))
    data = execute_query(SQLUtil.TEAM_EDUCATION.replace("%s", companyName))
    dataInput = {
        '学历': [],
        '学历占比（%）': []
    }
    if data:
        for row in data:
            dataInput['学历'].append(row[0])
            dataInput['学历占比（%）'].append(row[1])
        ringBar(NLPConstant.OUT_FILE_PATH + fileName, dataInput, stockName[0][0] + '研发团队学历占比', '0')
        return True
    return False


#getPic01("宁德时代新能源科技股份有限公司",'1.png')
getPic02("宁德时代新能源科技股份有限公司",'2.png')
getPic03("宁德时代新能源科技股份有限公司",'3.png')
getPic04("宁德时代新能源科技股份有限公司",'4.png')
getPic05("宁德时代新能源科技股份有限公司",'5.png')
