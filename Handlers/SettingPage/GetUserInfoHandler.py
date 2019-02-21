import json
import logging
import tornado.web
from Methods.ConnectDB import cursor


# TODO(Michael)上线时删除注释
class GetUserInfoHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        # userId=self.get_secure_cookie("user_id").decode("utf-8")
        userId = "1"
        cursor.execute(
            "SELECT username,email,avatar,sex,birthday,qq FROM user left join user_info ON user.user_id=user_info.user_id WHERE user.user_id=%s",
            userId)
        returnResult = {"userInfo": cursor.fetchone()}
        logging.info("获取用户:" + userId + "信息成功！")
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', 'x-requested-with')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, PUT, DELETE')
        self.write(json.dumps(returnResult, ensure_ascii=False))
