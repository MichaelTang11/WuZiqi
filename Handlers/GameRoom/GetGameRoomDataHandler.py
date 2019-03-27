import logging
import tornado.web
from Methods.GetGameRoomData import getGameRoomData
import json


class GetGameRoomDataHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        tableId=self.get_secure_cookie("tableId").decode("utf-8")
        logging.info("获取桌号" + str(tableId)+"初始化信息")
        self.set_header('Content-type', 'application/json')
        self.set_header('Access-Control-Allow-Origin', '*')
        self.write(json.dumps(getGameRoomData(tableId), ensure_ascii=False))
