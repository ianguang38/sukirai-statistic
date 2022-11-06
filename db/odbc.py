import pymysql

class odbcInstance():
    def __init__(self) -> None:
        self.connection = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            database='sukirai',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        ) 

    def update(self,sql,parameter=None,re=False):
        connection=self.connection
        cursor=connection.cursor()
        cursor.execute(sql,parameter)
        if re:
            print(cursor.rowcount)
            return cursor.fetchall()
        connection.commit()

    def end(self):
        self.connection.close()
