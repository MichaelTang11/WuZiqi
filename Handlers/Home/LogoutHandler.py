import json
import logging
import tornado.web
from GlobalValue.GlobalValue import HomeSocketCache,GameRoomSocketCache
from Methods.ConnectDB import cursor
from Methods.ExitGameRoom import exitGameRoom
from Methods.RefreshRealtiveFriendList import refreshRelativeFriendList


class LogoutHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        userId = self.get_secure_cookie("userId")
        if userId is None:
            returnJson = {"status": "00"}
            self.write(json.dumps(returnJson, ensure_ascii=False))
        else:
            userId=userId.decode("utf-8")
            cursor.execute("UPDATE user SET login_state=0,state=0 WHERE user_id=%s", userId)
            #查看是否关闭了GameRoom页面如果没有关闭则发送websocket关闭
            cursor.execute("SELECT * FROM user WHERE user_id=%s", userId)
            row = cursor.fetchone()
            tableId = row["table_id"]
            if tableId in GameRoomSocketCache.keys():
                if userId in GameRoomSocketCache[tableId].keys():
                    GameRoomSocketCache[tableId][userId].closeWindow()
                    exitGameRoom(userId, tableId)
                    del GameRoomSocketCache[tableId][userId]

            # 刷新相关好友列表
            refreshRelativeFriendList([userId])
            self.clear_all_cookies()
            logging.info("cookie清除成功！")
            returnJson = {"status": "00"}
            self.write(json.dumps(returnJson, ensure_ascii=False))
