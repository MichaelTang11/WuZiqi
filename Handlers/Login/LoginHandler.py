import hashlib
import logging
import tornado.web
from Methods.ConnectDB import con
from Methods.ConnectDB import cursor
import time


class LoginHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        username = self.get_argument("username")
        code = self.get_argument("code")
        code2 = hashlib.md5(("s" + code + "a" + username + "ult").encode("utf-8")).hexdigest()
        con.ping()
        row_number = cursor.execute("select * from user WHERE username=%s AND code = %s", (username, code2))
        row = cursor.fetchone()
        if row_number != 0:
            self.set_secure_cookie("userId", str(row['user_id']), expires_days=None)
            self.write("{'status':'True'}")
            cursor.execute("UPDATE user_info SET last_login_date =%s WHERE user_id=%s",
                           (time.strftime('%Y-%m-%d', time.localtime()), str(row['user_id'])))
            logging.info("用户:" + username + "登录成功！")

        else:
            self.write("{'status':'False'}")
            logging.info("用户:" + username + "登录失败！")
