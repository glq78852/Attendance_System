# 签到情况查询页面
import tkinter as tk
from tkinter import messagebox as tk_message
from tkinter import ttk
from Utils import Admin_Info, Create_Window, Connect_DataBase


class InfoCheckPage:
    def __init__(self, parent_window):
        # 创建弹窗，获取查询所需数据
        self.get_class_data_window = Create_Window.create_secondary_window('输入查询条件', 350, 100)
        tk.Label(self.get_class_data_window, text='请输入课程名称：', font=('宋体', 10)).place(x=10, y=35)
        database, db_cursor = Connect_DataBase.connect_db('teacher_class')
        db_sql = 'SELECT DISTINCT 课程名 FROM %s' % Admin_Info.get_name()  # 可能存在教不同的年级，极有可能存在同名课程，顾用distinct
        db_cursor.execute(db_sql)
        lesson = db_cursor.fetchall()  # 获取当前登录管理员的所有课程
        database.close()

        self.hide = []  # 隐藏的节点
        self.hide_id = []  # 隐藏的节点对应的位置索引，还原时需要
        self.table = None  # 返回最新的table

        var_class_data = tk.StringVar()
        combobox_class_data = ttk.Combobox(self.get_class_data_window, textvariable=var_class_data, width=18)
        combobox_class_data['value'] = lesson
        combobox_class_data.current(0)
        combobox_class_data.place(x=115, y=33)

        def create_table(columns, last_window, data):  # 创建树视图函数
            frame = tk.Frame(last_window)
            frame.place(x=50, y=50, width=800, height=500)
            x_scroll = tk.Scrollbar(frame, orient='horizontal')  # 创建x、y轴的滚动轮
            y_scroll = tk.Scrollbar(frame, orient='vertical')

            table = ttk.Treeview(
                master=frame,
                height=10,
                columns=columns,
                show='headings',
                xscrollcommand=x_scroll.set,
                yscrollcommand=y_scroll.set,
            )
            # 设置行样式
            for obj in columns:
                table.heading(column=obj, text=obj)
            for obj in columns:
                table.column(obj, width=50, anchor='center')

            x_scroll.config(command=table.xview)
            x_scroll.pack(side='bottom', fill='x')
            y_scroll.config(command=table.yview)
            y_scroll.pack(side='right', fill='y')

            for obj in data:  # 按行添加数据
                rank = []
                for i in range(len(obj)):
                    rank.append(obj[i])
                table.insert('', 'end', values=rank)

            # 点击列名排序
            def sort_table(tv, column, reverse):
                col_sort = [(tv.set(k, column), k) for k in tv.get_children('')]
                col_sort.sort(reverse=reverse)
                for index, (val, k) in enumerate(col_sort):
                    tv.move(k, '', index)
                tv.heading(column, command=lambda: sort_table(tv, column, not reverse))

            for col in columns:
                table.heading(col, text=col, command=lambda _col=col: sort_table(table, _col, False))

            return table

        def get_class_name():
            # 获取输入值，字符串拼接形成所需名字
            class_name = combobox_class_data.get()
            admin_name = Admin_Info.get_name()
            table_name = admin_name + '_' + class_name
            db, cursor = Connect_DataBase.connect_db('class_student')
            # 找到当前登录的教师对应的表
            sql_sentence = "SELECT count(*) FROM information_schema.tables WHERE table_schema = '%s' " \
                           "and table_name = '%s' and table_type = 'BASE TABLE';" % ('class_student', table_name)
            cursor.execute(sql_sentence)  # 查询结果
            result = cursor.fetchall()
            db.close()

            if result[0][0] == 1:  # 如果存在对应的表，则显示对应查询结果
                db, cursor = Connect_DataBase.connect_db('class_student')
                cursor.execute('SELECT * FROM %s' % table_name)
                data = cursor.fetchall()
                db.close()
                self.get_class_data_window.destroy()  # 关闭查询页面
                self.info_check_window = Create_Window.create_window('签到情况查询', 1100, 650)  # 创建查询结果页面

                # 获取表的列名
                db, cursor = Connect_DataBase.connect_db('class_student')
                sql_sentence = "select COLUMN_NAME from information_schema.COLUMNS where table_name = '%s' and " \
                               "table_schema = '%s'; " % (table_name, 'class_student')
                cursor.execute(sql_sentence)
                col = cursor.fetchall()
                db.close()
                col_ = []
                for obj in col:
                    col_.append(obj[0])

                # 创建树视图
                columns = tuple(col_)
                tab = create_table(columns, self.info_check_window, data)

                tab.place(width=780, height=480)
                self.table = tab

                # 树形图操作设计，添加学生、删除学生、修改内容、筛选学生
                def info_insert():  # 添加
                    insert_window = Create_Window.create_secondary_window('添加数据', 300, 300)
                    tk.Label(insert_window, text='姓名：', font=('宋体', 10)).place(x=50, y=30)
                    var_insert_name = tk.StringVar()
                    insert_name_entry = tk.Entry(insert_window, textvariable=var_insert_name, width=22)
                    insert_name_entry.place(x=90, y=28)

                    tk.Label(insert_window, text='学号：', font=('宋体', 10)).place(x=50, y=80)
                    var_insert_num = tk.StringVar()
                    insert_num_entry = tk.Entry(insert_window, textvariable=var_insert_num, width=22)
                    insert_num_entry.place(x=90, y=78)

                    tk.Label(insert_window, text='年级：', font=('宋体', 10)).place(x=50, y=130)
                    var_insert_grade = tk.StringVar()
                    insert_grade_entry = tk.Entry(insert_window, textvariable=var_insert_grade, width=22)
                    insert_grade_entry.place(x=90, y=128)

                    tk.Label(insert_window, text='专业：', font=('宋体', 10)).place(x=50, y=180)
                    var_insert_major = tk.StringVar()
                    insert_major_entry = tk.Entry(insert_window, textvariable=var_insert_major, width=22)
                    insert_major_entry.place(x=90, y=178)

                    def table_insert():  # 获取输入框数据并添加到树形图中
                        insert_name = str(insert_name_entry.get())
                        insert_num = str(insert_num_entry.get())
                        insert_grade = str(insert_grade_entry.get())
                        insert_major = str(insert_major_entry.get())

                        db_, cursor_ = Connect_DataBase.connect_db('class_student')
                        sql = "SELECT * FROM %s WHERE 学号='%s';" % (table_name, insert_num)
                        cursor_.execute(sql)
                        data_ = cursor_.fetchall()
                        db_.close()
                        if len(data_) == 0:
                            db_, cursor_ = Connect_DataBase.connect_db('class_student')
                            sql = "INSERT INTO %s(%s,%s,%s,%s) VALUES('%s', '%s', '%s', '%s')" % (table_name, '姓名',
                                                                                                  '学号', '年级', '专业',
                                                                                                  insert_name,
                                                                                                  insert_num,
                                                                                                  insert_grade,
                                                                                                  insert_major)
                            cursor_.execute(sql)
                            db_.commit()
                            db_.close()

                            self.table.insert('', 'end', values=(insert_name, insert_num, insert_grade, insert_major))
                            insert_window.destroy()
                            self.info_check_window.update()
                        else:
                            tk_message.showinfo(message='学生已存在！', title='出错了捏')

                    bt_confirm = tk.Button(insert_window, text='确定', command=table_insert, width=10)
                    bt_confirm.place(x=115, y=250)

                    insert_window.mainloop()

                def info_delete():  # 删除
                    if self.table.selection():  # 鼠标有选中节点才执行
                        parent_window.withdraw()
                        res = tk_message.askyesno('提示', '是否删除所选数据？')
                        if res:
                            delete_item = self.table.item(self.table.selection()[0], 'values')
                            db_, cursor_ = Connect_DataBase.connect_db('class_student')
                            sql = "DELETE FROM %s WHERE 学号='%s';" % (table_name, delete_item[1])
                            cursor_.execute(sql)
                            db_.commit()
                            db_.close()
                            self.table.delete(self.table.selection())
                        parent_window.deiconify()
                    self.info_check_window.update()

                def info_modify():  # 修改签到状态
                    if self.table.selection():
                        date_select_window = Create_Window.create_secondary_window('选择日期', 300, 220)  # 出现选择日期的弹窗
                        modify_item = self.table.item(self.table.selection()[0], 'values')
                        tk.Label(date_select_window, text='选择日期：', font=('宋体', 10)).place(x=25, y=35)
                        combobox = ttk.Combobox(date_select_window, width=15)  # 创建下拉选择框
                        combobox_value = tuple(col_[4:])  # 将所有的日期从列名中切片出来转为tuple
                        combobox['value'] = combobox_value
                        combobox.current(0)  # 默认显示第0项
                        combobox.place(x=100, y=32)

                        tk.Label(date_select_window, text='修改状态：', font=('宋体', 10)).place(x=25, y=90)
                        modify_status_combobox = ttk.Combobox(date_select_window, width=10)
                        modify_status_combobox['value'] = ('0', '1')  # 0代表未签到，1代表签到
                        modify_status_combobox.current(0)
                        modify_status_combobox.place(x=100, y=90)

                        def select_date():  # 点击确认选择日期后执行
                            date = combobox.get()
                            date_index = combobox.current()
                            new_status = modify_status_combobox.get()
                            db_, cursor_ = Connect_DataBase.connect_db('class_student')
                            sql = "UPDATE %s SET %s='%s' WHERE 学号=%s;" % (table_name, date, new_status,
                                                                          modify_item[1])
                            cursor_.execute(sql)
                            db_.commit()
                            db_.close()

                            new_item = list(modify_item)  # 先把选中的节点数据转为list
                            if len(new_item) > date_index + 4:  # 如果原本就有签到状态，则修改
                                new_item[date_index + 4] = new_status  # 在对应位置修改数据
                            else:  # 如果原本没有签到状态则新增
                                new_item.append(new_status)
                            new_item_tuple = tuple(new_item)  # 转回tuple
                            self.table.item(self.table.selection()[0], values=new_item_tuple)  # 更新数据

                            date_select_window.destroy()
                            self.info_check_window.update()

                        bt_confirm = tk.Button(date_select_window, text='确定', command=select_date, width=10)
                        bt_confirm.place(x=115, y=150)
                        date_select_window.mainloop()

                def info_select():  # 筛选
                    select_window = Create_Window.create_secondary_window('筛选数据', 300, 220)
                    tk.Label(select_window, text='选择年级：', font=('宋体', 10)).place(x=25, y=35)
                    combobox_select_grade = ttk.Combobox(select_window, width=10)  # 创建下拉选择框
                    combobox_select_grade['value'] = ('大一', '大二', '大三', '大四')
                    combobox_select_grade.current(0)  # 默认显示第0项
                    combobox_select_grade.place(x=100, y=32)

                    tk.Label(select_window, text='选择专业：', font=('宋体', 10)).place(x=25, y=90)
                    db_, cursor_ = Connect_DataBase.connect_db('class_student')
                    sql = "SELECT DISTINCT 专业 FROM %s" % table_name
                    cursor_.execute(sql)
                    major = cursor_.fetchall()
                    db_.close()
                    major_ = list(major)
                    major_.insert(0, '无')
                    major_new = tuple(major_)
                    combobox_select_major = ttk.Combobox(select_window, width=10)
                    combobox_select_major['value'] = major_new  # 列出所有专业
                    combobox_select_major.current(0)
                    combobox_select_major.place(x=100, y=89)

                    def show_select_info():  # 展示筛选结果
                        tv_children = self.table.get_children()  # 获取树视图中所有节点的id
                        select_grade = combobox_select_grade.get()
                        select_major = combobox_select_major.get()  # 获取输入
                        if select_grade == '无' and select_major == '无':  # 如果没选择任何条件则无事发生
                            return
                        else:
                            if select_grade != '无' and select_major != '无':  # 确定筛选项目
                                select_info = [2, 3]
                            elif select_grade == '无':
                                select_info = [3]
                            else:
                                select_info = [2]
                            for child in tv_children:  # 找出所有不符合筛选条件的节点
                                if len(select_info) == 2:
                                    if self.table.item(child)['values'][2] != select_grade or \
                                            self.table.item(child)['values'][3] != select_major:  # 年级专业都不符合
                                        self.hide.append(child)  # 把不符合的ID记录，后面隐藏
                                        self.hide_id.append(self.table.index(child))
                                else:
                                    if select_info[0] == 2:  # 如果单筛选项，且条件为年级
                                        if self.table.item(child)['values'][2] != select_grade:  # 条件不符合就加入隐藏名单
                                            self.hide.append(child)
                                            self.hide_id.append(self.table.index(child))
                                    elif select_info[0] == 3:  # 如果条件不是年级，就是专业
                                        if self.table.item(child)['values'][3] != select_major:  # 条件不符合则加入隐藏名单
                                            self.hide.append(child)
                                            self.hide_id.append(self.table.index(child))
                            for hide_obj in self.hide:  # 隐藏不符合条件的节点
                                self.table.detach(hide_obj)

                    def reset_info_select():
                        for index in range(len(self.hide)):
                            self.table.move(self.hide[index], '', index)
                        self.hide_id = []
                        self.hide = []

                    bt_select_info = tk.Button(select_window, text='确定', command=show_select_info, width=10)
                    bt_select_info.place(x=180, y=150)
                    bt_reset = tk.Button(select_window, text='筛选还原', command=reset_info_select, width=10)
                    bt_reset.place(x=60, y=150)
                    select_window.mainloop()

                def info_refresh():  # 刷新函数
                    db_, cursor_ = Connect_DataBase.connect_db('class_student')
                    cursor_.execute('SELECT * FROM %s' % table_name)
                    new_data = cursor_.fetchall()  # 重新获取数据库数据
                    db_.close()

                    db_, cursor_ = Connect_DataBase.connect_db('class_student')
                    sql = "select COLUMN_NAME from information_schema.COLUMNS where table_name = '%s' and " \
                          "table_schema = '%s'; " % (table_name, 'class_student')
                    cursor_.execute(sql)
                    _col = cursor_.fetchall()  # 重新获取新的列名
                    db_.close()
                    _col_ = []
                    for p in _col:
                        _col_.append(p[0])

                    # 创建树视图
                    columns_ = tuple(col_)
                    new_table = create_table(columns_, self.info_check_window, new_data)
                    new_table.place(width=780, height=480)
                    self.table = new_table

                bt_insert = tk.Button(self.info_check_window, text='添加数据', command=info_insert, width=15)
                bt_insert.place(x=920, y=60)
                bt_delete = tk.Button(self.info_check_window, text='删除数据', command=info_delete, width=15)
                bt_delete.place(x=920, y=150)
                bt_modify = tk.Button(self.info_check_window, text='修改签到状态', command=info_modify, width=15)
                bt_modify.place(x=920, y=240)
                bt_select = tk.Button(self.info_check_window, text='筛选数据', command=info_select, width=15)
                bt_select.place(x=920, y=330)
                bt_refresh = tk.Button(self.info_check_window, text="刷新数据", command=info_refresh, width=15)
                bt_refresh.place(x=920, y=420)

                self.info_check_window.mainloop()

            else:
                tk_message.showinfo(message='没有此课程', title='出错了捏')

        bt_search = tk.Button(self.get_class_data_window, text='查询', command=get_class_name, width=5)
        bt_search.place(x=290, y=27)

        self.get_class_data_window.mainloop()  # 先显示弹窗，输入的课程有查询结果再出现下一层弹窗
