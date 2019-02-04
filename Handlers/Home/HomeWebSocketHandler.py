import tornado.websocket
import logging
from GlobalValue.GlobalValue import HomeSocketCash

class HomeWebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self, *args, **kwargs):
        # userId=self.get_secure_cookie("user_id").decode("utf-8")
        userId = "1"
        HomeSocketCash[userId]=self

    def on_message(self, message):
        logging.info(message)
        # self.write_message("receieved your message!")

    def on_close(self):
        # userId=self.get_secure_cookie("user_id").decode("utf-8")
        userId = "1"
        del HomeSocketCash[userId]

    def check_origin(self, origin):
        return True