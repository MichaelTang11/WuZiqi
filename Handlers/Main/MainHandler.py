# 路由跳转handler
import logging
import tornado.web


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        userId = self.get_secure_cookie('userId')
        if userId:
            self.redirect("Home.html")
            logging.info("redirect Home.html")
        else:
            self.redirect("Login.html")
            logging.info("redirect Login.html")
