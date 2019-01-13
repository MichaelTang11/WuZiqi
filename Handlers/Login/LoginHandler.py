import hashlib
import logging
import tornado.web
from Methods.ConnectDB import con
from Methods.ConnectDB import cursor


class LoginHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        username = self.get_argument("username")
        code = self.get_argument("code")
        code2 = hashlib.md5(("s" + code + "a" + username + "ult").encode("utf-8")).hexdigest()
        con.ping()
        row_number = cursor.execute("select * from user WHERE username=%s AND code = %s", (username, code2))
        row = cursor.fetchone()
        if row_number != 0:
            self.set_secure_cookie("user_id", str(row['user_id']), expires_days=None)
            self.write("{'status':'True'}")
            logging.info("用户:" + username + "登录成功！")

        else:
            self.write("{'status':'False'}")
            logging.info("用户:" + username + "登录失败！")
