# 学生数据导出页面
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from Utils import Admin_Info, Create_Window, Connect_DataBase
import csv


class DataExportPage:
    def __init__(self):
        self.data_export_window = Create_Window.create_secondary_window('导出数据', 300, 300)
        admin_name = Admin_Info.get_name()
        db, cursor = Connect_DataBase.connect_db('teacher_class')  # 连接老师-课程的数据库，找到信息
        sql1 = 'SELECT DISTINCT 课程名 FROM %s' % admin_name
        sql3 = 'SELECT 专业 FROM %s' % admin_name

        cursor.execute(sql1)
        class_name = cursor.fetchall()  # 获取课程名
        cursor.execute(sql3)
        major = cursor.fetchall()  # 获取专业

        db.close()

        # 数据处理
        major_list = []
        class_list = []
        for i in major:
            for j in i:
                major_list = major_list + j.split(',')
        major_list = set(major_list)
        major_tuple = tuple(major_list)

        for i in class_name:
            for j in i:
                class_list = class_list + j.split(',')
        class_list = set(class_list)
        class_tuple = tuple(class_list)

        tk.Label(self.data_export_window, text='课程：', font=('宋体', 10)).place(x=70, y=60)
        class_combobox = ttk.Combobox(self.data_export_window, width=13)
        class_combobox['value'] = class_tuple
        class_combobox.current(0)
        class_combobox.place(x=110, y=58)

        tk.Label(self.data_export_window, text='年级：', font=('宋体', 10)).place(x=70, y=110)
        grade_combobox = ttk.Combobox(self.data_export_window, width=13)
        grade_combobox['value'] = ('大一', '大二', '大三', '大四')
        grade_combobox.current(0)
        grade_combobox.place(x=110, y=108)

        tk.Label(self.data_export_window, text='专业：', font=('宋体', 10)).place(x=70, y=160)
        major_combobox = ttk.Combobox(self.data_export_window, width=13)
        major_combobox['value'] = major_tuple
        major_combobox.current(0)
        major_combobox.place(x=110, y=158)

        def confirm_export():
            lesson_name = class_combobox.get()
            grade_name = grade_combobox.get()
            major_name = major_combobox.get()
            table_name = admin_name + '_' + lesson_name
            table_name_out = table_name + '_签退'

            file_type = [('Excel Files', '*.csv')]
            path = filedialog.asksaveasfilename(filetypes=file_type, defaultextension=file_type)  # 获取保存文件的路径
            file = open(path, 'w', newline='')
            file_writer = csv.writer(file)
            try:
                db, cursor = Connect_DataBase.connect_db('class_student')
                sql = "select COLUMN_NAME from information_schema.COLUMNS where table_name = '%s' " \
                      "and table_schema = '%s'; " % (table_name, 'class_student')
                cursor.execute(sql)
                col = cursor.fetchall()
                col_login = []
                for obj in col:
                    col_login.append(obj[0])
                columns_login = tuple(col_login)  # 获取列名，写在导出文件的第一行，以签到的日期为准，签退作为辅助手段，不以签退的日期为准
                file_writer.writerow(columns_login)
                print(col)
                print(col_login)

                sql = "select COLUMN_NAME from information_schema.COLUMNS where table_name = '%s' " \
                      "and table_schema = '%s'; " % (table_name_out, 'class_student')
                cursor.execute(sql)
                col = cursor.fetchall()
                db.close()
                col_logout = []
                for obj in col:
                    col_logout.append(obj[0])

            except KeyError:
                messagebox.showinfo(title='出错了捏', message='数据库连接失败，请重试！')
                return 'error'
            sql = "SELECT * FROM %s WHERE 年级='%s' AND 专业='%s'" % (table_name, grade_name, major_name)
            sql_out = "SELECT * FROM %s WHERE 年级='%s' AND 专业='%s'" % (table_name_out, grade_name, major_name)
            try:
                db, cursor = Connect_DataBase.connect_db('class_student')
                cursor.execute(sql)
                data_login = cursor.fetchall()
                cursor.execute(sql_out)
                data_logout = cursor.fetchall()
                list_data_login = []
                list_data_logout = []

                for obj1 in data_login:
                    list_data_login.append(list(obj1))
                for obj2 in data_logout:
                    list_data_logout.append(list(obj2))

                for num in range(4, len(col_login)):  # 考勤数据处理，签到签退都为1才算一次完整的签到，
                    if col_login[num] in col_logout:  # 如果当天既有签到又有签退，没有签退的情况不需要修改，直接使用签到数据集的数据
                        index = col_logout.index(col_login[num])  # 取到那一天的日期在签退列名中的索引
                        for item_index in range(len(list_data_login)):  # 遍历学生数据，总学生数量是相等的，所以len()谁都可以
                            if list_data_login[item_index][num] != list_data_logout[item_index][index]:
                                # 签到的索引用num，签退的索引用index，如果学生的签到签退数据不一样，直接算缺勤
                                list_data_login[item_index][num] = '0'
                            elif list_data_login[item_index][num] == '0' and list_data_logout[item_index][index]:
                                # 如果直接就没来，即签到签退都为0，也算缺勤
                                list_data_login[item_index][num] = '0'
                            # 最后只就剩下签到签退都为1的情况了，不需要修改

                for item in list_data_login:  # 数据写入csv
                    file_writer.writerow(item)
                file.close()
                db.close()
            except KeyError:
                messagebox.showinfo(title='出错了捏', message='连接数据库失败，请重试！')
                return 'error'

        bt_confirm = tk.Button(self.data_export_window, text='确定', command=confirm_export, width=10)
        bt_confirm.place(x=115, y=220)

        self.data_export_window.mainloop()
