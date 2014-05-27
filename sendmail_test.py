#!/usr/bin/env python
# mailer test


from scrapy.mail import MailSender

conf = {
    "smtphost" : "smtp.qq.com",
    "mailfrom" : "1124011778@qq.com",
    "smtpuser" : "1124011778@qq.com",
    "smtppass" : "33135331.",
    "smtpport" : 25,
    "smtpssl" : True
}

to = ["cjinle@gmail.com", "a@lok.me"]

send_conf = {
    "to" : to,
    "subject" : "scrapy subject",
    "body": "scrapy mail test content"
}

print send_conf

mailer = MailSender(**conf)
#mailer = MailSender.from_settings(**conf)

flg = mailer.send(**send_conf)

print flg
