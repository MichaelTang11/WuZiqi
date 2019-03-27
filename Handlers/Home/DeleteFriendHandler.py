import logging
import tornado.web
from Methods.ConnectDB import cursor
from GlobalValue.GlobalValue import HomeSocketCache
from Methods.GetMessageFriendList import getMessageFriendList


class DeleteFriendHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        userId = self.get_secure_cookie("userId").decode("utf-8")
        friendId = self.get_argument("friendId")
        cursor.execute("SELECT * FROM friend_info WHERE user_id=%s AND friend_id=%s", (userId, friendId))
        row = cursor.fetchone()
        oprId = row["opr_id"]
        cursor.execute("DELETE FROM friend_info WHERE opr_id=%s", oprId)
        #删除user的messageFriendList
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
        # 删除friend的messageFriendList
        messageFriendList = getMessageFriendList(friendId)
        # 将待删除friendId与messageFriendList中进行比对
        # 若messageFriendlist长度为1，则直接删除
        # 若报送的friendId已为激活状态则将上一位设置为激活状态，并删除
        # 若不为激活状态则直接删除
        if len(messageFriendList) != 1:
            for key in range(0, len(messageFriendList)):
                if str(messageFriendList[key]["friendId"]) == userId:
                    if messageFriendList[key]["activeState"] == 1:
                        cursor.execute(
                            "UPDATE message_friend_list SET active_state=1 WHERE user_id=%s AND friend_id=%s",
                            (friendId, messageFriendList[key - 1]["friendId"]))
                        break
        cursor.execute("DELETE FROM message_friend_list WHERE user_id=%s AND friend_id=%s", (friendId, userId))
        HomeSocketCache[userId].refreshMessageList(subType="04")
        if friendId in HomeSocketCache.keys():
            HomeSocketCache[friendId].refreshFriendList()
            HomeSocketCache[friendId].refreshMessageList(subType="04")
        logging.info("用户:" + userId + "删除好友！")
        self.write("{'status':'00'}")
