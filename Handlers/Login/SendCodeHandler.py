import random
from Methods import SendEmail
from GlobalValue.GlobalValue import CodeCash
from Methods.ConnectDB import cursor
import logging
import tornado.web

class SendCodeHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        username = self.get_argument("username")
        randomString = ""
        for i in range(0, 4):
            randomString = randomString + str(random.randint(1, 9))
        cursor.execute("select * from user WHERE username=%s", username)
        row = cursor.fetchone()
        address = row["email"]
        # 将验证码以 用户名：验证码 的形式写入CodeCash
        CodeCash[username] = randomString
        SendEmail.Send(randomString, address, username)
        logging.info("用户:" + username + "发送验证码！")
        self.write({"status": "00"})