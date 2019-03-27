# 测试用handler
import tornado.web
import logging

class TestHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        logging.info("test")