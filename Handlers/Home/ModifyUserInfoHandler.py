import logging
import tornado.web
from Methods.ConnectDB import cursor


# TODO(Michael)上线时删除注释
class ModifyUserInfoHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        # userId=self.get_secure_cookie("user_id").decode("utf-8")
        userId = "1"
        birthday = self.get_argument("birthday")
        sex = self.get_argument("sex")
        email = self.get_argument("email")
        qq = self.get_argument("qq")
        cursor.execute("UPDATE user_info SET  sex=%s,birthday=%s,qq=%s,if_first_login=0 WHERE user_id=%s",
                       (sex, birthday, qq, userId))
        cursor.execute("UPDATE user SET email=%s WHERE user_id=%s", (email, userId))
        logging.info("用户:" + userId + "信息更新成功！")
