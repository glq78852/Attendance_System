# 管理员身份信息管理文件

global admin_name
global class_name
global grade_num
global major_name
global code_num
global is_in_login_time
global is_in_logout_time
global ip_address
ip_address = []
is_in_login_time = 'no'
is_in_logout_time = 'no'
code_num = ''


def set_name(name):
    """ 定义一个全局变量 """
    global admin_name
    admin_name = name


def set_class(name):
    global class_name
    class_name = name


def set_grade(grade):
    global grade_num
    grade_num = grade


def set_major(major):
    global major_name
    major_name = major


def set_code(code):
    global code_num
    code_num = code


def set_status(new_status):
    global is_in_login_time
    is_in_login_time = new_status


def set_logout_status(new_status):
    global is_in_logout_time
    is_in_logout_time = new_status


def add_ip_address(address):
    global ip_address
    ip_address.append(address)


def ip_address_reset():
    global ip_address
    ip_address = []


def get_name():
    """ 获得一个全局变量,不存在则返回默认值 """
    try:
        return 'glq'  # admin_name
    except KeyError:
        return 'error'


def get_value(value):
    if value == 'class_name':
        return class_name
    elif value == 'grade':
        return grade_num
    elif value == 'major_name':
        return major_name
    elif value == 'code_num':
        return code_num
    elif value == 'status':
        return is_in_login_time
    elif value == 'sign_out_status':
        return is_in_logout_time
    elif value == 'ip_address':
        return ip_address
    else:
        return 'error'
