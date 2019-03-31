import logging
import tornado.web
from Methods.GetGameRoomData import getGameRoomData
import json


class GetGameRoomDataHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        userId = self.get_secure_cookie("userId").decode("utf-8")
        tableId=self.get_secure_cookie("tableId").decode("utf-8")
        logging.info("获取桌号" + str(tableId)+"初始化信息")
        self.set_header('Content-type', 'application/json')
        self.set_header('Access-Control-Allow-Origin', '*')
        returnData=getGameRoomData(tableId)
        returnData["whoGet"]=userId
        self.write(json.dumps(returnData, ensure_ascii=False))
