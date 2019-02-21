from Handlers.Home.AddFriendHandler import AddFriendHandler
from Handlers.Home.AddGroupHandler import AddGroupHandler
from Handlers.Home.AgreeAddFriendHandler import AgreeAddFriendHandler
from Handlers.Home.CheckLoginStatusHandler import CheckLoginStatusHandler
from Handlers.Home.DeleteFriendHandler import DeleteFriendHandler
from Handlers.Home.DeleteGroupHandler import DeleteGroupHandler
from Handlers.Home.DenyAddFriendHandler import DenyAddFriendHandler
from Handlers.Home.GetInitDataHandler import GetInitDataHandler
from Handlers.Home.HomeWebSocketHandler import HomeWebSocketHandler
from Handlers.Home.LogoutHandler import LogoutHandler
from Handlers.Home.ModifyGroupNameHandler import ModifyGroupNameHandler
from Handlers.Home.ModifyNoteHandler import ModifyNoteHandler
from Handlers.Home.ModifyUserAvatarHandler import ModifyUserAvatarHandler
from Handlers.Home.ModifyUserInfoHandler import ModifyUserInfoHandler
from Handlers.Home.MoveToGroupHandler import MoveToGroupHandler
from Handlers.Home.SitDownHandler import SitDownHandler
from Handlers.Login.CheckCodeHandler import CheckCodeHandler
from Handlers.Login.CheckUserHandler import CheckUserHandler
from Handlers.Login.LoginHandler import LoginHandler
from Handlers.Login.ResetPasswordHandler import ResetPasswordHandler
from Handlers.Login.SendCodeHandler import SendCodeHandler
from Handlers.Login.SignInHandler import SignInHandler
from Handlers.Main.MainHandler import MainHandler
from Handlers.Main.TestHandler import TestHandler
from Handlers.ProfilePage.GetUserProfileHandler import GetUserProfileHandler
from Handlers.SettingPage.GetUserInfoHandler import GetUserInfoHandler

url = {
    # 根目录跳转路由
    (r'/', MainHandler),
    # 登陆页面路由
    (r'/CheckLoginStatus', CheckLoginStatusHandler),
    (r'/Login', LoginHandler),
    (r'/SignIn', SignInHandler),
    (r'/CheckUser', CheckUserHandler),
    (r'/SendCode', SendCodeHandler),
    (r'/CheckCode', CheckCodeHandler),
    (r'/ResetPassword', ResetPasswordHandler),
    # 退出登录路由
    (r'/Logout', LogoutHandler),
    # home页面路由
    (r'/GetInitData', GetInitDataHandler),
    (r'/AddGroup', AddGroupHandler),
    (r'/MoveToGroup', MoveToGroupHandler),
    (r'/ModifyNote', ModifyNoteHandler),
    (r'/ModifyGroupName', ModifyGroupNameHandler),
    (r'/DeleteGroup', DeleteGroupHandler),
    (r'/ModifyUserInfo', ModifyUserInfoHandler),
    (r'/ModifyUserAvatar', ModifyUserAvatarHandler),
    (r'/AddFriend', AddFriendHandler),
    (r'/AgreeAddFriend', AgreeAddFriendHandler),
    (r'/DenyAddFriend', DenyAddFriendHandler),
    (r'/DeleteFriend', DeleteFriendHandler),
    (r'/HomeWebSocket', HomeWebSocketHandler),
    (r'/SitDown', SitDownHandler),
    # SettingPage页面路由
    (r'/GetUserInfo', GetUserInfoHandler),
    # ProfilePage页面路由
    (r'/GetUserProfile', GetUserProfileHandler),
    # 测试路由
    (r'/TestHandler', TestHandler)

}
