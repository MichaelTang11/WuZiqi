import logging
import tornado.web
import json
from Methods.ConnectDB import cursor
from Methods.GetInitData import getInitData

#TODO(Michael)上线时删除注释
class ModifyNoteHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        # userId=self.get_secure_cookie("user_id").decode("utf-8")
        userId='1'
        friendId=self.get_argument("friendId")
        note=self.get_argument("note")
        cursor.execute("UPDATE friend_info SET note=%s WHERE  user_id=%s AND  friend_id=%s",(note,userId,friendId))
        logging.info("用户ID:" + userId + "修改好友ID:" + friendId + "备注:" + note + "成功！")
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', 'x-requested-with')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, PUT, DELETE')
        self.write(json.dumps(getInitData(userId), ensure_ascii=False))
