import tornado.ioloop
import tornado.httpserver
import tornado.options
import logging
from Methods.GetServiceIP import ip
from url import url


def main():
    LOG_FORMAT = "%(asctime)s === %(module)s === %(funcName)s === %(levelname)s === %(message)s"
    logging.basicConfig(level=logging.DEBUG,format=LOG_FORMAT)
    application=tornado.web.Application( url,cookie_secret="dj2SOjWryYSaDiFjy2s4cjj")
    http_server = tornado.httpserver.HTTPServer(application)
    tornado.options.parse_command_line()
    http_server.listen(1001)
    print('Development server is running at http://'+ip+':1001')
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
