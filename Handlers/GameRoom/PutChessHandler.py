import logging
import time
import tornado.web
import json
from GlobalValue.GlobalValue import GameRoomSocketCache
from GlobalValue.GlobalValue import GameRoomCache
from Methods.JudgeWin import judgeWin
from Methods.ConnectDB import cursor
from Methods.RefreshRealtiveFriendList import refreshRelativeFriendList


class PutChessHandler(tornado.web.RequestHandler):
    def post(self):
        self.set_header('Content-type', 'application/json')
        userId = self.get_secure_cookie("userId").decode("utf-8")
        cursor.execute("SELECT * FROM user WHERE user_id=%s", userId)
        row = cursor.fetchone()
        tableId = row["table_id"]
        chessType = self.get_argument("chessType")
        x = self.get_argument("x")
        y = self.get_argument("y")
        logging.info("玩家" + userId + "下棋" + "index" + str([x, y]))
        roomCache = GameRoomCache[tableId]
        anotherPlayerId = None
        for key in roomCache["playerState"].keys():
            if key != userId:
                anotherPlayerId = key
                break
        # 对GameRoomCache进行更改
        roomCache["playerState"][userId]["myTurn"] = False
        roomCache["playerState"][anotherPlayerId]["myTurn"] = True
        roomCache["playerState"][anotherPlayerId]["chessTime"] = time.time()*1000
        roomCache["stepRecord"].append({"playerId": userId,
                                        "chessType": chessType,
                                        "point": [x, y]
                                        })
        # 对pointState进行更改
        pointState = roomCache["pointState"]
        if chessType == "black":
            pointState[int(x)][int(y)] = 1
        else:
            pointState[int(x)][int(y)] = 2
        # 判断输赢
        winFlag = False
        drawFlag = False
        if judgeWin(pointState, {"chessType": chessType, "chessPoint": [int(x), int(y)]}):
            winFlag = True
            roomCache["playerState"][userId]["myTurn"] = False
            roomCache["playerState"][userId]["winTime"] += 1
            roomCache["playerState"][anotherPlayerId]["myTurn"] = False
            roomCache["totalGameTime"] += 1
            cursor.execute("UPDATE user_info SET game_time=game_time+1 WHERE user_id=%s OR user_id=%s",
                           (userId, anotherPlayerId))
            cursor.execute("UPDATE user_info SET win_time=win_time+1 WHERE user_id=%s", userId)
            cursor.execute(
                "UPDATE game_table_info SET left_ready_state=0,right_ready_state=0,game_state=0 WHERE table_id=%s",
                tableId)
            # 将玩家状态改为在线，并通知其在线好友刷新friendList
            cursor.execute("UPDATE user SET state=1 WHERE user_id=%s OR user_id=%s", (userId, anotherPlayerId))
            # 刷新相关好友列表
            refreshRelativeFriendList([userId, anotherPlayerId])
        # 和棋
        if len(roomCache["stepRecord"]) == 196:
            drawFlag = True
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
        returnData = {"status": "00"}
        self.write(json.dumps(returnData, ensure_ascii=False))
        # 通知前端调用交换棋权
        GameRoomSocketCache[tableId][anotherPlayerId].refreshGameView()
        if winFlag:
            logging.info("玩家" + userId + "获胜")
            # 提醒前端胜负已分
            for key in GameRoomSocketCache[tableId]:
                GameRoomSocketCache[tableId][key].gameWin(userId)
        if drawFlag:
            logging.info(tableId + "和局")
            # 提醒前端和棋
            for key in GameRoomSocketCache[tableId]:
                GameRoomSocketCache[tableId][key].gameDraw()
