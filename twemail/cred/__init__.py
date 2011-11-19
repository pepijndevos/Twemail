from twisted.cred.portal import IRealm
from twisted.mail import smtp, pop3
from smtp.twitter import TwitterMessageDelivery
from pop3.twitter import TwitterMailbox
from zope.interface import implements

class TwitterSmtpRealm:
    implements(IRealm)

    def requestAvatar(self, avatarId, mind, *interfaces):
        if smtp.IMessageDelivery in interfaces:
            return smtp.IMessageDelivery, TwitterMessageDelivery(*avatarId), lambda: None
        else:
            raise NotImplementedError()

class TwitterPopRealm:
    implements(IRealm)

    def requestAvatar(self, avatarId, mind, *interfaces):
        if pop3.IMailbox in interfaces:
            return pop3.IMailbox, TwitterMailbox(*avatarId), lambda: None
        else:
            raise NotImplementedError()
