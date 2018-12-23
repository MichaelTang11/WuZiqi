from Methods.ConnectDB import con
from Methods.ConnectDB import cursor
import tornado.web
import logging

class CheckUserHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        username = self.get_argument("username")
        con.ping()
        row_number = cursor.execute("select * from user WHERE username=%s", username)
        if row_number != 0:
            self.write("{'status':'00'}")
            logging.info("用户:" + username + "查询成功！")
        else:
            self.write("{'status':'01'}")
            logging.info("用户:" + username + "无此用户名！")