# 创建窗口类
import tkinter as tk


def create_window(window_title, width, height):  # 创建主窗口
    window = tk.Tk()
    window.title(window_title)
    window.minsize(width, height)
    window.maxsize(width, height)  # 窗口不可缩放
    window.resizable(0, 0)
    screenwidth = window.winfo_screenwidth()
    screenheight = window.winfo_screenheight()
    window.geometry(
        '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2))  # 设置窗口大小，居中显示
    return window


def create_secondary_window(window_title, width, height):  # 创建子窗口
    window = tk.Toplevel(name=window_title)
    window.title(window_title)
    window.minsize(width, height)
    window.maxsize(width, height)
    window.resizable(0, 0)
    screenwidth = window.winfo_screenwidth()
    screenheight = window.winfo_screenheight()
    window.geometry(
        '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2))  # 设置窗口大小，居中显示
    return window


