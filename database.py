import pymysql

def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='zctzctzct', # 换成你的密码
        database='cold_chain_db',
        cursorclass=pymysql.cursors.DictCursor
    )