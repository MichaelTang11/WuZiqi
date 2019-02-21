import logging
import tornado.web


class CheckLoginStatusHandler(tornado.web.RequestHandler):
    def post(self):
        user_id = self.get_secure_cookie('user_id')  # 获取加密的cookie
        if user_id:
            self.write("{'status':'True'}")
            logging.info("write {'status':'True'}")
        else:
            self.write("{'status':'False'}")
            logging.info("write {'status':'False'}")
