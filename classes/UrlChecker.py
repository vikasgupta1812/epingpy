"""
Global imports
"""
import socket

"""
Import for official python class
"""
from threading import Thread, Lock
from urllib2 import Request, urlopen
from ConfigParser import ConfigParser

"""
Import for ePing.py specific classes
"""
from TimeoutController import TimeoutController
from classes.StopWatch import StopWatch

class UrlCheckerThread(Thread):
    """
    UrlChecker checks the status of the HTTP Status header. In case of timeout
    or error we can alert somebody. Because this class is threaded, all url's
    can be checked in parallel, not causing a long ait if several sites
    experience a timeout.
    """
    lock = Lock()
    threadId = 0
    
    def __init__(self, url, name):
        Thread.__init__(self)
        self.url = url
        self.name = name
        self.cfg = ConfigParser()
        self.cfg.read('config.cfg')
        self.thisId = UrlCheckerThread.threadId
        self.extendedTimeout = int(self.cfg.get('timeout', 'extended', 0))
        self.tc = TimeoutController()
        self.tc.setTimeout(self.extendedTimeout)
        UrlCheckerThread.threadId += 1

    def run(self):
        """
        getHeader uses urlopen to check wether an website is online or not
        """
        self.sw = StopWatch()
        self.sw.start()
        self.checker = UrlChecker()
        UrlCheckerThread.lock.acquire()
        self.status = self.checker.getStatus(self.url)
        self.sw.stop()
        self.runtime = self.sw.time()
        """
        if(isinstance(self.status, socket.timeout)):
            self.tc.setTimeout(self.extendedTimeout)
            self.status = self.checker.getStatus(self.url)
            if(self.status == 200):
                self.status = 'short time out'
            self.tc.setTimeout(self.defaultTimeout)
        """
        UrlCheckerThread.lock.release()

class UrlChecker:
    """
    UrlChecker retrieves the specified URL's and returns an error if found
    """
    def getStatus(self, url):
        """
        getHeader uses urlopen to check wether an website is online or not
        """
        request = Request(url, None)
        try:
            urlReq = urlopen(request)

            """
            getcode() return the HTTP status header, which should be 200
            in most cases.
            """
            return urlReq.getcode()
        except IOError, e:
            if hasattr(e, 'reason'):
                """
                e.reason returns an IOError object, which cannot be just
                inserted in the database. The IOError object is basically
                a 2-Tuple with an errornumber and an errorstring.
                Since an errornumber is less readable then a string,
                we use e.reason.strerror to just return IOError's string
                """
                return e.reason.strerror
            elif hasattr(e, 'code'):
                """
                e.code is an int object, which is perfectly fine to insert in
                the database. So no further modification needed.
                """
                return e.code
    
