import logging
import tornado.web


class LogoutHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        self.clear_cookie('user_id')
        self.redirect("Login.html")
        logging.info("cookie清除成功！")