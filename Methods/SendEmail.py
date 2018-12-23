from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

import smtplib


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def Send(code, address, username):
    from_addr = "1091149562@qq.com"
    password = 'dijjryaijyusicjj'
    to_addr = address
    msg = MIMEText('验证码为：' + code, 'plain', 'utf-8')
    msg['From'] = _format_addr('五子棋游戏系统 <%s>' % from_addr)
    msg['To'] = _format_addr('用户 :' + username + '<%s>' % to_addr)
    msg['Subject'] = Header('重置密码验证码', 'utf-8').encode()
    server = smtplib.SMTP_SSL("smtp.qq.com", 465)
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()
