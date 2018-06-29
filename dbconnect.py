import MySQLdb



import psycopg2
import sys
def connect():
    #con = psycopg2.connect("host='localhost' dbname='partial_translate' user='pt' password='123'")
    con = psycopg2.connect("host='ec2-54-83-23-91.compute-1.amazonaws.com' dbname='d3lbavjjjeu5ma' user='zjazeeigyilrje' password='a72c950323ed6e80fe631b69a6450dfef226d496bb4965307d9ed9376c50a39b' port='5432'")
    c = con.cursor()
    return (c,con)

#
# def connect():
#     conn = MySQLdb.connect(host="localhost",
#                            user = "root",
#                            passwd="67637111Aa",
#                            db = "partial_translate",
#                            charset='utf8',
#                            init_command='SET NAMES UTF8')
#     c = conn.cursor()
#     return c, conn
