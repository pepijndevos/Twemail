# Twemail #

Twemail is a Twisted server that acts as a proxy between Twitter and your email application, by providing POP and SMTP implementations that interacts with Twitter.

Twemail allows you to read and write tweets using your mail client. It also supports replying and retweeting.

## Configuration ##

Twemail runs on Dotcloud at `twitteremail-pepijndevos.dotcloud.com` on port 18069 for POP3 and 18070 for SMTP.

Just add a new account to your email application with the email address `<your-twitter-username>@twitteremail-pepijndevos.dotcloud.com` and your twitter password.

Use password authentication with the above ports. Resort to your applications' documentation for how to do this.

## Usage ##

Basically you just read your email. Replying is replying, forwarding is retweeting, sending a message to `post@twitteremail-pepijndevos.dotcloud.com` posts a new tweet.

## Known deficiencies ##

**patches welcome**

* No SSL
* Forwarding/retweeting is a hack
* Seemingly never-ending unicode/HTML issues
* Uses Python's shelve