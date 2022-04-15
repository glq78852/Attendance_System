# 操作中转界面
import tkinter as tk
from Utils import Create_Window
from admin_system import Info_Check_Page
from admin_system import Punch_Release_Page
from admin_system import Data_Export_Page
from admin_system import Sign_Out_Page


class OperatePage:
    def __init__(self):
        # 创建操作界面窗口
        self.op_window = Create_Window.create_window('后台管理系统操作界面', 400, 250)

        def punch_release():  # 发布签到按钮，弹出发布窗口
            Punch_Release_Page.PunchReleasePage()

        def info_check():  # 弹出查看学生签到情况的页面
            Info_Check_Page.InfoCheckPage(self.op_window)

        def info_export():  # 弹出签到情况导出页面
            Data_Export_Page.DataExportPage()

        def sign_out():  # 弹出签退页面
            Sign_Out_Page.SignOutPage()

        # 操作按钮设置
        self.bt_punch_release = tk.Button(self.op_window, text='发布签到', command=punch_release, width=15, height=3)
        self.bt_punch_release.place(x=50, y=40)

        self.bt_info_check = tk.Button(self.op_window, text='签到情况查询', command=info_check, width=15, height=3)
        self.bt_info_check.place(x=235, y=150)

        self.bt_info_import = tk.Button(self.op_window, text='签到情况导出', command=info_export, width=15, height=3)
        self.bt_info_import.place(x=50, y=150)

        self.bt_vacation_approval = tk.Button(self.op_window, text='发布签退', command=sign_out, width=15, height=3)
        self.bt_vacation_approval.place(x=235, y=40)

        self.op_window.mainloop()

