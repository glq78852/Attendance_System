# 测试专用文件

from Utils import Connect_DataBase

db, cursor = Connect_DataBase.connect_db('attendance_system')
sql = "INSERT INTO f_user_p(管理员姓名,管理员账号,管理员密码) SELECT 管理员姓名,管理员账号,AES_ENCRYPT(管理员密码,'mysql') FROM 管理员账号数据库"
cursor.execute(sql)
db.commit()
sql = "SELECT * FROM f_user_p"
cursor.execute(sql)
data = cursor.fetchall()
print(data)
# sql = "SELECT * FROM f_user_p"
# cursor.execute(sql)
# data = cursor.fetchall()
# print(data)
# db.close()
