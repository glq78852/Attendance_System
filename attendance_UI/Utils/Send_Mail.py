# 发送邮件

import smtplib
from email.mime.text import MIMEText


def send_email(class_name, student_name, time, email_receiver, status):
    email_host = 'smtp.126.com'
    email_user = 'g13690102717'
    email_password = 'ganliuqi26#'
    sender = 'g13690102717@126.com'
    if status == 'sign_in':
        message = MIMEText(student_name + '同学，' + time + '的' + class_name + '课程你未签到或签到失败，如有特殊情况请尽快联系老师，'
                                                                            '否则将缺勤一次。', 'plain', 'utf-8')
        message['Subject'] = '课程签到情况'
    else:
        message = MIMEText(student_name + '同学，' + time + '的' + class_name + '课程你未签退或签退失败，如有特殊情况请尽快联系老师，'
                                                                            '否则将缺勤一次。', 'plain', 'utf-8')
        message['Subject'] = '课程签退情况'
    message['From'] = sender
    message['To'] = email_receiver
    smtpobj = smtplib.SMTP()
    smtpobj.connect(email_host, 25)
    smtpobj.login(email_user, email_password)
    smtpobj.sendmail(sender, email_receiver, message.as_string())
    smtpobj.quit()
