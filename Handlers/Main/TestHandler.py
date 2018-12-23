#测试用handler
import tornado.web


class TestHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.set_secure_cookie("user_id", "1")
        self.write("test handler")