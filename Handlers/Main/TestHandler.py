# 测试用handler
import tornado.web


class TestHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', 'x-requested-with')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, PUT, DELETE')
        message = self.get_argument("message")
        print(message)
