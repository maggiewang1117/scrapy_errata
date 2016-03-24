import sys
import re
import urllib2
import urllib
import requests
import cookielib

reload(sys)
sys.setdefaultencoding("utf8")

loginurl = "https://errata.devel.redhat.com/package/show/ovirt-node"
logindomain = "redhat.com"

class Login(object):
    def __init__(self):
        self.name = ''
        self.password = ''
        self.domain = ''

        self.cj = cookielib.LWPCookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
        urllib2.install_opener(self.opener)

    def setLoginInfo(self, username, password, domain):
        self.name = username
        self.pwd = password
        self.domain = domain

    def login(self):
        loginparams = {'domain': self.domain, 'email': self.name, self.password}
        