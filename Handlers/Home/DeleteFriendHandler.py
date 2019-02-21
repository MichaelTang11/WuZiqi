import logging
import tornado.web
from Methods.ConnectDB import cursor
from GlobalValue.GlobalValue import HomeSocketCash


# TODO(Michael):上线时需要将注释部分取消
class DeleteFriendHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        # user_id=self.get_secure_cookie("user_id").decode("utf-8")
        userId = '1'
        friendId = self.get_argument("friendId")
        cursor.execute("SELECT * FROM friend_info WHERE user_id=%s AND friend_id=%s", (userId, friendId))
        row = cursor.fetchone()
        oprId = row["opr_id"]
        cursor.execute("DELETE FROM friend_info WHERE opr_id=%s", oprId)
        if friendId in HomeSocketCash.keys():
            HomeSocketCash[friendId].refreshFriendList()
        logging.info("用户:" + userId + "删除好友！")
        self.write("{'status':'00'}")
