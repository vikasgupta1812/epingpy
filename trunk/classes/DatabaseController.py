"""
Global imports
"""
import sqlite3
import os

"""
Import for official python class
"""

"""
Import for ePing.py specific classes
"""

class DatabaseController:
    """
    DatabaseController should be the class to interface between the database
    and ePing.py.
    """

    def __init__(self):
        """
        Get the database setup.
        """
        self.prepareDatabase()

    def getConn(self):
        """
        Return a connection to experiment with
        """
        try:
            self.conn = sqlite3.connect('database/epingpydb.sqlite')
        except sqlite3.Error, e:
            print "An error occured: ", e.args[0]
            
        return self.conn

    def prepareDatabase(self):
        """
        Check if tables exist. If not, create them
        """
        conn = self.getConn()

        conn.execute('''CREATE TABLE IF NOT EXISTS logger\
        (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, url TEXT,\
        status TEXT, runtime TEXT, date DATETIME)''')

        conn.execute('''CREATE TABLE IF NOT EXISTS defcon\
        (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, level INTEGER,\
        log_id INTEGER, notified INTEGER DEFAULT(0))''')

        conn.close()

    def getDefcon(self, level=0, selection=0):
        """
        Return a list with the last entered websites, so can be compared to
        current list of fails. Specific list returned depends on input params.
        """        
        conn = self.getConn()
        cursor = conn.cursor()
            
        if selection == 0:
            cursor.execute('''SELECT name, level FROM defcon WHERE\
            level >= ?''', (level,))
            list_of_sites = cursor.fetchall()
        elif selection == 1:
            cursor.execute('''SELECT l.name, l.url, l.status,\
            l.runtime, l.date FROM defcon AS d LEFT JOIN logger AS l ON\
            d.log_id = l.id WHERE notified = 0 AND level = ?''', (level,))
            list_of_sites = cursor.fetchall()
        else:
            cursor.execute('''SELECT name, level FROM defcon WHERE\
            name = ?''', (selection,))
            list_of_sites = cursor.fetchall()
            
        conn.close()
        return list_of_sites

    def addLog(self, values):
        """
        Any encountered error will be logged in the database, whether an
        e-mail alert will be send or not. 
        """
        conn = self.getConn()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO logger VALUES (NULL, ?,\
?, ?, ?, ?)', values)
        conn.commit()
        cursor.execute('SELECT last_insert_rowid()')
        for row in cursor:
            rowId = row[0]
        cursor.close()
        return rowId

    def raiseDefconLevel(self, name, rowId, level=0):
        """
        Raise the defonlevel. Insert if does not exist. Higher if level = 1.
        Update the log_id if level is 2.
        """
        conn = self.getConn()
        cursor = conn.cursor()

        params = (rowId, name)
        
        if (level == 2):
            cursor.execute('''UPDATE defcon SET log_id = ? WHERE\
                name = ?''',params)
        elif (level == 1):
            cursor.execute('''UPDATE defcon SET level = 2, log_id = ? WHERE\
                name = ?''',params)
        elif (level == 0):
            cursor.execute('''INSERT INTO defcon (log_id, name, level) VALUES\
            (?, ?, 1)''', params)

        conn.commit()
        cursor.close()

    def lowerDefconLevel(self, name, level):
        """
        Lower Defconlevel. If level is 2, lower to 1. If 1, remove from
        Defconlist
        """
        conn = self.getConn()
        cursor = conn.cursor()

        name = (name,)
        
        if(level == 1):
            cursor.execute('''DELETE FROM defcon WHERE name = ?''',\
                           name)
        elif (level == 2):
            cursor.execute('''UPDATE defcon SET level = 1, notified = 1 WHERE\
                name = ?''', name)

        conn.commit()
        cursor.close()
        
    def setDefcon(self, names):
        """
        Check Defconlist against list with encountered incidents.
        """
        listDefcon = {}
        for key, value in self.getDefcon():
            listDefcon[key] = value
        
        for name, rowId in names:
            if name in listDefcon:
                 self.raiseDefconLevel(name, rowId, listDefcon[name])
                 del listDefcon[name]
            elif not name in listDefcon:
                 self.raiseDefconLevel(name, rowId)

        for key, value in listDefcon.iteritems():
            self.lowerDefconLevel(key, value)

    def setNotified(self, name):
        """
        Mark this site as notified, so will only be notified once.
        """
        conn = self.getConn()
        cursor = conn.cursor()

        name = (name,)

        cursor.execute('''UPDATE defcon SET notified = 1 WHERE name = ?''',\
                       name)

        conn.commit()
        cursor.close()
    
