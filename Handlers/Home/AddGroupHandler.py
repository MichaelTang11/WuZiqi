import tornado.web
import json
from Methods.ConnectDB import cursor


# TODO(Michael):上线时需要将注释部分取消
class AddGroupHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        # user_id=self.get_secure_cookie("user_id").decode("utf-8")
        userId = '1'
        groupName = self.get_argument("groupName")
        cursor.execute("INSERT INTO group_info(user_id, group_name) VALUES(%s,%s)", (userId, groupName))
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', 'x-requested-with')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, PUT, DELETE')
        returnResult = {"status": "00"}
        self.write(json.dumps(returnResult, ensure_ascii=False))
