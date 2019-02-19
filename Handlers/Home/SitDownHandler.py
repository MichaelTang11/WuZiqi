import logging
import tornado.web
from Methods.ConnectDB import cursor
from GlobalValue.GlobalValue import HomeSocketCash

class SitDownHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        # userId=self.get_secure_cookie("user_id").decode("utf-8")
        oldTableId=None
        userId = "1"
        position=self.get_argument("position")
        tableId=self.get_argument("tableId")
        rowNumber = cursor.execute("SELECT * FROM game_table_info WHERE right_player_id=%s OR left_player_id=%s",
                                   (userId, userId))
        if rowNumber == 0:
            sitDownState = False
        else:
            sitDownState = True
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', 'x-requested-with')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, PUT, DELETE')
        if sitDownState:
            cursor.execute("SELECT * FROM game_table_info WHERE left_player_id=%s OR right_player_id=%s",(userId,userId))
            row=cursor.fetchone()
            if row["game_state"]==1:
                self.write("{'status':'01'}")
                #已经处于游戏状态无法换桌
                logging.info("write {'status':'01'}")
                return
            oldTableId=row["table_id"]
            if str(row["left_player_id"])==userId :
                cursor.execute("UPDATE game_table_info SET left_player_id=NULL WHERE table_id=%s",oldTableId)
            else:
                cursor.execute("UPDATE game_table_info SET right_player_id=NULL WHERE table_id=%s", oldTableId)

        if position=="left":
            cursor.execute("UPDATE game_table_info SET left_player_id=%s WHERE table_id=%s ",(userId,tableId))
        else:
            cursor.execute("UPDATE game_table_info SET right_player_id=%s WHERE table_id=%s ", (userId, tableId))

        if oldTableId is None:
            rowNumber=cursor.execute("SELECT a.table_id,a.left_player_id,c.username AS left_username,b.avatar AS left_avatar,a.right_player_id,e.username AS right_username,d.avatar AS right_avatar,a.game_state FROM game_table_info AS a LEFT join user_info AS b ON a.left_player_id=b.user_id LEFT JOIN  user AS c ON b.user_id=c.user_id LEFT JOIN user_info AS d ON a.right_player_id=d.user_id LEFT JOIN user AS e ON e.user_id=d.user_id WHERE a.table_id=%s",tableId)
        else:
            rowNumber=cursor.execute(
                "SELECT a.table_id,a.left_player_id,c.username AS left_username,b.avatar AS left_avatar,a.right_player_id,e.username AS right_username,d.avatar AS right_avatar,a.game_state FROM game_table_info AS a LEFT join user_info AS b ON a.left_player_id=b.user_id LEFT JOIN  user AS c ON b.user_id=c.user_id LEFT JOIN user_info AS d ON a.right_player_id=d.user_id LEFT JOIN user AS e ON e.user_id=d.user_id WHERE a.table_id=%s OR a.table_id=%s",(tableId,oldTableId))
        refreshData=[]
        for i in range(0, rowNumber):
            row = cursor.fetchone()
            temp = {"tableId": row["table_id"], "leftPlayerId": row["left_player_id"], "leftUsername": row["left_username"],
                    "leftAvatar": row["left_avatar"], "rightPlayerId": row["right_player_id"],
                    "rightUsername": row["right_username"], "rightAvatar": row["right_avatar"],
                    "gameState": row["game_state"]}
            refreshData.append(temp)
        for key in HomeSocketCash:
            HomeSocketCash[key].refreshGameTableList(refreshData)
        self.write("{'status':'00'}")
        logging.info("write {'status':'00'}")