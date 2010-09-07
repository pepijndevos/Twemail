= Twemail =

Twemail is a Twisted server that acts as a proxy between Twitter and your email application, by providing POP and SMTP implementations that interact with Twitter.

Twemail allows you to read and write tweets using your mail client. It also supports replying and retweeting.

== Installation ==

Twemail requires Twisted and OAuth2 to be installed. The Python lib for processing tweets is also needed, but is bundled for some weird reason. I'll add a setup.py later to deal with this stuff.

Run Twemail:

    twistd -ny twemail.tac
