import tornado.web
import logging
from Methods.ConnectDB import con
from Methods.ConnectDB import cursor
import hashlib
import time


class SignInHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        # 注册handler，注册成功返回00，如有重复用户名返回01
        email = self.get_argument("sign_in_email")
        username = self.get_argument("sign_in_username")
        code = self.get_argument("code")
        code2 = hashlib.md5(("s" + code + "a" + username + "ult").encode("utf-8")).hexdigest()
        con.ping()
        row_number = cursor.execute("select * from user WHERE username=%s", username)
        if row_number == 0:
            cursor.execute("INSERT INTO user(username,code,email) VALUES(%s,%s,%s)", (username, code2, email))
            self.write("{'status':'00'}")
            logging.info("用户:" + username + "注册成功！")
            cursor.execute("SELECT user_id FROM user WHERE username=%s", username)
            row = cursor.fetchone()
            userId = row["user_id"]
            cursor.execute("INSERT INTO user_info(user_id,register_date) values (%s,%s)",
                           (userId, time.strftime('%Y-%m-%d', time.localtime())))
            logging.info("用户id:" + str(userId) + "插入user_info表成功")
            cursor.execute("INSERT INTO group_info(user_id, group_name) VALUES (%s,%s)", (userId, "我的好友"))
        else:
            self.write("{'status':'01'}")
            logging.info("用户:" + username + "注册失败！")
