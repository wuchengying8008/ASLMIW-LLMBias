#sys
IMAGE_PATH ='D:\logo\logo.png'
IMAGE_PATH2='D:\logo\logo2.png'
LSTM_DEV_PATH='D:\\dev.txt'
OUT_FILE_PATH='D:\\'
#system
STOCK_HODE=['持仓','金额']
#LSTM
LSTM_LABELS_NUM=2

#Mysql
MYSQL_HOST='192.168.1.177'
MYSQL_PORT=3306
MYSQL_USER='stocktest'
MYSQL_PASSWORD = 'stockTest@123'
MYSQL_DATABASE = 'stock_match_test'

#TODO 容器内用这个
# MYSQL_HOST='10.86.0.43'
# MYSQL_PORT=30055
# MYSQL_USER='hczqjavadoc'
# MYSQL_PASSWORD = 'hczqjavadoc!2!'
# MYSQL_DATABASE = 'stock_match_test'

#es 本地
# ES_HOST='192.168.4.151'
# ES_PORT=9200
# ES_USER='elastic'
# ES_PASSWORD='elastic@123'
# ES_SSL_CONTEXT='D:\\tools\elasticsearch\elasticsearch-8.17.0\config\certs\http_ca.crt'

# 测试环境
ES_HOST='192.168.1.129'
ES_PORT=9200
ES_USER='elastic'
ES_PASSWORD='Hchz@2025'
ES_SSL_CONTEXT='D:\\tools\elasticsearch\combined.crt'

#DeepSeek
DS_URL="https://hczqai.hctest.tech/api/chat/completions"
DS_KRY="sk-3d8c2d9d2d8a4c29a7d6f1b6d7c1a9b"
DS_MODEL="hczqds:32b"