import logging
import tornado.web
from Methods.ConnectDB import cursor
import random


# TODO(Michael)之后需要通过websocket刷新相应好友页面
class AgreeAddFriendHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        userId=self.get_secure_cookie("user_id").decode("utf-8")
        fromId = self.get_argument("fromId")
        oprId = random.randint(0, 999999)
        cursor.execute("DELETE FROM game_notification WHERE from_id=%s AND to_id=%s",(fromId,userId))
        cursor.execute("SELECT * FROM group_info WHERE user_id=%s AND group_name='我的好友'", userId)
        row = cursor.fetchone()
        userDefaultGroupId = row["group_id"]
        cursor.execute("SELECT * FROM group_info WHERE user_id=%s AND group_name='我的好友'", fromId)
        row = cursor.fetchone()
        fromDefaultGroupId = row["group_id"]
        cursor.execute("INSERT INTO friend_info (user_id, friend_id, group_id, opr_id) VALUES (%s,%s,%s,%s)",
                       (userId, fromId, userDefaultGroupId, oprId))
        cursor.execute("INSERT INTO friend_info (user_id, friend_id, group_id, opr_id) VALUES (%s,%s,%s,%s)",
                       (fromId, userId, fromDefaultGroupId, oprId))
        logging.info("用户:" + userId + "好友添加成功！操作号" + str(oprId))
        logging.info("用户:" + fromId + "好友添加成功！操作号" + str(oprId))
        self.write("{'status':'00'}")