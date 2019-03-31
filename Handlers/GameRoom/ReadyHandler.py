import logging
import tornado.web
from Methods.ConnectDB import cursor
from Methods.InitGame import initGame
from GlobalValue.GlobalValue import GameRoomSocketCache
import json


class ReadyHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        self.set_header('Content-type', 'application/json')
        userId = self.get_secure_cookie("userId").decode("utf-8")
        tableId=self.get_secure_cookie("tableId").decode("utf-8")
        readyState=self.get_argument("readyState")
        rowNumber=cursor.execute("SELECT * FROM game_table_info WHERE left_player_id=%s AND table_id=%s",(userId,tableId))
        if rowNumber>=1:
            #用户坐在左边
            if readyState=="0":
                cursor.execute("UPDATE game_table_info SET left_ready_state=1 WHERE table_id=%s",tableId)
            else:
                cursor.execute("UPDATE game_table_info SET left_ready_state=0 WHERE table_id=%s", tableId)
        else:
            # 用户坐在右边
            if readyState=="0":
                cursor.execute("UPDATE game_table_info SET right_ready_state=1 WHERE table_id=%s", tableId)
            else:
                cursor.execute("UPDATE game_table_info SET right_ready_state=1 WHERE table_id=%s", tableId)
        returnData = {"status": "00"}
        self.write(json.dumps(returnData, ensure_ascii=False))
        #通知房间内的玩家刷新player-status
        for key in GameRoomSocketCache[tableId].keys():
            GameRoomSocketCache[tableId][key].refreshPlayerStatus()

        #判断是否双方都已准备开始游戏，并在公共变量中添加GameRoomCache
        cursor.execute("SELECT * FROM game_table_info WHERE table_id=%s",tableId)
        row=cursor.fetchone()
        if row["left_ready_state"]==1 and row["right_ready_state"]==1:
            initGame(tableId)
