#获取初始数据方法
from Methods.ConnectDB import cursor


def getInitData(user_id):
    returnData = {}
    userData = {}
    notificationData=[]
    gameTableData=[]
    # 获取userData
    cursor.execute("SELECT * FROM user AS a LEFT JOIN user_info AS b ON a.user_id=b.user_id WHERE a.user_id=%s",
                   user_id)
    row = cursor.fetchone()
    userData["username"] = row["username"]
    userData["avatar"]=row["avatar"]
    userData["ifFirstLogin"] = row["if_first_login"]

    # 从group_info表中获取此用户id下所有的用户分组存入groupNameList
    row_number = cursor.execute("select * from group_info where user_id=%s ORDER BY group_id", user_id)
    friendInfo = {}
    groupNameList = []
    for i in range(0, row_number):
        row = cursor.fetchone()
        groupNameList.append(row["group_name"])

    # 根据groupNameList和用户ID查询好友的信息，并组成friendInfo字典
    for i in range(0, len(groupNameList)):
        groupListData = []
        group_name = groupNameList[i]
        row_number = cursor.execute(
            "SELECT a.user_id,a.friend_id,d.avatar,c.username AS 'friend_username',a.note,c.login_state,c.state,a.group_id,b.group_name FROM friend_info AS a LEFT JOIN group_info AS b ON a.group_id = b.group_id LEFT JOIN user AS c ON a.friend_id = c.user_id LEFT JOIN user_info AS d on a.friend_id=d.user_id WHERE a.user_id = %s AND b.group_name= %s ORDER BY c.login_state DESC,c.username ASC",
            (user_id, group_name))
        for j in range(0, row_number):
            row = cursor.fetchone()
            temp = {"friendId": row["friend_id"], "avatar": row["avatar"], "friendUsername": row["friend_username"],
                    "note": row["note"], "loginState": row["login_state"], "state": row["state"]}
            groupListData.append(temp)
        friendInfo[group_name] = groupListData
    # friendInfo字典组装完毕
    #根据user_id获取notification
    row_number = cursor.execute("SELECT a.from_id,b.username AS from_username,a.to_id,c.username AS to_username FROM game_notification AS a LEFT JOIN user AS b ON a.from_id = b.user_id LEFT JOIN user AS c ON a.to_id=c.user_id WHERE to_id=%s ORDER BY id", user_id)
    for i in range(0, row_number):
        row = cursor.fetchone()
        temp= {"fromId": row["from_id"], "fromUsername": row["from_username"], "toId": row["to_id"],
               "toUsername": row["to_username"]}
        notificationData.append(temp)

    #组装gameTableData
    row_number=cursor.execute("SELECT a.table_id,a.left_player_id,c.username AS left_username,b.avatar AS left_avatar,a.right_player_id,e.username AS right_username,d.avatar AS right_avatar,a.game_state FROM game_table_info AS a LEFT join user_info AS b ON a.left_player_id=b.user_id LEFT JOIN  user AS c ON b.user_id=c.user_id LEFT JOIN user_info AS d ON a.right_player_id=d.user_id LEFT JOIN user AS e ON e.user_id=d.user_id ORDER BY a.table_id ")
    for i in range(0, row_number):
        row = cursor.fetchone()
        temp= {"tableId": row["table_id"], "leftPlayerId": row["left_player_id"], "leftUsername": row["left_username"],
               "leftAvatar": row["left_avatar"], "rightPlayerId": row["right_player_id"],
               "rightUsername": row["right_username"], "rightAvatar": row["right_avatar"],
               "gameState": row["game_state"]}
        gameTableData.append(temp)

    #组装messageData
    messageData={}
    messageFriendList=[]
    rowNumber=cursor.execute("SELECT a.user_id,a.friend_id,b.username,c.avatar FROM message_friend_list AS a LEFT JOIN user AS b ON a.friend_id=b.user_id LEFT JOIN user_info AS c ON b.user_id=c.user_id WHERE a.user_id=%s ORDER BY id",user_id)
    for i in range(0, rowNumber):
        row = cursor.fetchone()
        temp= {"friendId": row["friend_id"], "username": row["username"], "avatar": row["avatar"]}
        messageFriendList.append(temp)
    messageData["messageFriendList"]=messageFriendList

    returnData["userData"] = userData
    returnData["friendData"] = friendInfo
    returnData["gameTableData"] = gameTableData
    returnData["notificationData"] = notificationData
    returnData["messageData"] = messageData
    return returnData