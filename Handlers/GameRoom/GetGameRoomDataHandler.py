import logging
import tornado.web
from Methods.GetGameRoomData import getGameRoomData
from Methods.ConnectDB import cursor
import json


class GetGameRoomDataHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        userId = self.get_secure_cookie("userId").decode("utf-8")
        cursor.execute("SELECT * FROM user WHERE user_id=%s", userId)
        row = cursor.fetchone()
        tableId = row["table_id"]
        logging.info("获取桌号" + tableId + "初始化信息")
        self.set_header('Content-type', 'application/json')
        returnData = getGameRoomData(tableId)
        returnData["whoGet"] = userId
        self.write(json.dumps(returnData, ensure_ascii=False))
