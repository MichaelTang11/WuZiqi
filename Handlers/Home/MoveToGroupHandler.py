import logging
import tornado.web
import json
from Methods.ConnectDB import cursor
from Methods.GetInitData import getInitData


# TODO(Michael)上线时删除注释
class MoveToGroupHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        userId=self.get_secure_cookie("user_id").decode("utf-8")
        friendId = self.get_argument("friendId")
        groupName = self.get_argument("groupName")
        cursor.execute("SELECT  * FROM group_info WHERE user_id=%s AND group_name=%s", (userId, groupName))
        row = cursor.fetchone()
        groupId = row["group_id"]
        cursor.execute("UPDATE friend_info SET group_id=%s WHERE user_id=%s AND friend_id=%s",
                       (groupId, userId, friendId))
        logging.info("用户ID:" + userId + "移动好友ID:" + friendId + "至分组:" + groupName + "成功！")
        self.write(json.dumps(getInitData(userId), ensure_ascii=False))
