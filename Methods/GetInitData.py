#获取初始数据方法
from Methods.ConnectDB import cursor


def getInitData(user_id):
    returnData = {}
    userData = {}
    # 获取userData
    cursor.execute("SELECT * FROM user AS a LEFT JOIN user_info AS b ON a.user_id=b.user_id WHERE a.user_id=%s",
                   user_id)
    row = cursor.fetchone()
    userData["username"] = row["username"]
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
            "SELECT a.user_id,a.friend_id,d.avatar,c.username AS 'friend_username',a.note,c.login_state,c.state,a.group_id,b.group_name FROM friend_info AS a LEFT JOIN group_info AS b ON a.group_id = b.group_id LEFT JOIN user AS c ON a.friend_id = c.user_id LEFT JOIN user_info AS d on a.user_id=d.user_id WHERE a.user_id = %s AND b.group_name= %s ORDER BY c.login_state DESC,c.username ASC",
            (user_id, group_name))
        for j in range(0, row_number):
            temp = {}
            row = cursor.fetchone()
            temp["friendId"] = row["friend_id"]
            temp["avatar"] = row["avatar"]
            temp["friendUsername"] = row["friend_username"]
            temp["note"] = row["note"]
            temp["loginState"] = row["login_state"]
            temp["state"] = row["state"]
            groupListData.append(temp)
        friendInfo[group_name] = groupListData
    # friendInfo字典组装完毕
    returnData["userData"] = userData
    returnData["friendData"] = friendInfo
    returnData["gameTableData"] = ''
    returnData["infoData"] = ''
    returnData["messageData"] = ''
    return returnData