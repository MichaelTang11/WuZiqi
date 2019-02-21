import logging
import tornado.web
from GlobalValue.GlobalValue import CodeCash


class CheckCodeHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        # 获取传入参数
        username = self.get_argument("username")
        code = self.get_argument("code")
        # 与CodeCash中的数据进行比对
        if code == CodeCash[username]:
            # 比对成功后清除内容释放内存
            logging.info("用户:" + username + "验证码校验成功！")
            logging.info("清除用户:" + username + " 验证码：" + CodeCash.pop(username))
            self.write({"status": "00"})
        else:
            logging.info("用户:" + username + "验证码校验失败！")
            self.write({"status": "01"})
