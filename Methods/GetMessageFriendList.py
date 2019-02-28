# 获取指定消息框好友列表方法
from Methods.ConnectDB import cursor


def getMessageFriendList(userId):
    messageFriendList = []
    rowNumber = cursor.execute(
        "SELECT a.user_id,a.friend_id,b.username,c.avatar,a.message_number,a.active_state FROM message_friend_list AS a LEFT JOIN user AS b ON a.friend_id=b.user_id LEFT JOIN user_info AS c ON b.user_id=c.user_id WHERE a.user_id=%s ORDER BY id",
        userId)
    for i in range(0, rowNumber):
        row = cursor.fetchone()
        temp = {"friendId": row["friend_id"], "username": row["username"], "avatar": row["avatar"],
                "messageNumber": row["message_number"], "activeState": row["active_state"]}
        messageFriendList.append(temp)
    return messageFriendList
