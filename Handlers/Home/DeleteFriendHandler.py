import logging
import tornado.web
from Methods.ConnectDB import cursor
from GlobalValue.GlobalValue import HomeSocketCash


class DeleteFriendHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        userId = self.get_secure_cookie("userId").decode("utf-8")
        friendId = self.get_argument("friendId")
        cursor.execute("SELECT * FROM friend_info WHERE user_id=%s AND friend_id=%s", (userId, friendId))
        row = cursor.fetchone()
        oprId = row["opr_id"]
        cursor.execute("DELETE FROM friend_info WHERE opr_id=%s", oprId)
        cursor.execute("DELETE FROM wuziqi.message_friend_list WHERE user_id=%s AND friend_id=%s",(userId,friendId))
        cursor.execute("DELETE FROM wuziqi.message_friend_list WHERE user_id=%s AND friend_id=%s", (friendId, userId))
        HomeSocketCash[userId].refreshMessageList(subType="04")
        if friendId in HomeSocketCash.keys():
            HomeSocketCash[friendId].refreshFriendList()
            HomeSocketCash[friendId].refreshMessageList(subType="04")
        logging.info("用户:" + userId + "删除好友！")
        self.write("{'status':'00'}")
