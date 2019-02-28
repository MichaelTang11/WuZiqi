import tornado.websocket
import logging
from GlobalValue.GlobalValue import HomeSocketCash
from Methods.GetMessageFriendList import getMessageFriendList
from Methods.ConnectDB import cursor
import json
import time


# TODO(Michael):上线时需要将注释部分取消
class HomeWebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self, *args, **kwargs):
        # userId=self.get_secure_cookie("user_id").decode("utf-8")
        userId = "1"
        HomeSocketCash[userId] = self

    def on_message(self, message):
        self.treatMessageData(message)

    def on_close(self):
        # userId=self.get_secure_cookie("user_id").decode("utf-8")
        userId = "1"
        del HomeSocketCash[userId]

    def check_origin(self, origin):
        return True

    def refreshFriendList(self):
        returnData = {}
        returnData["type"] = "01"
        self.write_message(json.dumps(returnData, ensure_ascii=False))

    def refreshNotificationList(self):
        returnData = {}
        returnData["type"] = "02"
        self.write_message(json.dumps(returnData, ensure_ascii=False))

    def refreshMessageList(self, **parm):
        returnData = {}
        returnData["type"] = "03"
        for key in parm:
            returnData[key] = parm[key]
        self.write_message(json.dumps(returnData, ensure_ascii=False))

    def refreshGameTableList(self, refreshData):
        logging.info("刷新game-table")
        returnData = {}
        returnData["type"] = "04"
        returnData["refreshData"] = refreshData
        self.write_message(json.dumps(returnData, ensure_ascii=False))

    def treatMessageData(self, data):
        data = json.loads(data)
        # userId=self.get_secure_cookie("user_id").decode("utf-8")
        userId = "1"
        friendId = data["friendId"]
        message = data["message"]

        # 接收方MessageFriendList
        toMessageFriendList = getMessageFriendList(friendId)
        # 将数据插入数据库
        cursor.execute("INSERT INTO message_info (from_id, to_id, content, update_time)values(%s,%s,%s,%s) ",
                       (userId, friendId, message, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
        # 若messageFriendList不存在好友ID则插入
        # 若存在将message_friend_list中的message_number数量+1
        for item in toMessageFriendList:
            if item["friendId"] == userId:
                cursor.execute(
                    "UPDATE message_friend_list SET message_number=message_number+1 WHERE user_id=%s AND friend_id=%s",
                    (friendId, userId))
            else:
                cursor.execute(
                    "INSERT INTO message_friend_list (USER_ID, FRIEND_ID, ACTIVE_STATE, MESSAGE_NUMBER)VALUES(%s,%s,%s,%s) ",
                    (friendId, userId, 0, 1))
        # 通知相应好友添加message
        if friendId in HomeSocketCash.keys():
            for item in toMessageFriendList:
                if item["friendId"] == userId and item["activeState"] == 1:
                    HomeSocketCash[friendId].refreshMessageList(subType="02", data=message)
                    break
