import json
import logging
import tornado.web
from GlobalValue.GlobalValue import HomeSocketCache
from Methods.ConnectDB import cursor


class LogoutHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        userId = self.get_secure_cookie("userId").decode("utf-8")
        returnJson = {"status": "00"}
        self.write(json.dumps(returnJson, ensure_ascii=False))
        cursor.execute("UPDATE user SET login_state=0,state=0 WHERE user_id=%s", userId)
        tableId = self.get_secure_cookie("tableId")
        if tableId is not None:
            cursor.execute("UPDATE game_table_info SET left_player_id=NULL WHERE table_id=%s AND left_player_id=%s",
                           (tableId, userId))
            cursor.execute("UPDATE game_table_info SET right_player_id=NULL WHERE table_id=%s AND right_player_id=%s",
                           (tableId, userId))
        for key in HomeSocketCache:
            HomeSocketCache[key].refreshFriendList()
        if tableId is not None:
            for key in HomeSocketCache:
                HomeSocketCache[key].refreshGameTableList()
        self.clear_all_cookies()
        logging.info("cookie清除成功！")
