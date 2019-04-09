import logging
import tornado.web
from Methods.ConnectDB import cursor
from GlobalValue.GlobalValue import GameRoomSocketCache,GameRoomCache
from Methods.RefreshRealtiveFriendList import refreshRelativeFriendList

class OnTimeDrawHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
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
        roomCache["playerState"][userId]["myTurn"] = False
        roomCache["playerState"][anotherPlayerId]["myTurn"] = False
        roomCache["totalGameTime"] += 1
        cursor.execute(
            "UPDATE user_info SET game_time=game_time+1,draw_time=draw_time+1 WHERE user_id=%s OR user_id=%s",
            (userId, anotherPlayerId))
        cursor.execute(
            "UPDATE game_table_info SET left_ready_state=0,right_ready_state=0,game_state=0 WHERE table_id=%s",
            tableId)
        # 将玩家状态改为在线，并通知其在线好友刷新friendList
        cursor.execute("UPDATE user SET state=1 WHERE user_id=%s OR user_id=%s", (userId, anotherPlayerId))
        # 刷新相关好友列表
        refreshRelativeFriendList([userId, anotherPlayerId])
        # 提醒前端和棋
        for key in GameRoomSocketCache[tableId]:
            GameRoomSocketCache[tableId][key].gameDraw()