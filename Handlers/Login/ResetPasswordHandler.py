import hashlib
import logging
import tornado.web
from Methods.ConnectDB import cursor


class ResetPasswordHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        username = self.get_argument("username")
        code = self.get_argument("code")
        code2 = hashlib.md5(("s" + code + "a" + username + "ult").encode("utf-8")).hexdigest()
        cursor.execute("UPDATE user SET code=%s WHERE username =%s", (code2, username))
        logging.info("用户:" + username + "重置密码成功！")
