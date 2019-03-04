import logging
import tornado.web
from Methods.ConnectDB import cursor
import json


class GetMessageListHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        userId=self.get_secure_cookie("userId").decode("utf-8")
        friendId = self.get_argument("friendId")
        viewName = "user_" + str(userId) + "_message"
        rowNumber = cursor.execute(
            "SELECT a.content,a.type FROM " + viewName + " AS a WHERE related_user=%s ORDER BY update_time", friendId)
        returnData = []
        for i in range(0, rowNumber):
            row = cursor.fetchone()
            returnData.append(row)
        self.write(json.dumps(returnData, ensure_ascii=False))
        logging.info("用户:"+userId+"获取消息成功！")
