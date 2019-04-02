import logging
import tornado.web

from GlobalValue.GlobalValue import GameRoomCache, HomeSocketCache, GameRoomSocketCache
from Methods.GetGameRoomData import getGameRoomData
from Methods.ConnectDB import cursor
import json


class GiveUpHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        userId = self.get_secure_cookie("userId").decode("utf-8")
        cursor.execute("SELECT * FROM user WHERE user_id=%s", userId)
        row = cursor.fetchone()
        tableId = row["table_id"]
        self.set_header('Content-type', 'application/json')
        roomCache = GameRoomCache[tableId]
        anotherPlayerId = None
        for key in roomCache["playerState"].keys():
            if key != userId:
                anotherPlayerId = key
                break

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
        playerList = [userId, anotherPlayerId]
        for i in range(0, 2):
            rowNumber = cursor.execute(
                "SELECT * FROM friend_info AS a LEFT JOIN `user` AS b ON a.friend_id=b.user_id WHERE a.user_id=%s and b.login_state=1",
                playerList[i])
            for j in range(0, rowNumber):
                row = cursor.fetchone()
                HomeSocketCache[str(row["friend_id"])].refreshFriendList()

        GameRoomSocketCache[tableId][anotherPlayerId].refreshGameView()

        # 提醒前端认输
        for key in GameRoomSocketCache[tableId]:
            GameRoomSocketCache[tableId][key].giveUp(userId)