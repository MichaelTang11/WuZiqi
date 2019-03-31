import tornado.websocket
from GlobalValue.GlobalValue import GameRoomSocketCache
import logging
import json


class GameRoomWebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self, *args, **kwargs):
        userId = self.get_secure_cookie("userId").decode("utf-8")
        tableId = self.get_secure_cookie("tableId").decode("utf-8")
        if tableId in GameRoomSocketCache.keys():
            GameRoomSocketCache[tableId].update({userId: self})
        else:
            GameRoomSocketCache[tableId] = {userId: self}
        logging.info(userId + "打开" + tableId + "房间连接")

    def on_close(self):
        userId = self.get_secure_cookie("userId").decode("utf-8")
        tableId=self.get_secure_cookie("tableId").decode("utf-8")
        if tableId in GameRoomSocketCache.keys() :
            if userId in GameRoomSocketCache[tableId].keys():
                del GameRoomSocketCache[tableId][userId]
                logging.info(userId + "关闭" + tableId + "房间连接")
                if len(GameRoomSocketCache[tableId]) == 0:
                    del GameRoomSocketCache[tableId]

    def check_origin(self, origin):
        return True

    def on_message(self, message):
        data = json.loads(message)
        if data["type"] == "00":
            self.maintainConnection()

    def refreshGameRoom(self):
        logging.info("刷新GameRoom")
        returnData = {}
        returnData["type"] = "00"
        self.write_message(json.dumps(returnData, ensure_ascii=False))

    # 心跳包处理
    def maintainConnection(self):
        userId = self.get_secure_cookie("userId").decode("utf-8")
        returnData = {"type": "01"}
        self.write_message(json.dumps(returnData, ensure_ascii=False))
        logging.info("用户：" + userId + "发送心跳包")

    def gameStart(self):
        logging.info("游戏开始")
        returnData = {"type": "02"}
        self.write_message(json.dumps(returnData, ensure_ascii=False))

    def refreshPlayerStatus(self):
        logging.info("刷新player-status")
        returnData = {"type": "03"}
        self.write_message(json.dumps(returnData, ensure_ascii=False))

    def refreshGameView(self):
        logging.info("刷新gameView")
        returnData = {"type": "04"}
        self.write_message(json.dumps(returnData, ensure_ascii=False))

    def gameWin(self,playerId):
        logging.info("决出胜者"+playerId)
        returnData={"type": "05","winnerId":playerId}
        self.write_message(json.dumps(returnData, ensure_ascii=False))

    def gameDraw(self):
        logging.info("游戏平局")
        returnData={"type": "06"}
        self.write_message(json.dumps(returnData, ensure_ascii=False))

    def escapeGame(self):
        logging.info("对手逃离")
        returnData = {"type": "07"}
        self.write_message(json.dumps(returnData, ensure_ascii=False))