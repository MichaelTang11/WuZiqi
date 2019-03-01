import tornado.web
import json
from Methods.ConnectDB import cursor


class AddGroupHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        userId = self.get_secure_cookie("userId").decode("utf-8")
        groupName = self.get_argument("groupName")
        cursor.execute("INSERT INTO group_info(user_id, group_name) VALUES(%s,%s)", (userId, groupName))
        returnResult = {"status": "00"}
        self.write(json.dumps(returnResult, ensure_ascii=False))
