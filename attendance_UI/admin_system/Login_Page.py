# 登录界面

import tkinter as tk
import tkinter.messagebox as tk_message
import MySQLdb
from admin_system import Operate_Page
from Utils import Admin_Info, Create_Window


class LoginPage:
    def __init__(self):
        self.login_window = Create_Window.create_window('系统登录', 600, 600)

        # 放置logo
        img1 = tk.PhotoImage(file="./images/logo1.png")  # 华大logo图片
        canvas = tk.Canvas(self.login_window, bg='white', width=300, height=300)  # 画布
        canvas.pack()
        canvas.create_image(25, 0, anchor='nw', image=img1)

        # 创建账号输入框
        tk.Label(self.login_window, text="管理员账号：", font=("宋体", 12)).place(x=150, y=350)
        var_usr_name = tk.StringVar()
        entry_usr_name = tk.Entry(self.login_window, textvariable=var_usr_name, width=27)
        entry_usr_name.place(x=250, y=350)

        # 创建密码输入框
        tk.Label(self.login_window, text="管理员密码：", font=("宋体", 12)).place(x=150, y=400)
        var_usr_password = tk.StringVar()
        entry_usr_password = tk.Entry(self.login_window, textvariable=var_usr_password, width=27, show='*')
        entry_usr_password.place(x=250, y=400)

        # 登录函数
        def usr_login():
            usr_name = var_usr_name.get()
            usr_password = var_usr_password.get()
            db = MySQLdb.Connect("localhost", "root", "", "attendance_system", charset="utf8")
            cursor = db.cursor()
            cursor.execute("SELECT * FROM 管理员账号数据库")
            data = cursor.fetchall()
            if usr_name == '' or usr_password == '':
                tk_message.showinfo(message='账号或密码不能为空', title='出错了捏')
            else:
                for obj in data:  # 查找匹配的管理员
                    if obj[1] == usr_name and obj[2] == usr_password:
                        Admin_Info.set_name(obj[0])  # 传递管理员名字
                        self.login_window.destroy()
                        Operate_Page.OperatePage()  # 页面跳转
                        Admin_Info.set_status('no')  # 成功登陆后将签到状态改为no，即当前不在签到时间内
                        cursor.close()
                        db.close()
                        return
                tk_message.showinfo(message='账号或密码错误', title='出错了捏')

        # 创建登陆按钮
        bt_login = tk.Button(self.login_window, text="登录", command=usr_login, width=15)
        bt_login.place(x=245, y=450)

        self.login_window.mainloop()
