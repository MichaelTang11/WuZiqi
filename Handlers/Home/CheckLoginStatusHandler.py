import logging
import tornado.web


class CheckLoginStatusHandler(tornado.web.RequestHandler):
    def post(self):
        userId = self.get_secure_cookie('userId')  # 获取加密的cookie
        if userId:
            self.write("{'status':'True'}")
            logging.info("write {'status':'True'}")
        else:
            self.write("{'status':'False'}")
            logging.info("write {'status':'False'}")
