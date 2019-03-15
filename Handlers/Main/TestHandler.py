# 测试用handler
import tornado.web


class TestHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        self.clear_all_cookies()
