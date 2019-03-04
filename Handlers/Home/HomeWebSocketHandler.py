import tornado.websocket
import logging
from GlobalValue.GlobalValue import HomeSocketCash
from Methods.GetMessageFriendList import getMessageFriendList
from Methods.ConnectDB import cursor
import json
import time


class HomeWebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self, *args, **kwargs):
        userId=self.get_secure_cookie("userId").decode("utf-8")
        HomeSocketCash[userId] = self

    def on_message(self, message):
        data = json.loads(message)
        if data["type"]=="01":
            self.treatMessageData(data)
        if data["type"]=="02":
            self.clearMessageNotice(data)

    def on_close(self):
        userId=self.get_secure_cookie("userId").decode("utf-8")
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
        userId=self.get_secure_cookie("userId").decode("utf-8")
        friendId = data["friendId"]
        message = data["message"]
        logging.info("接受到消息:"+message)
        # 接收方MessageFriendList
        toMessageFriendList = getMessageFriendList(friendId)
        # 将数据插入数据库
        cursor.execute("INSERT INTO message_info (from_id, to_id, content, update_time)values(%s,%s,%s,%s) ",
                       (userId, friendId, message, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
        # 若messageFriendList不存在好友ID则插入
        # 若存在将message_friend_list中的message_number数量+1
        if len(toMessageFriendList)==0:
            cursor.execute(
                "INSERT INTO message_friend_list (USER_ID, FRIEND_ID, ACTIVE_STATE, MESSAGE_NUMBER)VALUES(%s,%s,%s,%s) ",
                (friendId, userId, 0, 1))
        else:
            for item in toMessageFriendList:
                if str(item["friendId"]) == userId:
                    cursor.execute(
                        "UPDATE message_friend_list SET message_number=message_number+1 WHERE user_id=%s AND friend_id=%s",
                        (friendId, userId))
                else:
                    cursor.execute(
                        "INSERT INTO message_friend_list (USER_ID, FRIEND_ID, ACTIVE_STATE, MESSAGE_NUMBER)VALUES(%s,%s,%s,%s) ",
                        (friendId, userId, 0, 1))
        #刷新toMessageFriendList
        toMessageFriendList = getMessageFriendList(friendId)
        #获取接收方消息窗口打开状态
        cursor.execute("SELECT * FROM user WHERE user_id=%s",friendId)
        row=cursor.fetchone()
        messageWidgetState=row["message_widget_state"]
        # 通知相应好友添加message
        #判断接受方是否在线
        if str(friendId) in HomeSocketCash.keys():
            if messageWidgetState==0:
                HomeSocketCash[str(friendId)].refreshMessageList(subType="04")
            else:
                for item in toMessageFriendList:
                    if item["friendId"]==userId and item["activeState"]==1:
                        HomeSocketCash[str(friendId)].refreshMessageList(subType="02",data=message)
                        break
                    if item["friendId"]==userId and item["activeState"]!=1:
                        HomeSocketCash[str(friendId)].refreshMessageList(subType="01")
                        HomeSocketCash[str(friendId)].refreshMessageList(subType="03")
                        break

    def clearMessageNotice(self,data):
        friendId = data["friendId"]
        userId = self.get_secure_cookie("userId").decode("utf-8")
        cursor.execute("UPDATE message_friend_list SET message_number=0 WHERE user_id=%s AND friend_id=%s",(userId,friendId))
        self.refreshMessageList(subType="01")