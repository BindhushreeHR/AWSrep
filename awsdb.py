import pymysql

host="bindhushreedb.cugatrgk9epo.us-east-2.rds.amazonaws.com"
port=3306
dbname="database1"
user="bindhushree"
password="BinMay18!"

connect = pymysql.connect(host, user, password, dbname)
