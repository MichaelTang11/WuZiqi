#测试用handler
import tornado.web
from Methods.ConnectDB import cursor


class TestHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        userId="3"
        friendId="1"
        cursor.execute("INSERT INTO message_friend_list (user_id, friend_id) values(%s,%s)", (userId, friendId))