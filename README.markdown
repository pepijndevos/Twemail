= Twemail =

Twemail is a Twisted server that acts as a proxy between Twitter and your email application, by providing POP and SMTP implementations that interact with Twitter.

Twemail allows you to read and write tweets using your mail client. It also supports replying and retweeting.

== Installation ==

Twemail requires Twisted, Twitter-Text-Python and OAuth2 to be installed. You might try to use the setup.py for getting them.

Run Twemail:

    twistd -ny twemail.tac
