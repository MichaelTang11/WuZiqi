import logging
import tornado.web
from Methods.ConnectDB import cursor


class ChangeMessageWidgetStateHandler(tornado.web.RequestHandler):
    def post(self):
        userId = self.get_secure_cookie("userId")
        if userId is None:
            return
        userId=userId.decode("utf-8")
        widgetState = self.get_argument("widgetState")
        cursor.execute(
            "UPDATE user SET message_widget_state=%s WHERE user_id=%s;",
            (widgetState, userId))
        logging.info("用户:" + userId + "更新信息成功！")
