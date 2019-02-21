import json
import logging
import tornado.web
from Methods.ConnectDB import cursor


class GetUserProfileHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        username = self.get_argument("username")
        cursor.execute(
            "SELECT a.username,b.avatar,b.sex,b.birthday,b.qq,b.register_date,b.last_login_date,b.game_time,b.win_time FROM user AS a LEFT JOIN user_info AS b ON a.user_id=b.user_id WHERE a.username=%s",
            username)
        returnResult = {}
        content = {}
        row = cursor.fetchone()
        content["username"] = row["username"]
        content["avatar"] = row["avatar"]
        content["sex"] = row["sex"]
        content["birthday"] = row["birthday"]
        content["qq"] = row["qq"]
        content["registerDate"] = row["register_date"]
        content["lastLoginDate"] = row["last_login_date"]
        content["gameTime"] = row["game_time"]
        content["winTime"] = row["win_time"]
        returnResult["userProfile"] = content
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', 'x-requested-with')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, PUT, DELETE')
        logging.info("获取用户:" + username + "信息成功！")
        self.write(json.dumps(returnResult, ensure_ascii=False))
