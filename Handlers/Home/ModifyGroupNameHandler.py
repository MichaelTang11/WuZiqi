import logging
import tornado.web
import json
from Methods.ConnectDB import cursor

# TODO(Michael):上线时需要将注释部分取消
class ModifyGroupNameHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        # userId=self.get_secure_cookie("user_id").decode("utf-8")
        userId = '1'
        oldGroupName=self.get_argument("oldGroupName")
        newGroupName=self.get_argument("newGroupName")
        #更新分组信息
        cursor.execute("UPDATE group_info SET group_name=%s WHERE user_id=%s AND group_name=%s",(newGroupName,userId,oldGroupName))
        logging.info("用户ID:" + userId + "修改分组名:" + newGroupName + "成功！")
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', 'x-requested-with')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, PUT, DELETE')
        returnResult={"status":"00"}
        self.write(json.dumps(returnResult, ensure_ascii=False))


