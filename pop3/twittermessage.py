from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from ttp import Parser
import codecs

class TwitterTemplate(MIMEMultipart):
    def __init__(self, tweet, to):
        MIMEMultipart.__init__(self, 'alternative', _charset='utf-8')
        
        tweet['html_text'] = Parser().parse(tweet['text']).html
        
        self['Subject'] = Header(tweet['text'].encode('utf-8'), 'utf-8')
        f = Header(tweet['user']['name'].encode('utf-8'), 'utf-8')
        f.append('<{0}@twitter.com>'.format(tweet['user']['screen_name']), 'ascii')
        self['From'] = f
        self['To'] = to+'@twitter.com'
        self['Date'] = tweet['created_at']
        self['Message-ID'] = "<{0}@twitter.com>".format(tweet['id'])
        
        self.attach(MIMEText(tweet['text'].encode('utf-8'), 'plain', _charset='utf-8'))
        
        with codecs.open('mail.html', 'r', 'utf-8') as f:
            template = f.read()
            template = template.format(**tweet)
            template = template.encode('utf-8')
            self.attach(MIMEText(template, 'html', _charset='utf-8'))

