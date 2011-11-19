from twisted.cred.checkers import ICredentialsChecker
from twisted.cred import error, credentials
from twisted.internet.defer import maybeDeferred
from collections import deque

import util

from zope.interface import implements

def fail(err):
    raise error.UnauthorizedLogin(err)

class TwitterChecker:
    """
    Checks credentials with Twitter using XAuth
    """

    implements(ICredentialsChecker)
    credentialInterfaces = (credentials.IUsernamePassword,)

    def requestAvatarId(self, credentials):
        d = util.getXAuthTokens(credentials.username, credentials.password)
        
        def add(t):
            util.addUser(credentials.username, credentials.password, t[0], t[1])
            return t
        
        return d.addCallbacks(add, fail)

class DBChecker:
    """
    Checks credentials with the database
    """

    implements(ICredentialsChecker)
    credentialInterfaces = (credentials.IUsernamePassword,)

    def requestAvatarId(self, credentials):
        return util.getUser(credentials.username, credentials.password)

class CascadingChecker:
    """
    Check multiple checkers untill one succeeds.
    Else raise UnauthorizedLogin.
    """

    implements(ICredentialsChecker)
    credentialInterfaces = set()
    
    def __init__(self):
        self.checkers = []
        self.checked = []
    
    def registerChecker(self, checker):
        self.checkers.append(checker)
        self.credentialInterfaces.update(checker.credentialInterfaces)
    
    def _requestAvatarId(self, err, queue, credentials):
        try:
            ch = queue.popleft()
        except IndexError:
            raise error.UnauthorizedLogin()
        
        d = maybeDeferred(ch.requestAvatarId, credentials)
        return d.addErrback(self._requestAvatarId, queue, credentials)
    
    requestAvatarId = lambda self, credentials: self._requestAvatarId(None, deque(self.checkers), credentials)
