from Handlers.Home.AddGroupHandler import AddGroupHandler
from Handlers.Home.CheckLoginStatusHandler import CheckLoginStatusHandler
from Handlers.Home.GetInitDataHandler import GetInitDataHandler
from Handlers.Login.CheckCodeHandler import CheckCodeHandler
from Handlers.Login.CheckUserHandler import CheckUserHandler
from Handlers.Login.LoginHandler import LoginHandler
from Handlers.Login.ResetPasswordHandler import ResetPasswordHandler
from Handlers.Login.SendCodeHandler import SendCodeHandler
from Handlers.Login.SignInHandler import SignInHandler
from Handlers.Main.MainHandler import MainHandler
from Handlers.Main.TestHandler import TestHandler

url = {
    (r'/',MainHandler),
    (r'/CheckLoginStatus', CheckLoginStatusHandler),
    (r'/Login', LoginHandler),
    (r'/SignIn', SignInHandler),
    (r'/CheckUser', CheckUserHandler),
    (r'/SendCode', SendCodeHandler),
    (r'/CheckCode', CheckCodeHandler),
    (r'/ResetPassword', ResetPasswordHandler),
    (r'/GetInitData', GetInitDataHandler),
    (r'/AddGroup', AddGroupHandler),
    (r'/TestHandler', TestHandler)

}
