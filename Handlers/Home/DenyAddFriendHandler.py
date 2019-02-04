import logging
import tornado.web
from Methods.ConnectDB import cursor


# TODO(Michael)之后需要通过websocket刷新相应好友页面
class DenyAddFriendHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        userId=self.get_secure_cookie("user_id").decode("utf-8")
        fromId = self.get_argument("fromId")
        cursor.execute("DELETE FROM game_notification WHERE from_id=%s AND to_id=%s",(fromId,userId))
        logging.info("用户:" + userId + "拒绝好友请求！" )
        self.write("{'status':'00'}")