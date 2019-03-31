import logging
import tornado.web
from Methods.ConnectDB import cursor
from GlobalValue.GlobalValue import HomeSocketCache
from GlobalValue.GlobalValue import GameRoomSocketCache


class SitDownHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        userId = self.get_secure_cookie("userId").decode("utf-8")
        oldTableId = self.get_secure_cookie("tableId")
        position = self.get_argument("position")
        tableId = self.get_argument("tableId")

        # 根据前端中的cookies值判断是否为坐下状态
        if oldTableId:
            oldTableId = oldTableId.decode("utf-8")
            sitDownState = True
        else:
            sitDownState = False

        # 根据不同的状态对数据库进行操作
        if sitDownState:
            # 查询数据库若已处于游戏状态中则不能更换位置
            cursor.execute("SELECT * FROM game_table_info WHERE left_player_id=%s OR right_player_id=%s",
                           (userId, userId))
            row = cursor.fetchone()
            if row["game_state"]== 1 or (row["left_ready_state"]==1 and str(row["left_player_id"])==userId) or (row["right_ready_state"]==1 and str(row["right_player_id"])==userId):
                self.write("{'status':'01'}")
                # 已经处于游戏状态无法换桌
                logging.info("write {'status':'01'}")
                return
            # 将tableId进行utf8编码
            # 将旧卓的信息删除
            if str(row["left_player_id"]) == userId:
                cursor.execute("UPDATE game_table_info SET left_player_id=NULL WHERE table_id=%s", oldTableId)
            else:
                cursor.execute("UPDATE game_table_info SET right_player_id=NULL WHERE table_id=%s", oldTableId)

        if position == "left":
            cursor.execute("UPDATE game_table_info SET left_player_id=%s WHERE table_id=%s ", (userId, tableId))
        else:
            cursor.execute("UPDATE game_table_info SET right_player_id=%s WHERE table_id=%s ", (userId, tableId))

        # 组装刷新数据并通知前端刷新游戏大厅
        if not sitDownState:
            rowNumber = cursor.execute(
                "SELECT a.table_id,a.left_player_id,c.username AS left_username,b.avatar AS left_avatar,a.right_player_id,e.username AS right_username,d.avatar AS right_avatar,a.game_state FROM game_table_info AS a LEFT join user_info AS b ON a.left_player_id=b.user_id LEFT JOIN  user AS c ON b.user_id=c.user_id LEFT JOIN user_info AS d ON a.right_player_id=d.user_id LEFT JOIN user AS e ON e.user_id=d.user_id WHERE a.table_id=%s",
                tableId)
        else:
            rowNumber = cursor.execute(
                "SELECT a.table_id,a.left_player_id,c.username AS left_username,b.avatar AS left_avatar,a.right_player_id,e.username AS right_username,d.avatar AS right_avatar,a.game_state FROM game_table_info AS a LEFT join user_info AS b ON a.left_player_id=b.user_id LEFT JOIN  user AS c ON b.user_id=c.user_id LEFT JOIN user_info AS d ON a.right_player_id=d.user_id LEFT JOIN user AS e ON e.user_id=d.user_id WHERE a.table_id=%s OR a.table_id=%s",
                (tableId, oldTableId))
        refreshData = []
        for i in range(0, rowNumber):
            row = cursor.fetchone()
            temp = {"tableId": row["table_id"], "leftPlayerId": row["left_player_id"],
                    "leftUsername": row["left_username"],
                    "leftAvatar": row["left_avatar"], "rightPlayerId": row["right_player_id"],
                    "rightUsername": row["right_username"], "rightAvatar": row["right_avatar"],
                    "gameState": row["game_state"]}
            refreshData.append(temp)
        for key in HomeSocketCache:
            HomeSocketCache[key].refreshGameTableList(refreshData)
        #设置cookie及返回值
        self.set_secure_cookie("tableId", tableId)
        if not sitDownState:
            self.write("{'status':'00'}")
            logging.info("write {'status':'00'}")
        else:
            self.write("{'status':'02'}")
            logging.info("write {'status':'02'}")
            GameRoomSocketCache[oldTableId][userId].refreshGameRoom()
            del GameRoomSocketCache[oldTableId][userId]
            logging.info(userId + "关闭" + tableId + "房间连接")
            if len(GameRoomSocketCache[tableId]) == 0:
                del GameRoomSocketCache[tableId]

        #刷新相关房间的用户页面
        if tableId in GameRoomSocketCache.keys():
            for key in GameRoomSocketCache[tableId].keys():
                GameRoomSocketCache[tableId][key].refreshGameRoom()
        if oldTableId in GameRoomSocketCache.keys():
            for key in GameRoomSocketCache[oldTableId].keys():
                GameRoomSocketCache[oldTableId][key].refreshGameRoom()