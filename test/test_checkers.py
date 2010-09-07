from twisted.trial import unittest
from cred.checkers import CascadingChecker
from twisted.cred.credentials import UsernamePassword
from twisted.cred.checkers import InMemoryUsernamePasswordDatabaseDontUse
from twisted.cred.error import UnauthorizedLogin
from twisted.cred.credentials import IUsernameHashedPassword, IUsernamePassword

class CascadingTest(unittest.TestCase):
    
    def setUp(self):
        ch1 = InMemoryUsernamePasswordDatabaseDontUse()
        ch2 = InMemoryUsernamePasswordDatabaseDontUse()
        self.cach = CascadingChecker()
        
        ch1.addUser('foo', 'bar')
        ch1.addUser('boo', 'far')
        ch2.addUser('for', 'bao')
        
        self.cach.registerChecker(ch1)
        self.cach.registerChecker(ch2)
    
    def testInterfaces(self):
        self.assertEquals(self.cach.credentialInterfaces.difference((IUsernameHashedPassword, IUsernamePassword)), set())
    
    def testLoginFirstChecker(self):
        user = UsernamePassword('foo', 'bar')
        return self.cach.requestAvatarId(user)
    
    def testLoginSecondChecker(self):
        user = UsernamePassword('for', 'bao')
        return self.cach.requestAvatarId(user)
    
    def testLoginFail(self):
        user = UsernamePassword('steve', 'pswd')
        self.assertFailure(self.cach.requestAvatarId(user), UnauthorizedLogin)
