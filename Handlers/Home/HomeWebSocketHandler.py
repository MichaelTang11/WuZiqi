import tornado.websocket
import logging
from GlobalValue.GlobalValue import HomeSocketCash
import json

class HomeWebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self, *args, **kwargs):
        # userId=self.get_secure_cookie("user_id").decode("utf-8")
        userId = "1"
        HomeSocketCash[userId]=self

    def on_message(self, message):
        logging.info(message)
        # self.write_message("receieved your message!")

    def on_close(self):
        # userId=self.get_secure_cookie("user_id").decode("utf-8")
        userId = "1"
        del HomeSocketCash[userId]

    def check_origin(self, origin):
        return True

    def refreshFriendList(self):
        returnData={}
        returnData["type"]="01"
        self.write_message(json.dumps(returnData, ensure_ascii=False))

    def refreshNotificationList(self):
        returnData = {}
        returnData["type"] = "02"
        self.write_message(json.dumps(returnData, ensure_ascii=False))

    def refreshMessageList(self):
        returnData = {}
        returnData["type"] = "03"
        self.write_message(json.dumps(returnData, ensure_ascii=False))

    def refreshGameTableList(self,refreshData):
        logging.info("刷新game-table")
        returnData = {}
        returnData["type"] = "04"
        returnData["refreshData"]=refreshData
        self.write_message(json.dumps(returnData, ensure_ascii=False))