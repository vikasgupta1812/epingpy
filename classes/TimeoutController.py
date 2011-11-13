import socket

class TimeoutController:
    """
    Python by default has no timeout at all. TimeoutController can be used
    to change the timeout value. When this class is instantiated, it gives
    a default value of 30 seconds. This can of course be changed with
    setTimeout(). getTimeout() returns the timeout value.
    """
    def __init__(self):
        """
        The default timeout for socket is basically unlimited. 30 seconds
        seems way more reasonably for almost any purpose
        """
        if(socket.getdefaulttimeout() == None):
            socket.setdefaulttimeout(30)
        
    def setTimeout(self, timeout):
        """
        Change the time before timeout, in seconds
        """
        socket.setdefaulttimeout(timeout)

    def getTimeout(self):
        """
        Return the timeout set for this session. Should be set in any case,
        but just to be sure if..else struct.
        """
        if(socket.getdefaulttimeout() != None):
            return socket.getdefaulttimeout()
        else:
            return 'No timeout set'
