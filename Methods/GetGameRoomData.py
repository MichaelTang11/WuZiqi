# 获取游戏房间初始数据方法
from Methods.ConnectDB import cursor
from GlobalValue.GlobalValue import GameRoomCache


def getGameRoomData(tableId):
    gameRoomData = {}
    playerInfo = []
    sqlString = "SELECT\n" + \
                "	a.left_ready_state,\n" + \
                "	b.user_id AS left_user_id,\n" + \
                "	b.username AS left_username,\n" + \
                "	c.avatar AS left_avatar,\n" + \
                "	c.sex AS left_sex,\n" + \
                "	c.birthday AS left_birthday,\n" + \
                "	c.qq AS left_qq,\n" + \
                "	c.game_time AS left_game_time,\n" + \
                "	c.win_time AS left_win_time,\n" + \
                "	c.draw_time AS left_draw_time,\n" + \
                "	a.right_ready_state,\n" + \
                "	d.user_id AS right_user_id,\n" + \
                "	d.username AS right_username,\n" + \
                "	e.avatar AS right_avatar,\n" + \
                "	e.sex AS right_sex,\n" + \
                "	e.birthday AS right_birthday,\n" + \
                "	e.qq AS right_qq,\n" + \
                "	e.game_time AS right_game_time,\n" + \
                "	e.win_time AS right_win_time,\n" + \
                "	e.draw_time AS right_draw_time\n" + \
                "FROM\n" + \
                "	game_table_info AS a\n" + \
                "LEFT JOIN `user` AS b ON a.left_player_id = b.user_id\n" + \
                "LEFT JOIN user_info AS c ON b.user_id = c.user_id\n" + \
                "LEFT JOIN `user` AS d ON a.right_player_id = d.user_id\n" + \
                "LEFT JOIN user_info AS e ON d.user_id = e.user_id\n" + \
                "WHERE\n" + \
                "	a.table_id = %s"
    rowNumber = cursor.execute(sqlString, tableId)
    for i in range(0, rowNumber):
        row = cursor.fetchone()
        if row["left_user_id"]:
            temp = {"position": "left", "readyState": row["left_ready_state"], "userId": row["left_user_id"],
                    "username": row["left_username"],
                    "avatar": row["left_avatar"], "sex": row["left_sex"], "birthday": row["left_birthday"],
                    "qq": row["left_qq"], "gameTime": row["left_game_time"], "winTime": row["left_win_time"],
                    "drawTime": row["left_draw_time"]}
            playerInfo.append(temp)
        if row["right_user_id"]:
            temp = {"position": "right", "readyState": row["right_ready_state"], "userId": row["right_user_id"],
                    "username": row["right_username"],
                    "avatar": row["right_avatar"], "sex": row["right_sex"], "birthday": row["right_birthday"],
                    "qq": row["right_qq"], "gameTime": row["right_game_time"], "winTime": row["right_win_time"],
                    "drawTime": row["right_draw_time"]}
            playerInfo.append(temp)
    gameRoomData["playerInfo"] = playerInfo
    # 组装gameState数据
    cursor.execute("SELECT * FROM game_table_info WHERE table_id=%s", tableId)
    row = cursor.fetchone()
    gameRoomData["gameState"] = row["game_state"]
    if tableId in GameRoomCache.keys():
        gameRoomData["gameInfo"] = GameRoomCache[tableId]
    return gameRoomData
