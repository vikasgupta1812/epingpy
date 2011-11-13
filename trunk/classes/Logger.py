"""
Global imports
"""
import logging
import time

"""
Import for ePing.py specific classes
"""
from classes.DatabaseController import DatabaseController
from classes.EmailAlert import EmailAlert

class Logger:
    """
    Logger is to decide how to add status of websites
    """    
    LOG_FILENAME = 'log.out'
    logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG,)

    def writeLog(self, status):
        """
        writeLog is the old way of loggin. It writes to a normal textfile using
        the built-in logging class of Python. Right now this is not used anymore
        because logging now uses SQLite.
        """
        string = ''
        for name, statusTuple in status.iteritems():
            string = string + "\t %s : %s\n" % (name, statusTuple)

        logging.info("\t" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                         + "\n" + string)

    def addLogDict(self, status):
        """
        addLogDict adds any encountered (possible) problems to a SQLite
        database.
        """
        listDefcon = []
        
        db = DatabaseController()
        
        for key, (name, url, status, runtime) in status.iteritems():
            values = (name, url, status, runtime, time.strftime("%Y-%m-%d %H:%M:%S",
                                                  time.localtime()))
            rowId = db.addLog(values)
            listDefcon.append((name, rowId))

        db.setDefcon(listDefcon)

    def checkDefcon(self):
        """
        Check the Defconlist to see if any sites report a level 2 and have no
        notification yet. In that case, send an e-mail alert. Also change
        notified setting so this specific incident is only reported once.
        """
        defconDict = {}
        db = DatabaseController()
        notifyList = db.getDefcon(2,1)
        if len(notifyList) > 0:
            for row in notifyList:
                defconDict[row[0]] = (row[0], row[1], row[2], row[3], row[4])
                db.setNotified(row[0])
                
            alert = EmailAlert()
            alert.sendMail(defconDict)

    def clearDefcon(self, name):
        """
        Any website that did not produce an error this specific check should,
        if on the Defcon list, be lowered in level.
        """
        db = DatabaseController()
        cleanDefcon = db.getDefcon(selection = name)
        if len(cleanDefcon) > 0:
            for row in cleanDefcon:
                db.lowerDefconLevel(row[0], row[1])
        
