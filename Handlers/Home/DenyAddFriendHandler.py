import logging
import tornado.web
from Methods.ConnectDB import cursor


# TODO(Michael):上线时需要将注释部分取消
class DenyAddFriendHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        # userId=self.get_secure_cookie("user_id").decode("utf-8")
        userId = '1'
        fromId = self.get_argument("fromId")
        cursor.execute("DELETE FROM game_notification WHERE from_id=%s AND to_id=%s", (fromId, userId))
        logging.info("用户:" + userId + "拒绝好友请求！")
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', 'x-requested-with')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, PUT, DELETE')
        self.write("{'status':'00'}")
