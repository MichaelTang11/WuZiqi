# 初始化对局
from Methods.ConnectDB import cursor
from GlobalValue.GlobalValue import HomeSocketCache
from GlobalValue.GlobalValue import GameRoomSocketCache
from GlobalValue.GlobalValue import GameRoomCache
from Methods.RefreshRealtiveFriendList import refreshRelativeFriendList


def initGame(tableId):
    # 将数据库中gameState设置为1
    cursor.execute("UPDATE game_table_info SET game_state=1 WHERE table_id=%s", tableId)
    # 获取此桌的玩家id
    cursor.execute("SELECT * FROM game_table_info WHERE table_id=%s", tableId)
    row = cursor.fetchone()
    leftUserId = str(row["left_player_id"])
    rightUserId = str(row["right_player_id"])
    #将两个玩家的state改为2游戏中
    cursor.execute("UPDATE user SET state=2 WHERE user_id=%s OR user_id=%s", (leftUserId,rightUserId))
    # 刷新相关好友列表
    refreshRelativeFriendList([leftUserId,rightUserId])
    # 准备刷新数据
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
    # 通知在线用户前端刷新数据
    for key in HomeSocketCache:
        HomeSocketCache[key].refreshGameTableList(refreshData)

    # 初始化pointState数组
    pointState = []
    for i in range(0, 15):
        temp = []
        for j in range(0, 15):
            temp.append(0)
        pointState.append(temp)

    # 初始化GameRoomCache
    if tableId in GameRoomCache.keys():
        if GameRoomCache[tableId]["totalGameTime"] % 2 == 0:
            GameRoomCache[tableId]["playerState"][leftUserId]["chessType"] = "black"
            GameRoomCache[tableId]["playerState"][leftUserId]["myTurn"] = True
            GameRoomCache[tableId]["playerState"][rightUserId]["chessType"] = "white"
            GameRoomCache[tableId]["playerState"][rightUserId]["myTurn"] = False
            GameRoomCache[tableId]["stepRecord"] = []
            GameRoomCache[tableId]["pointState"] = pointState
        else:
            GameRoomCache[tableId]["playerState"][leftUserId]["chessType"] = "white"
            GameRoomCache[tableId]["playerState"][leftUserId]["myTurn"] = False
            GameRoomCache[tableId]["playerState"][rightUserId]["chessType"] = "black"
            GameRoomCache[tableId]["playerState"][rightUserId]["myTurn"] = True
            GameRoomCache[tableId]["stepRecord"] = []
            GameRoomCache[tableId]["pointState"] = pointState
    else:
        GameRoomCache[tableId] = {"gameTime": "",
                                  "totalGameTime": 0,
                                  "playerState": {
                                      leftUserId: {"chessType": "black",
                                                   "winTime": 0,
                                                   "chessTime": "",
                                                   "myTurn": True},
                                      rightUserId: {"chessType": "white",
                                                    "winTime": 0,
                                                    "chessTime": "",
                                                    "myTurn": False}
                                  },
                                  "stepRecord": [],
                                  "pointState": pointState
                                  }
    # 通知前端对局开始
    GameRoomSocketCache[tableId][leftUserId].gameStart()
    GameRoomSocketCache[tableId][rightUserId].gameStart()
