from zope.interface import implements
from twisted.mail import smtp
from twisted.internet import defer
import util
from twisted.cred.portal import IRealm
from email.parser import Parser
import re
from conf import domain

class TwitterSmtpRealm:
    implements(IRealm)

    def requestAvatar(self, avatarId, mind, *interfaces):
        if smtp.IMessageDelivery in interfaces:
            return smtp.IMessageDelivery, TwitterMessageDelivery(*avatarId), lambda: None
        else:
            raise NotImplementedError()

class TwitterMessageDelivery:
    implements(smtp.IMessageDelivery)

    def __init__(self, key, secret, username):
        self.key = key
        self.secret = secret
        self.username = username
    
    def receivedHeader(self, helo, origin, recipients):
        return "Received: TwitterMessageDelivery"
    
    def validateFrom(self, helo, origin):
        # All addresses are accepted
        return origin
    
    def validateTo(self, user):
        if user.dest.domain == domain:
            return lambda: TwitterMessage(self.key, self.secret, self.username)
        else:
            raise smtp.SMTPBadRcpt(user)

class TwitterMessage:
    implements(smtp.IMessage)
    
    def __init__(self, key, secret, username):
        self.key = key
        self.secret = secret
        self.username = username
        self.message = []
    
    def lineReceived(self, line):
        self.message.append(line)

    def eomReceived(self):
        msg = '\n'.join(self.message)
        headers = Parser().parsestr(msg)
        tweet = util.unicodeHeader(headers['subject'])
        tweet = tweet.encode('utf-8')
        if headers['in-reply-to']:
            tweet = '@' + util.parseEmail(util.unicodeHeader(headers['to'])) + ' ' + tweet
            return util.updateTwitterTimeline(
                self.key,
                self.secret,
                status=tweet,
                in_reply_to_status_id=util.parseEmail(headers['in-reply-to']))
        elif 'fwd:' in headers['subject'].lower():
            # do_ugly_rt(easter_egg, good_feeling, raw_input('Enter some magic: '))
            tweet = re.sub(r'^\[?(.*)[Ff]wd: (.*?)\]?$', '\\1RT @{0} \\2', tweet).format(util.parseEmail(util.unicodeHeader(headers['to'])))

        return util.updateTwitterTimeline(
            self.key,
            self.secret,
            status=tweet)
    
    def connectionLost(self):
        pass
