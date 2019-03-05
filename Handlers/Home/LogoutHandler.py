import json
import logging
import tornado.web
from GlobalValue.GlobalValue import HomeSocketCash
from Methods.ConnectDB import cursor


class LogoutHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        userId = self.get_secure_cookie("userId").decode("utf-8")
        self.clear_cookie('userId')
        returnJson = {"status": "00"}
        self.write(json.dumps(returnJson, ensure_ascii=False))
        cursor.execute("UPDATE user SET login_state=0,state=0 WHERE user_id=%s", userId)
        for key in HomeSocketCash:
            HomeSocketCash[key].refreshFriendList()
        logging.info("cookie清除成功！")
