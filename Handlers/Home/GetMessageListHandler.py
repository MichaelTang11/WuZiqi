import logging
import tornado.web
from Methods.ConnectDB import cursor
import json


# TODO(Michael)上线时删除注释
class GetMessageListHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        # userId=self.get_secure_cookie("user_id").decode("utf-8")
        userId = "1"
        friendId = self.get_argument("friendId")
        viewName = "user_" + str(userId) + "_message"
        rowNumber = cursor.execute(
            "SELECT a.content,a.type FROM " + viewName + " AS a WHERE related_user=%s ORDER BY update_time", friendId)
        returnData = []
        for i in range(0, rowNumber):
            row = cursor.fetchone()
            returnData.append(row)
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', 'x-requested-with')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, PUT, DELETE')
        self.write(json.dumps(returnData, ensure_ascii=False))
