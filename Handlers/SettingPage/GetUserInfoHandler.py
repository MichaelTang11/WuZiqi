import json
import logging
import tornado.web
from Methods.ConnectDB import cursor


class GetUserInfoHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        userId = self.get_secure_cookie("userId").decode("utf-8")
        cursor.execute(
            "SELECT username,email,avatar,sex,birthday,qq FROM user left join user_info ON user.user_id=user_info.user_id WHERE user.user_id=%s",
            userId)
        returnResult = {"userInfo": cursor.fetchone()}
        logging.info("获取用户:" + userId + "信息成功！")
        self.write(json.dumps(returnResult, ensure_ascii=False))
