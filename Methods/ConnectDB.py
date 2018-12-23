import pymysql
from Methods.GetServiceIP import ip

con = pymysql.connect(host='127.0.0.1', user='root', port=3306, database='wuziqi', charset='utf8',password='usbw')
con.autocommit(1)
cursor = con.cursor(cursor=pymysql.cursors.DictCursor)