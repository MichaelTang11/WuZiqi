import json
import logging
import time
import tornado.web
from Methods.ConnectDB import cursor
from GlobalValue.GlobalValue import GameRoomSocketCache,GameRoomCache
from Methods.RefreshRealtiveFriendList import refreshRelativeFriendList

class OverTimeHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        self.set_header('Content-type', 'application/json')
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
        # 对GameRoomCache进行更改
        roomCache["playerState"][userId]["myTurn"] = False
        roomCache["playerState"][userId]["overTimeCount"] +=1
        roomCache["playerState"][anotherPlayerId]["myTurn"] = True
        roomCache["playerState"][anotherPlayerId]["chessTime"] = time.time() * 1000
        returnData = {"status": "00"}
        self.write(json.dumps(returnData, ensure_ascii=False))
        # 通知前端调用交换棋权
        GameRoomSocketCache[tableId][anotherPlayerId].refreshGameView()
        if roomCache["playerState"][userId]["overTimeCount"]==2:
            #当超时次数超过两次直接判输
            roomCache["playerState"][userId]["myTurn"] = False
            roomCache["playerState"][anotherPlayerId]["winTime"] += 1
            roomCache["playerState"][anotherPlayerId]["myTurn"] = False
            roomCache["totalGameTime"] += 1
            cursor.execute("UPDATE user_info SET game_time=game_time+1 WHERE user_id=%s OR user_id=%s",
                           (userId, anotherPlayerId))
            cursor.execute("UPDATE user_info SET win_time=win_time+1 WHERE user_id=%s", anotherPlayerId)
            cursor.execute(
                "UPDATE game_table_info SET left_ready_state=0,right_ready_state=0,game_state=0 WHERE table_id=%s",
                tableId)
            # 将玩家状态改为在线，并通知其在线好友刷新friendList
            cursor.execute("UPDATE user SET state=1 WHERE user_id=%s OR user_id=%s", (userId, anotherPlayerId))
            # 刷新相关好友列表
            refreshRelativeFriendList([userId, anotherPlayerId])

            logging.info("玩家" + anotherPlayerId + "获胜")
            # 提醒前端胜负已分
            for key in GameRoomSocketCache[tableId]:
                GameRoomSocketCache[tableId][key].gameWin(anotherPlayerId)

