# main函数
from admin_system import Login_Page
from tornado import web, ioloop, httpserver
from server import tornado_server
import threading

if __name__ == '__main__':
    application = web.Application([
        (r"/", tornado_server.MainPageHandler),
    ])

    http_server = httpserver.HTTPServer(application)
    http_server.listen(8080)

    thread = threading.Thread(target=ioloop.IOLoop.current().start, name='test', daemon=True)
    thread.start()  # 开启服务器

    login = Login_Page.LoginPage()
