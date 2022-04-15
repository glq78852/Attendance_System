# 签到发布页面
import tkinter as tk
from tkinter import ttk

from Utils import Admin_Info, Create_Window, Connect_DataBase
import datetime
from tkinter import messagebox as tk_message
import threading
from Utils import Send_Mail


class PunchReleasePage:
    def __init__(self):
        self.punch_release_window = Create_Window.create_secondary_window('发布签到', 300, 300)
        admin_name = 'glq'  # Admin_Info.get_name()
        db, cursor = Connect_DataBase.connect_db('teacher_class')  # 连接老师-课程的数据库，找到信息
        sql1 = 'SELECT DISTINCT 课程名 FROM %s' % admin_name
        sql3 = 'SELECT 专业 FROM %s' % admin_name
        self.table_name = ''
        self.lesson_name = ''
        self.time = ''

        cursor.execute(sql1)
        class_name = cursor.fetchall()  # 获取课程名
        cursor.execute(sql3)
        major = cursor.fetchall()  # 获取专业

        db.close()

        major_list = []
        for i in major:
            for j in i:
                major_list = major_list + j.split(',')
        major_list = set(major_list)
        major_tuple = tuple(major_list)

        tk.Label(self.punch_release_window, text='课程：', font=('宋体', 10)).place(x=70, y=30)
        class_combobox = ttk.Combobox(self.punch_release_window, width=13)
        class_combobox['value'] = class_name[0]
        class_combobox.current(0)
        class_combobox.place(x=110, y=28)

        tk.Label(self.punch_release_window, text='年级：', font=('宋体', 10)).place(x=70, y=70)
        grade_combobox = ttk.Combobox(self.punch_release_window, width=13)
        grade_combobox['value'] = ('大一', '大二', '大三', '大四')
        grade_combobox.current(0)
        grade_combobox.place(x=110, y=68)

        tk.Label(self.punch_release_window, text='专业：', font=('宋体', 10)).place(x=70, y=110)
        major_combobox = ttk.Combobox(self.punch_release_window, width=13)
        major_combobox['value'] = major_tuple
        major_combobox.current(0)
        major_combobox.place(x=110, y=108)

        tk.Label(self.punch_release_window, text='口令：', font=('宋体', 10)).place(x=70, y=150)
        random_code_combobox = tk.Entry(self.punch_release_window, width=15)
        random_code_combobox.place(x=110, y=148)

        tk.Label(self.punch_release_window, text='时间：', font=('宋体', 10)).place(x=70, y=190)
        sign_time_combobox = tk.Entry(self.punch_release_window, width=5)
        sign_time_combobox.place(x=110, y=188)

        tk.Label(self.punch_release_window, text='秒', font=('宋体', 10)).place(x=150, y=188)

        def time_counting():
            Admin_Info.set_status('no')
            Admin_Info.ip_address_reset()  # 重置ip地址的记录
            Send_Mail.send_email(self.lesson_name, '甘流奇', self.time, 'glq78852@qq.com', 'sign_in')

        def confirm_release_punch():
            Admin_Info.set_class(class_combobox.get())  # 传递课程名
            Admin_Info.set_grade(grade_combobox.get())  # 传递年级数
            Admin_Info.set_major(major_combobox.get())  # 传递专业名
            Admin_Info.set_code(random_code_combobox.get())  # 传递签到口令

            if sign_time_combobox.get() != '':  # 如果有输入则按输入的来，没输入默认3分钟
                sign_time = float(sign_time_combobox.get())  # 获取签到时间
            else:
                sign_time = 180

            time = datetime.datetime.now().strftime('%Y年%m月%d日')
            self.time = time
            lesson_name = class_combobox.get()
            self.lesson_name = lesson_name
            table_name = admin_name + '_' + lesson_name
            self.table_name = table_name

            sql_check = "select count(*) from information_schema.columns where table_name = '%s' " \
                        "and column_name = '%s'" % (table_name, time)
            try:
                db, cursor = Connect_DataBase.connect_db('class_student')
                cursor.execute(sql_check)
                result = cursor.fetchall()
                if result[0][0] == 0:  # 一名老师当天不止签到一次，如果是第一堂课则创建新列，不是则不创建，直接开始签到计时
                    sql = "ALTER TABLE %s ADD COLUMN %s VARCHAR(255) NOT NULL DEFAULT '0'" \
                          % (table_name, time)  # 第一次发布签到，新增一列
                    cursor.execute(sql)
                self.punch_release_window.destroy()
                Admin_Info.set_status('yes')  # 成功发布签到后修改为yes，代表当前正在签到时间内
                timer = threading.Timer(sign_time, time_counting)  # 定时器，超过时间后不可签到
                timer.start()
            except KeyError:
                tk_message.showinfo(message='数据库连接失败，请重试！', title='出错了捏')
                return 'error'

        bt_confirm = tk.Button(self.punch_release_window, text='确定', command=confirm_release_punch, width=10)
        bt_confirm.place(x=115, y=230)

        self.punch_release_window.mainloop()


# PunchReleasePage()
