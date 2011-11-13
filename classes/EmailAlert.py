"""
Global imports
"""
import time
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from ConfigParser import ConfigParser

class EmailAlert:
    """
    EmailAlert creates an e-mail with the error status on the failing websites.
    """

    msg = MIMEMultipart('alternative')
    text = ''
    html = ''
    
    def __init__(self):
        """
        Use config-file to get all the settings to send email.
        """
        cfg = ConfigParser()
        cfg.read('config.cfg')
        self.fromAddress = cfg.get('email', 'from', 0)
        self.subject = cfg.get('email', 'subject', 0)
        self.to = cfg.get('email', 'to', 0)
        self.smtp = cfg.get('email', 'smtp', 0)

    def sendMail(self, statusDict):
        """
        Use the statusDict to create an email in both text and html stating
        which sites have what error.
        """
        self.msg['Subject'] = self.subject
        self.msg['From'] = self.fromAddress
        timestamp = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())

        self.text = 'Your e-mail client supports no HTML, this is plaintext\n'
        for name, (name, url, status, runtime, timestamp)\
            in statusDict.iteritems():
            self.text = self.text + 'On '
            self.text = self.text + timestamp
            self.text = self.text + url + ' had errorstatus: '
            self.text = self.text + "%s, and ran for %s seconds.\n" %\
                        (status, runtime)           
                        
        self.html = '<html><head></head><body>'
        self.html = self.html + 'On ' + time.strftime("%Y/%m/%d %H:%M:%S",\
                                                  time.localtime()) +\
                ' the following websites had problems:<br /><br />'
        for name, (name, url, status, runtime, timestamp)\
            in statusDict.iteritems():
            self.html = self.html + '<a href="' + url +\
                        '">' + url + '</a>. Errorstatus:<b> '
            self.html = self.html + "%s" % (status)
            self.html = self.html + '</b>. Time: <b>%s seconds</b><br />'%\
                        (runtime)
        self.html = self.html + '</body></html>'

        self.msg['To'] = self.to
        
        part1 = MIMEText(self.text, 'plain')
        part2 = MIMEText(self.html, 'html')

        self.msg.attach(part1)
        self.msg.attach(part2)

        s = smtplib.SMTP(self.smtp)
        s.sendmail(self.fromAddress, self.to, self.msg.as_string())
        s.close()
