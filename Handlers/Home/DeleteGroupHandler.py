import logging
import tornado.web
import json
from Methods.ConnectDB import cursor
from Methods.GetInitData import getInitData

class DeleteGroupHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        # userId=self.get_secure_cookie("user_id").decode("utf-8")
        userId = '1'
        groupName=self.get_argument("groupName")
        #获取输入的组名的组id
        cursor.execute("SELECT group_id FROM group_info WHERE user_id=%s AND  group_name=%s",(userId,groupName))
        row=cursor.fetchone()
        groupId=row["group_id"]
        #删除组信息
        cursor.execute("DELETE FROM group_info WHERE group_id=%s",groupId)
        #获取默认分组的组ID
        cursor.execute("SELECT group_id FROM group_info WHERE user_id=%s AND  group_name='我的好友'",userId)
        row = cursor.fetchone()
        defaultGroupId = row["group_id"]
        #将删除组下的好友移动至默认分组
        cursor.execute("UPDATE friend_info SET group_id=%s WHERE user_id=%s AND group_id=%s", (defaultGroupId,userId,groupId))
        logging.info("用户ID:" + userId + "删除分组:" + groupName + "成功！")
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', 'x-requested-with')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, PUT, DELETE')
        self.write(json.dumps(getInitData(userId), ensure_ascii=False))


