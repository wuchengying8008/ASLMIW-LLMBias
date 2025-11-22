import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, './Utils'))
sys.path.append(os.path.join(current_dir, './STOCK'))
sys.path.append(os.path.join(current_dir, './COMPANY'))
from DataBase import getMysqlDataCursor,execute_query
import SQLUtil
from ESUtil import get_elasticsearch_client, index_document, search_elasticsearch, get_document
sys.path.append(os.path.join(current_dir, './MARKET'))

def saveOrUpdateToES(dataType, companyId, newContent):
    es = get_elasticsearch_client()
    query = {
        "query": {
            "bool": {
                "must": [
                    {"match": {"dataType": dataType}},
                    {"match": {"companyId": companyId}}
                ]
            }
        },
        "script": {
            "source": "ctx._source.content = params.newContent",
            "params": {
                "newContent": newContent
            }
        }
    }
    try:
        res = es.update_by_query(index="company_analysis", body=query)
        if len(res.get('failures', [])) > 0:
            return "Failure"
        if res.get('updated', 0) > 0:
            return "Success"
        return "Failure"
    except Exception as e:
        print(f"Failure：{e}")
        return "Failure in ES "

def generateNo1(companyName):
  data = execute_query(SQLUtil.COMPANY_QUERY.replace("%s", companyName))
  baseData = execute_query(SQLUtil.COMPANY_BASE+"'%"+companyName+"%'")
  holderData=execute_query(SQLUtil.COMPANY_HOLDER+"'%"+companyName+"%'")
  baseInfo = str(baseData[0][0]) + ";"
  holderInfo='持股情况如下：'
  for one in holderData:
      holderInfo=holderInfo+str(one[0])
  content = baseInfo + holderInfo + str(baseData[0][1])
  return saveOrUpdateToES("01", str(data[0][0]), content)

def generateNo2(companyName):
    arrList = []
    data = execute_query(SQLUtil.COMPANY_QUERY.replace("%s", companyName))
    positionData = execute_query(SQLUtil.POSITION_BASE.replace("#companyName", "'%" + companyName + "%'"))
    skillData = execute_query(SQLUtil.PROFESSIONAL_SKILL_INFO.replace("#companyName", "'%" + companyName + "%'"))
    managerData = execute_query(SQLUtil.BUSINESS_MANAGER_INFO.replace("#companyName", "'%" + companyName + "%'"))
    holderData = execute_query(SQLUtil.COMPANY_HOLDER + "'%" + companyName + "%'")
    if positionData:
        positionInfo='管理层职务如下：'
        for onePosition in positionData:
            positionInfo = positionInfo + str(onePosition[1]) + "," + str(onePosition[2]) + ";"
        arrList.append(positionInfo)
    if managerData:
        managerInfo='业务分管如下：'
        for oneManager in managerData:
            managerInfo = managerInfo + str(oneManager[0]) + ";"
        arrList.append(managerInfo)
    if holderData:
        holderInfo = '持股情况如下：'
        for one in holderData:
            holderInfo = holderInfo + str(one[0])
        arrList.append(holderInfo)
    if skillData:
        skillInfo='专业技能如下：'
        for oneSkill in skillData:
            skillInfo = skillInfo + str(oneSkill[0]) + "," + str(oneSkill[1]) + ";"
        arrList.append(skillInfo)
    content = '，'.join(arrList)
    return saveOrUpdateToES("02", str(data[0][0]), content)

def generateNo3(companyName):
    data = execute_query(SQLUtil.COMPANY_QUERY.replace("%s", companyName))
    assetData = execute_query(SQLUtil.ASSET_INFO + "'%" + companyName + "%'")
    assetInfo = "资产信息如下："
    for oneAsset in assetData:
        assetInfo = assetInfo + str(oneAsset[0]) + ";"
    return saveOrUpdateToES("03", str(data[0][0]), assetInfo)

def generateNo4(companyName):
    data = execute_query(SQLUtil.COMPANY_QUERY.replace("%s", companyName))
    debitData = execute_query(SQLUtil.DEBIT_INFO + "'%" + companyName + "%'")
    debitInfo = "负债信息如下："
    for oneDebit in debitData:
        debitInfo = debitInfo + str(oneDebit[0]) + ";"
    return saveOrUpdateToES("04", str(data[0][0]), debitInfo)

def generateNo5(companyName):
    data = execute_query(SQLUtil.COMPANY_QUERY.replace("%s", companyName))
    profitData = execute_query(SQLUtil.PROFIT_INFO + "'%" + companyName + "%'")
    profitInfo = "盈利能力信息如下："
    for oneProfit in profitData:
        profitInfo = profitInfo + str(oneProfit[0]) + ";"
    return saveOrUpdateToES("05", str(data[0][0]), profitInfo)

def generateNo6(companyName):
    data = execute_query(SQLUtil.COMPANY_QUERY.replace("%s", companyName))
    clientData = execute_query(SQLUtil.CLIENT_INFO + "'%" + companyName + "%'" + 'HAVING res is not null')
    supplierData = execute_query(SQLUtil.SUPPLIER_INFO + "'" + companyName + "'" + 'HAVING res is not null')
    clientInfo = '客户信息如下：'
    for one in clientData:
        clientInfo = clientInfo + str(one[0]) + ";"
    supplierInfo='供应商信息如下：'
    for one in supplierData:
        supplierInfo = supplierInfo + str(one[0]) + ";"
    content = clientInfo + supplierInfo
    return saveOrUpdateToES("06", str(data[0][0]), content)

def generateNo7(companyName):
    data = execute_query(SQLUtil.COMPANY_QUERY.replace("%s", companyName))
    incomeData = execute_query(
        SQLUtil.PRODUCT_BUSINESS_INFO.replace("#companyName", "'%" + companyName + "%'").replace("#businessType", "1"))
    costData = execute_query(
        SQLUtil.PRODUCT_BUSINESS_INFO.replace("#companyName", "'%" + companyName + "%'").replace("#businessType", "2"))
    rateData = execute_query(
        SQLUtil.PRODUCT_BUSINESS_INFO.replace("#companyName", "'%" + companyName + "%'").replace("#businessType", "3"))
    incomeInfo='产品构成与市场信息如下：营业收入：'
    for oneIncome in incomeData:
        incomeInfo = incomeInfo + str(oneIncome[1]) + ',' + str(oneIncome[3]) + str(oneIncome[2]) + "万元;"
    costInfo='营业成本：'
    for oneCost in costData:
        costInfo = costInfo + str(oneCost[1]) + str(oneCost[3]) + str(oneCost[2]) + "万元;"
    rateInfo='毛利率：'
    for oneRate in rateData:
        rateInfo = rateInfo + str(oneRate[1]) + str(oneRate[3]) + str(oneRate[4] * 100) + "%;"
    content = incomeInfo + costInfo + rateInfo
    return saveOrUpdateToES("07", str(data[0][0]), content)

def generateNo8(companyName):
    arrList = []
    data = execute_query(SQLUtil.COMPANY_QUERY.replace("%s", companyName))
    patentData = execute_query(SQLUtil.PATENT_INFO + "'%" + companyName + "%'" + 'HAVING res is not null')
    writeData = execute_query(SQLUtil.WRITE_INFO + "'%" + companyName + "%'" + 'HAVING res is not null')
    if patentData:
        patentInfo='专利信息如下：'
        for onePatent in patentData:
            patentInfo = patentInfo + str(onePatent[1]) + ";"
        arrList.append(patentInfo)
    if writeData:
        writeInfo='软件/作品著作权信息如下：'
        for oneWrite in writeData:
            writeInfo = writeInfo + str(oneWrite[1]) + ";"
        arrList.append(writeInfo)
    content = '，'.join(arrList)
    return saveOrUpdateToES("08", str(data[0][0]), content)
