import tornado.websocket
from GlobalValue.GlobalValue import GameRoomSocketCache, GameRoomCache, HomeSocketCache
from Methods.ConnectDB import cursor
import logging
import json

from Methods.RefreshRealtiveFriendList import refreshRelativeFriendList


class GameRoomWebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self, *args, **kwargs):
        userId = self.get_secure_cookie("userId").decode("utf-8")
        cursor.execute("SELECT * FROM user WHERE user_id=%s",userId)
        row = cursor.fetchone()
        tableId = row["table_id"]
        if tableId in GameRoomSocketCache.keys():
            GameRoomSocketCache[tableId].update({userId: self})
        else:
            GameRoomSocketCache[tableId] = {userId: self}
        logging.info(userId + "打开" + tableId + "房间连接")

    def on_close(self):
        userId = self.get_secure_cookie("userId").decode("utf-8")
        cursor.execute("SELECT * FROM user WHERE user_id=%s", userId)
        row = cursor.fetchone()
        tableId = row["table_id"]
        if tableId in GameRoomSocketCache.keys():
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
        if data["type"] == "01":
            userId = self.get_secure_cookie("userId").decode("utf-8")
            cursor.execute("SELECT * FROM user WHERE user_id=%s", userId)
            row = cursor.fetchone()
            tableId = row["table_id"]
            for key in GameRoomSocketCache[tableId].keys():
                if key!=userId:
                    returnData = {}
                    returnData["type"] = "08"
                    returnData["data"]=data["message"]
                    GameRoomSocketCache[tableId][key].write_message(json.dumps(returnData, ensure_ascii=False))

        if data["type"]=="02":
            userId = self.get_secure_cookie("userId").decode("utf-8")
            cursor.execute("SELECT * FROM user WHERE user_id=%s", userId)
            row = cursor.fetchone()
            tableId = row["table_id"]
            roomCache = GameRoomCache[tableId]
            anotherPlayerId = None
            for key in roomCache["playerState"].keys():
                if key != userId:
                    anotherPlayerId = key
                    break
            if data["result"]=="agree":
                roomCache["playerState"][userId]["myTurn"] = False
                roomCache["playerState"][anotherPlayerId]["myTurn"] = False
                roomCache["totalGameTime"] += 1
                cursor.execute(
                    "UPDATE user_info SET game_time=game_time+1,draw_time=draw_time+1 WHERE user_id=%s OR user_id=%s",
                    (userId, anotherPlayerId))
                cursor.execute(
                    "UPDATE game_table_info SET left_ready_state=0,right_ready_state=0,game_state=0 WHERE table_id=%s",
                    tableId)
                cursor.execute("UPDATE user SET state=1 WHERE user_id=%s OR user_id=%s", (userId, anotherPlayerId))
                # 将玩家状态改为在线，并通知其在线好友刷新friendList
                cursor.execute("UPDATE user SET state=1 WHERE user_id=%s OR user_id=%s", (userId, anotherPlayerId))
                # 刷新相关好友列表
                refreshRelativeFriendList([userId, anotherPlayerId])
                 # 提醒前端和棋
                for key in GameRoomSocketCache[tableId]:
                    GameRoomSocketCache[tableId][key].gameDraw()
            else:
                GameRoomSocketCache[tableId][anotherPlayerId].denyDraw()


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

    def gameWin(self, playerId):
        logging.info("决出胜者" + playerId)
        returnData = {"type": "05", "winnerId": playerId}
        self.write_message(json.dumps(returnData, ensure_ascii=False))

    def gameDraw(self):
        logging.info("游戏平局")
        returnData = {"type": "06"}
        self.write_message(json.dumps(returnData, ensure_ascii=False))

    def escapeGame(self):
        logging.info("对手逃离")
        returnData = {"type": "07"}
        self.write_message(json.dumps(returnData, ensure_ascii=False))

    def giveUp(self,playerId):
        logging.info(playerId+"投降！")
        returnData = {"type": "09", "looserId": playerId}
        self.write_message(json.dumps(returnData, ensure_ascii=False))

    def begDraw(self):
        returnData = {"type": "10"}
        self.write_message(json.dumps(returnData, ensure_ascii=False))

    def denyDraw(self):
        returnData = {"type": "11"}
        self.write_message(json.dumps(returnData, ensure_ascii=False))

    def closeWindow(self):
        returnData = {"type": "12"}
        self.write_message(json.dumps(returnData, ensure_ascii=False))