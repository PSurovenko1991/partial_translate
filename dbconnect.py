import MySQLdb


def connect():
    conn = MySQLdb.connect(host="localhost",
                           user = "root",
                           passwd="67637111Aa",
                           db = "partial_translate")
    c = conn.cursor()
    return c, conn