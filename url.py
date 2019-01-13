from Handlers.Home.AddGroupHandler import AddGroupHandler
from Handlers.Home.CheckLoginStatusHandler import CheckLoginStatusHandler
from Handlers.Home.DeleteGroupHandler import DeleteGroupHandler
from Handlers.Home.GetInitDataHandler import GetInitDataHandler
from Handlers.Home.ModifyNoteHandler import ModifyNoteHandler
from Handlers.Home.ModifyUserInfoHandler import ModifyUserInfoHandler
from Handlers.Home.MoveToGroupHandler import MoveToGroupHandler
from Handlers.Login.CheckCodeHandler import CheckCodeHandler
from Handlers.Login.CheckUserHandler import CheckUserHandler
from Handlers.Login.LoginHandler import LoginHandler
from Handlers.Login.ResetPasswordHandler import ResetPasswordHandler
from Handlers.Login.SendCodeHandler import SendCodeHandler
from Handlers.Login.SignInHandler import SignInHandler
from Handlers.Main.MainHandler import MainHandler
from Handlers.Main.TestHandler import TestHandler
from Handlers.SettingPage.GetUserInfoHandler import GetUserInfoHandler

url = {
    #根目录跳转路由
    (r'/',MainHandler),
    #登陆页面路由
    (r'/CheckLoginStatus', CheckLoginStatusHandler),
    (r'/Login', LoginHandler),
    (r'/SignIn', SignInHandler),
    (r'/CheckUser', CheckUserHandler),
    (r'/SendCode', SendCodeHandler),
    (r'/CheckCode', CheckCodeHandler),
    (r'/ResetPassword', ResetPasswordHandler),
    #home页面路由
    (r'/GetInitData', GetInitDataHandler),
    (r'/AddGroup', AddGroupHandler),
    (r'/MoveToGroup', MoveToGroupHandler),
    (r'/ModifyNote', ModifyNoteHandler),
    (r'/DeleteGroup', DeleteGroupHandler),
    (r'/ModifyUserInfo', ModifyUserInfoHandler),
    #SettingPage页面路由
    (r'/GetUserInfo', GetUserInfoHandler),
    #测试路由
    (r'/TestHandler', TestHandler)

}
