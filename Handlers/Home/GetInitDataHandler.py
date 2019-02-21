import json
import logging
import tornado.web
from Methods.GetInitData import getInitData


class GetInitDataHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        # 获取用户id
        # user_id = self.get_secure_cookie('user_id').decode("utf-8")
        user_id = "1"
        logging.info("获取用户ID:" + user_id)
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', 'x-requested-with')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, PUT, DELETE')
        self.write(json.dumps(getInitData(user_id), ensure_ascii=False))
