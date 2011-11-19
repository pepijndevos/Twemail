from twisted.mail.pop3 import IMailbox
from zope.interface import implements
from twisted.internet import defer
from StringIO import StringIO
import oauth2 as oauth
from twisted.cred.portal import IRealm
import util
from twisted.internet.defer import inlineCallbacks, returnValue
from twittermessage import TwitterTemplate

class TwitterPopRealm:
    implements(IRealm)

    def requestAvatar(self, avatarId, mind, *interfaces):
        if IMailbox in interfaces:
            return IMailbox, TwitterMailbox(*avatarId), lambda: None
        else:
            raise NotImplementedError()

class TwitterMailbox:
    implements(IMailbox)
    
    def __init__(self, key, secret, username):
        self.key = key
        self.secret = secret
        self.username = username
        self.messages = []
        self.last = None
    
    @inlineCallbacks
    def listMessages(self, index=None):
        if not self.last:
            try:
                self.last = yield util.getLastTweet(self.username)
            except IndexError:
                pass
            
        if not self.messages:
            timeline = yield util.getTwitterTimeline(self.key, self.secret, self.last)
            returnValue(self.addMessages(timeline, index))
        elif index == None:
            returnValue([len(m[1]) for m in self.messages])
        else:
            returnValue(len(self.messages[index][1]))
            
    def addMessages(self, messages, index):
        def proccess(message):
            proccessed = TwitterTemplate(message, self.username).as_string()
            self.messages.append((message, proccessed))
            return len(proccessed)
        
        mlist = map(proccess, messages)
        if index == None: # 0 == False
            return mlist
        else:
            return mlist[index]
        
    def getMessage(self, index):
        twid = self.getUidl(index)
        if max(self.last, twid) == twid:
            self.last = twid
            util.setLastTweet(self.username, twid)
        
        return StringIO(self.messages[index][1])

    def getUidl(self, index):
        return self.messages[index][0]['id']

    def deleteMessage(self, index):
        pass

    def undeleteMessages(self):
        pass

    def sync(self):
        pass

