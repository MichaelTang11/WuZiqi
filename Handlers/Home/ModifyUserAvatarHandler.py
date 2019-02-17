import logging
import tornado.web
from Methods.ConnectDB import cursor
import re

# TODO(Michael)上线时删除注释,更改保存路径
class ModifyUserAvatarHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        userId=self.get_secure_cookie("user_id").decode("utf-8")
        images=self.request.files.get('avatar',None)
        for image in images:
            searchObj =re.search('\.\S*',image['filename'])
            fileType=searchObj.group()
            savePath='/webRoot/wuziqi/assets/images/avatars/user'+userId+fileType
            with open(savePath,'wb') as f:
                f.write(image['body'])
            cursor.execute("UPDATE user_info SET avatar=%s WHERE user_id=%s",('assets/images/avatars/user'+userId+fileType,userId))
        logging.info("用户:" + userId + "头像更新成功！")
