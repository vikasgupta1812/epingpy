"""
Global imports
"""

"""
Import for official python class
"""
from ConfigParser import ConfigParser

"""
Import for ePing.py specific classes
"""
from UrlChecker import UrlCheckerThread
from Logger import Logger

class ActionController:
    """
    ActionController is supposed to take a list with sites and check wether
    they're online or not. Based on the status it should then do nothing,
    log and error or notify the authorities by e-mail
    """
    logDict = {}
    
    def __init__(self):
        """
        Pass each url in the inputList to an UrlChecker object. If an error is
        encountered, put this in statusDict dictionary.
        """
        cfg = ConfigParser()
        logger = Logger()
        
        cfg.read('config.cfg')
        urls = cfg.items('urls')
        
        defaulttimeout = int(cfg.get('timeout', 'default', 0))
        
        threadList = []
        
        for name, url in urls:
            checker = UrlCheckerThread(url, name)
            threadList.append(checker)
            checker.start()

        for threads in threadList:
            threads.join()

        for x in threadList:
            status = x.status
            url = x.url
            name = x.name
            runtime = x.runtime
            
            """
            If there is an error, put information in a dict for furher
            processing. Else make sure this site gets removed from the
            Defconlist.
            """
            if(status != None and status != 200 or runtime >= defaulttimeout):
                self.logDict[name]= (name, url, status, runtime)
            else:
                logger.clearDefcon(name)

        if(len(self.logDict)>0):
            """
            If any errors are found, then logDict is bigger then one. Every
            error will be written down in the log, and mailed to specified
            addresses.
            """        
            logger.addLogDict(self.logDict)
            logger.checkDefcon()
        
