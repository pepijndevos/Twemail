import conf
import oauth2 as oauth
from twisted.web.client import getPage
import cgi
import twisted.web.error
from urllib import quote
import json
from hashlib import md5
from urllib import urlencode
from email.header import decode_header
import shelve

db = shelve.open('twemaildb')

def parseEmail(email):
    """Get the Twitter name from a mail address like
    Pepijn de Vos <pepijndevos@twitter.com>"""
    return email.split('@')[0].split('<')[-1]

def unicodeHeader(header):
    return ' '.join(unicode(t, m or 'ascii') for t, m in decode_header(header))

def getXAuthTokens(username, password):
    consumer = oauth.Consumer(conf.xauth['key'], conf.xauth['secret'])

    request = oauth.Request.from_consumer_and_token(
        consumer=consumer,
        http_method='POST',
        http_url=conf.xauth['url'],
        parameters = {
            'x_auth_mode': 'client_auth',
            'x_auth_username': username,
            'x_auth_password': password
        }
    )
    request.sign_request(oauth.SignatureMethod_HMAC_SHA1(), consumer, None)

    d = getPage(conf.xauth['url'], method='POST', postdata=request.to_postdata())
    
    def parseTokens(postdata):
        params = cgi.parse_qs(postdata, keep_blank_values=False)
        return (params['oauth_token'][0], params['oauth_token_secret'][0], username)

    return d.addCallback(parseTokens)

def getOAuthHeader(key, secret, url, method, parameters={}):
    consumer = oauth.Consumer(conf.xauth['key'], conf.xauth['secret'])
    token = oauth.Token(key, secret)
    oauth_request = oauth.Request.from_consumer_and_token(consumer=consumer, token=token, http_method=method, http_url=url, parameters=parameters)
    oauth_request.sign_request(oauth.SignatureMethod_HMAC_SHA1(), consumer, token)
    return oauth_request.to_header()

def getTwitterTimeline(key, secret, last=None):
    method = "GET"
    url = conf.apiurl+'/statuses/home_timeline.json?count=200'
    if last:
        url += '&since_id='+str(last)
    headers = getOAuthHeader(key, secret, url, method)
    headers = dict((k, v.encode('utf-8')) for k, v in headers.iteritems())
    return getPage(url, method=method, headers=headers).addCallback(json.loads)

def updateTwitterTimeline(key, secret, **data):
    method = "POST"
    url = conf.apiurl+'/statuses/update.json'
    headers = getOAuthHeader(key, secret, url, method, data)
    headers.update({'Content-Type': "application/x-www-form-urlencoded"})
    return getPage(url, method=method, headers=headers, postdata=urlencode(data)).addCallback(json.loads)

def getUser(username, password):
    password = md5(conf.secret + password).hexdigest()
    if db[username]['password'] == password:
        return (db[username]['key'], db[username]['secret'], username)
    else:
        raise KeyError('Invalid password')

def addUser(username, password, key, secret):
    password = md5(conf.secret + password).hexdigest()
    db[username] = {'password': password,
                    'key': key,
                    'secret': secret,
                    'last': None}

def setLastTweet(username, twid):
    u = db[username]
    u['last'] = twid
    db[username] = u

def getLastTweet(username):
    return db[username]['last']
