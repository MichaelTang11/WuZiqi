import logging
import tornado.web
from Methods.ConnectDB import cursor
from GlobalValue.GlobalValue import HomeSocketCash


class AddFriendHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        userId=self.get_secure_cookie("user_id").decode("utf-8")
        username=self.get_argument("username")
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', 'x-requested-with')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, PUT, DELETE')
        rowNumber = cursor.execute("SELECT * FROM user WHERE username=%s", username)
        if rowNumber == 0:
            self.write("{'status':'01'}")
            logging.info("write {'status':'01'}")
        else:
            rowNumber = cursor.execute("SELECT * FROM friend_info AS a LEFT JOIN  user AS b ON a.friend_id=b.user_id WHERE a.user_id=%s AND b.username=%s",(userId, username))
            if rowNumber ==0:
                cursor.execute("SELECT * FROM user WHERE username=%s",username)
                row=cursor.fetchone()
                toId=row["user_id"]
                rowNumber = cursor.execute("SELECT * FROM game_notification WHERE from_id=%s AND to_id=%s", (userId,toId))
                rowNumber2 = cursor.execute("SELECT * FROM game_notification WHERE from_id=%s AND to_id=%s",
                                           (toId, userId))
                if rowNumber!=0 or rowNumber2!=0:
                    self.write("{'status':'03'}")
                    logging.info("write {'status':'03'}")
                    return 
                cursor.execute("INSERT INTO game_notification(`from_id`, `to_id`) VALUES (%s,%s)",(userId,toId))
                if toId in HomeSocketCash.keys():
                    HomeSocketCash[toId].refreshNotificationList()
                self.write("{'status':'00'}")
                logging.info("write {'status':'00'}")
            else:
                self.write("{'status':'02'}")
                logging.info("write {'status':'02'}")
