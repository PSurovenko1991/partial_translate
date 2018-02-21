import MySQLdb


def connect():
    conn = MySQLdb.connect(host="localhost",
                           user = "root",
                           passwd="67637111Aa",
                           db = "partial_translate",
                           charset='utf8',
                           init_command='SET NAMES UTF8')
    c = conn.cursor()
    return c, conn