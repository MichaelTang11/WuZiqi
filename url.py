from Handlers.GameRoom.BegDrawHandler import BegDrawHandler
from Handlers.GameRoom.ExitGameRoomHandler import ExitGameRoomHandler
from Handlers.GameRoom.GameRoomWebSocketHandler import GameRoomWebSocketHandler
from Handlers.GameRoom.GetGameRoomDataHandler import GetGameRoomDataHandler
from Handlers.GameRoom.GiveUpHandler import GiveUpHandler
from Handlers.GameRoom.OnTimeDrawHandler import OnTimeDrawHandler
from Handlers.GameRoom.OverTimeHandler import OverTimeHandler
from Handlers.GameRoom.PutChessHandler import PutChessHandler
from Handlers.GameRoom.ReadyHandler import ReadyHandler
from Handlers.Home.ActiveMessageFriendListItemHandler import ActiveMessageFriendListItemHandler
from Handlers.Home.AddFriendHandler import AddFriendHandler
from Handlers.Home.AddGroupHandler import AddGroupHandler
from Handlers.Home.AgreeAddFriendHandler import AgreeAddFriendHandler
from Handlers.Home.ChangeMessageWidgetStateHandler import ChangeMessageWidgetStateHandler
from Handlers.Home.CheckLoginStatusHandler import CheckLoginStatusHandler
from Handlers.Home.DeleteFriendHandler import DeleteFriendHandler
from Handlers.Home.DeleteFriendListItemHandler import DeleteFriendListItemHandler
from Handlers.Home.DeleteGroupHandler import DeleteGroupHandler
from Handlers.Home.DenyAddFriendHandler import DenyAddFriendHandler
from Handlers.Home.GetInitDataHandler import GetInitDataHandler
from Handlers.Home.GetMessageListHandler import GetMessageListHandler
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
    (r'/GetMessageList', GetMessageListHandler),
    (r'/ActiveMessageFriendListItem', ActiveMessageFriendListItemHandler),
    (r'/DeleteFriendListItem', DeleteFriendListItemHandler),
    (r'/ChangeMessageWidgetState', ChangeMessageWidgetStateHandler),
    # SettingPage页面路由
    (r'/GetUserInfo', GetUserInfoHandler),
    # ProfilePage页面路由
    (r'/GetUserProfile', GetUserProfileHandler),
    # GameRoom页面路由
    (r'/GetGameRoomData', GetGameRoomDataHandler),
    (r'/GameRoomWebSocket', GameRoomWebSocketHandler),
    (r'/ExitGameRoom', ExitGameRoomHandler),
    (r'/Ready', ReadyHandler),
    (r'/PutChess', PutChessHandler),
    (r'/GiveUp', GiveUpHandler),
    (r'/BegDraw', BegDrawHandler),
    (r'/OverTime', OverTimeHandler),
    (r'/OnTimeDraw', OnTimeDrawHandler),
    # 测试路由
    (r'/Test', TestHandler)

}
