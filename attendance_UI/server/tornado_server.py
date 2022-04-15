# tornado框架实现的本地服务器
from abc import ABC
from tornado import web

from Utils import Admin_Info, Connect_DataBase
import datetime


class MainPageHandler(web.RequestHandler, ABC):
    def get(self):  # 响应get请求
        self.write('hello')
        print(self.request)

    def post(self):  # 响应post请求
        name = self.get_argument('username')
        num = self.get_argument('num')
        grade = self.get_argument('grade')
        major = self.get_argument('major')
        code = self.get_argument('code')  # 管理员发布签到时给的口令
        class_name = self.get_argument('classname')
        ip_address = self.request.remote_ip  # 获取IP地址，防止重复签到的措施
        movement = self.get_argument('isLogin')
        sign_in_status = Admin_Info.get_value('status')
        sign_out_status = Admin_Info.get_value('sign_out_status')
        sign_code = Admin_Info.get_value('code_num')

        db, cursor = Connect_DataBase.connect_db('class_student')
        time = datetime.datetime.now().strftime('%Y-%m-%d')  # 返回当前服务器时间作为签到为准的时间
        column_name = datetime.datetime.now().strftime('%Y年%m月%d日')  # 列名

        if ip_address not in Admin_Info.get_value('ip_address'):
            if sign_in_status == 'yes' or sign_out_status == 'yes':
                sign_class_name = Admin_Info.get_value('class_name')  # 获取课程名
                sign_grade = Admin_Info.get_value('grade')  # 获取当前签到年级
                sign_major = Admin_Info.get_value('major_name')  # 获取当前签到专业

                if sign_in_status == 'yes':  # 判断现在是签到还是签退，选择对应的数据表
                    table_name = Admin_Info.get_name() + '_' + Admin_Info.get_value('class_name')
                else:
                    table_name = Admin_Info.get_name() + '_' + Admin_Info.get_value('class_name') + '_签退'

                if movement == 'yes' and code == sign_code and class_name == sign_class_name and major == sign_major \
                        and grade == sign_grade:  # 如果是签到请求，且输入的信息也符合当前正在签到的课程
                    sql = "SELECT * FROM %s WHERE 学号='%s' AND 姓名='%s'" % (table_name, num, name)
                    cursor.execute(sql)
                    data = cursor.fetchall()
                    if len(data) != 0:  # 如果是空集，则说明没有这个人，或者信息输入错误
                        sql = "UPDATE %s SET %s='1' WHERE 学号=%s AND 专业='%s' AND 年级='%s' AND 姓名='%s'" % \
                              (table_name, column_name, num, major, grade, name)  # 通过学号、专业、年级查找当前签到范围内的学生
                        try:
                            cursor.execute(sql)
                            data = {'status': 'sign in/out success', 'time': time, 'result': 'success'}
                            Admin_Info.add_ip_address(ip_address)  # 操作成功才记录ip地址
                        except KeyError:
                            data = {'status': 'something went wrong, can not sign in/out', 'time': time,
                                    'result': 'wrong'}
                        finally:
                            db.commit()
                            db.close()
                    else:
                        data = {'status': 'student name or number may wrong, please check again', 'time': time,
                                'result': 'wrong'}
                        db.close()
                else:
                    data = {'status': 'information may wrong or you are not in sign time,please check again',
                            'time': time}
            else:
                print(sign_in_status)
                data = {'status': 'not in sign time, please wait', 'time': time}
        else:
            data = {'status': 'you have already signed in/out, do not sign again', 'time': time}

        self.write(data)

    def prepare(self):  # 本地跨域访问
        origin = self.request.headers.get("Origin", "http://local.test.com:8080")
        self.set_header('Access-Control-Allow-Origin', origin)
        self.set_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, PATCH, OPTIONS')
        self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Access-Control-Allow-Credentials', "true")

# application = web.Application([
#     (r"/", MainPageHandler),
# ])
#
# if __name__ == '__main__':
#     http_server = httpserver.HTTPServer(application)
#     http_server.listen(8080)
#     ioloop.IOLoop.current().start()
