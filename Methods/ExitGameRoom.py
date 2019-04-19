from GlobalValue.GlobalValue import HomeSocketCache, GameRoomSocketCache
from GlobalValue.GlobalValue import GameRoomCache
from Methods.ConnectDB import cursor
from Methods.RefreshRealtiveFriendList import refreshRelativeFriendList


def exitGameRoom(userId,tableId):
    cursor.execute("UPDATE game_table_info SET left_player_id=NULL,left_ready_state=0 WHERE table_id=%s AND left_player_id=%s",
                   (tableId, userId))
    cursor.execute("UPDATE game_table_info SET right_player_id=NULL,right_ready_state=0 WHERE table_id=%s AND right_player_id=%s",
                   (tableId, userId))
    # 获取gameState
    cursor.execute("SELECT * FROM game_table_info WHERE table_id=%s", tableId)
    row = cursor.fetchone()
    gameState = row["game_state"]
    # 获取anotherPlayerId
    anotherPlayerId = None
    if gameState == 1:
        for key in GameRoomCache[tableId]["playerState"].keys():
            if key != userId:
                anotherPlayerId = key
                break
    escapeFlag = False
    if gameState == 1:
        # 玩家逃离对局，进行相应数据库操作
        escapeFlag = True
        cursor.execute(
            "UPDATE game_table_info SET left_ready_state=0,right_ready_state=0,game_state=0 WHERE table_id=%s",
            tableId)
        cursor.execute(
            "UPDATE user_info SET win_time=win_time+1,game_time=game_time+1 WHERE user_id=%s",
            anotherPlayerId)
        cursor.execute(
            "UPDATE user_info SET game_time=game_time+1 WHERE user_id=%s",
            userId)
        GameRoomSocketCache[tableId][anotherPlayerId].escapeGame()
        # 刷新相关好友列表
        refreshRelativeFriendList([userId, anotherPlayerId])
    # 判断tableId是否存在于GameRoomCache中
    if tableId in GameRoomCache.keys():
        # 删除缓存中的对局信息
        del GameRoomCache[tableId]
    if not escapeFlag:
        if tableId in GameRoomSocketCache.keys():
            for key in GameRoomSocketCache[tableId].keys():
                GameRoomSocketCache[tableId][key].refreshGameRoom()
    rowNumber = cursor.execute(
        "SELECT a.table_id,a.left_player_id,c.username AS left_username,b.avatar AS left_avatar,a.right_player_id,e.username AS right_username,d.avatar AS right_avatar,a.game_state FROM game_table_info AS a LEFT join user_info AS b ON a.left_player_id=b.user_id LEFT JOIN  user AS c ON b.user_id=c.user_id LEFT JOIN user_info AS d ON a.right_player_id=d.user_id LEFT JOIN user AS e ON e.user_id=d.user_id WHERE a.table_id=%s",
        tableId)
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
    cursor.execute("UPDATE user SET `table_id`=NULL WHERE user_id=%s", userId)
