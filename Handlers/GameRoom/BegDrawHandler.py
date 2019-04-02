import logging
import tornado.web
from GlobalValue.GlobalValue import GameRoomCache, HomeSocketCache, GameRoomSocketCache
from Methods.ConnectDB import cursor
import json


class BegDrawHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        userId = self.get_secure_cookie("userId").decode("utf-8")
        cursor.execute("SELECT * FROM user WHERE user_id=%s", userId)
        row = cursor.fetchone()
        tableId = row["table_id"]
        anotherPlayerId = None
        for key in GameRoomCache[tableId]["playerState"].keys():
            if key != userId:
                anotherPlayerId = key
                break
        logging.info(userId+"请求和棋")
        GameRoomSocketCache[tableId][anotherPlayerId].begDraw()