import pymysql as pmq
import NLPConstant
def getMysqlDataCursor(type):
   con = pmq.connect(host=NLPConstant.MYSQL_HOST,
                  port=NLPConstant.MYSQL_PORT,
                  user=NLPConstant.MYSQL_USER,
                  password=NLPConstant.MYSQL_PASSWORD,
                  database=NLPConstant.MYSQL_DATABASE)
   return con
def execute_query(sql):
 conn = getMysqlDataCursor(0)
 cur = conn.cursor()
 cur.execute(sql)
 data = cur.fetchall()
 return data

#sql="select lowest_price  from market_data where stock_code='#stockcode'"
#execute_query(sql.replace("#stockcode", "600570"))