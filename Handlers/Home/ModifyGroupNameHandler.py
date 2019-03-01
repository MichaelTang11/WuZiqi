import logging
import tornado.web
import json
from Methods.ConnectDB import cursor


class ModifyGroupNameHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        userId = self.get_secure_cookie("userId").decode("utf-8")
        oldGroupName = self.get_argument("oldGroupName")
        newGroupName = self.get_argument("newGroupName")
        # 更新分组信息
        cursor.execute("UPDATE group_info SET group_name=%s WHERE user_id=%s AND group_name=%s",
                       (newGroupName, userId, oldGroupName))
        logging.info("用户ID:" + userId + "修改分组名:" + newGroupName + "成功！")
        returnResult = {"status": "00"}
        self.write(json.dumps(returnResult, ensure_ascii=False))
