import json
import tornado.web
import logging
from Methods.ConnectDB import cursor
from Methods.GetMessageFriendList import getMessageFriendList
from GlobalValue.GlobalValue import HomeSocketCash


class ActiveMessageFriendListItemHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        # 获取用户id
        userId = self.get_secure_cookie('userId').decode("utf-8")
        friendId = self.get_argument("friendId")
        # 获取messageFriendList
        messageFriendList = getMessageFriendList(userId)
        # 对送报的friendId进行校验
        # 若再messageFriendList中无相同项，则将他人active状态置为0，并添加friendId将其active状态置为1
        # 若有相同项，则将他人active状态置为0，将其active状态置为1
        addFlag = True
        for item in messageFriendList:
            if str(item["friendId"]) == friendId:
                addFlag = False
                cursor.execute("UPDATE message_friend_list SET  active_state=0 WHERE user_id=%s AND friend_id!=%s;",
                               (userId, friendId))
                cursor.execute(
                    "UPDATE message_friend_list SET active_state=1,message_number=0 WHERE user_id=%s AND friend_id=%s;",
                    (userId, friendId))
                HomeSocketCash[userId].refreshMessageList(subType="01")
                break
        if addFlag:
            cursor.execute("UPDATE message_friend_list SET  active_state=0 WHERE user_id=%s ",
                           userId)
            cursor.execute("INSERT INTO message_friend_list (user_id, friend_id) values(%s,%s)", (userId, friendId))
        logging.info("用户" + userId + "更新好友active状态成功！")
        returnResult = {"status": "00"}
        self.write(json.dumps(returnResult, ensure_ascii=False))
