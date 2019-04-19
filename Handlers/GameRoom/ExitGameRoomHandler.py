import logging
import tornado.web
from Methods.ConnectDB import cursor
from Methods.ExitGameRoom import exitGameRoom


class ExitGameRoomHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        userId = self.get_secure_cookie("userId")
        if userId is None:
            return
        userId = userId.decode("utf-8")
        cursor.execute("SELECT * FROM user WHERE user_id=%s", userId)
        row = cursor.fetchone()
        tableId = row["table_id"]
        if tableId is None:
            return
        exitGameRoom(userId, str(tableId))
        logging.info(userId + "退出游戏房间!")
