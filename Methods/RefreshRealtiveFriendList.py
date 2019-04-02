from GlobalValue.GlobalValue import HomeSocketCache
from Methods.ConnectDB import cursor

def refreshRelativeFriendList(userList):
    for i in range(0,len(userList)):
        rowNumber = cursor.execute(
            "SELECT * FROM friend_info AS a LEFT JOIN `user` AS b ON a.friend_id=b.user_id WHERE a.user_id=%s and b.login_state=1",
            userList[i])
        for j in range(0, rowNumber):
            row = cursor.fetchone()
            HomeSocketCache[str(row["friend_id"])].refreshFriendList()