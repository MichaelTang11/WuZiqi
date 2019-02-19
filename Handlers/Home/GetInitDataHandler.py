import json
import logging
import tornado.web
from Methods.GetInitData import getInitData

class GetInitDataHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        #获取用户id
        user_id = self.get_secure_cookie('user_id').decode("utf-8")
        logging.info("获取用户ID:" + user_id)
        self.write(json.dumps(getInitData(user_id),ensure_ascii=False))