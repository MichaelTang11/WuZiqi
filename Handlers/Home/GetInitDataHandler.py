import json
import logging
import tornado.web
from Methods.GetInitData import getInitData


class GetInitDataHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        # 获取用户id
        userId = self.get_secure_cookie('userId')
        if userId is None:
            return
        userId=userId.decode("utf-8")
        logging.info("获取用户ID:" + userId)
        self.write(json.dumps(getInitData(userId), ensure_ascii=False))
