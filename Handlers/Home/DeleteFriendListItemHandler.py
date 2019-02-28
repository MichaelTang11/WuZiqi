import json
import tornado.web
import logging
from Methods.ConnectDB import cursor
from Methods.GetMessageFriendList import getMessageFriendList


# TODO(Michael)上线时删除注释
class DeleteFriendListItemHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        # 获取用户id
        # user_id = self.get_secure_cookie('user_id').decode("utf-8")
        userId = "1"
        friendId = self.get_argument("friendId")
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', 'x-requested-with')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, PUT, DELETE')
        # 获取messageFriendList
        messageFriendList = getMessageFriendList(userId)
        # 将待删除friendId与messageFriendList中进行比对
        # 若messageFriendlist长度为1，则直接删除
        # 若报送的friendId已为激活状态则将上一位设置为激活状态，并删除
        # 若不为激活状态则直接删除
        if len(messageFriendList) != 1:
            for key in range(0, len(messageFriendList)):
                if str(messageFriendList[key]["friendId"]) == friendId:
                    if messageFriendList[key]["activeState"] == 1:
                        cursor.execute(
                            "UPDATE message_friend_list SET active_state=1 WHERE user_id=%s AND friend_id=%s",
                            (userId, messageFriendList[key - 1]["friendId"]))
                        break
        cursor.execute("DELETE FROM message_friend_list WHERE user_id=%s AND friend_id=%s", (userId, friendId))
        logging.info("用户" + userId + "删除消息列表好友成功！")
        returnResult = {"status": "00"}
        self.write(json.dumps(returnResult, ensure_ascii=False))
