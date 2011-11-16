"""
A Twitter <-> E-mail proxy
"""

from twisted.application import internet
from twisted.application import service

from twisted.cred.portal import Portal
from twisted.internet.protocol import ServerFactory
from twisted.mail import pop3
from twisted.mail.protocols import ESMTPFactory
from twisted.mail.imap4 import LOGINCredentials, PLAINCredentials

from cred import checkers
from smtp.twitter import TwitterSmtpRealm
from pop3.twitter import TwitterPopRealm

import os

ch = checkers.CascadingChecker()
ch.registerChecker(checkers.DBChecker())
ch.registerChecker(checkers.TwitterChecker())

smtpPortal = Portal(TwitterSmtpRealm())
smtpPortal.registerChecker(ch)

popPortal = Portal(TwitterPopRealm())
popPortal.registerChecker(ch)

application = service.Application("Twemail")
challengers = {"LOGIN": LOGINCredentials, "PLAIN": PLAINCredentials}

f = ESMTPFactory(None, smtpPortal)
f.challengers = challengers
internet.TCPServer(os.environ["PORT_SMTP"], f).setServiceParent(application)

f = ServerFactory()
f.protocol = pop3.POP3
f.protocol.portal = popPortal
f.challengers = challengers
internet.TCPServer(os.environ["PORT_POP3"], f).setServiceParent(application)
