#!/usr/bin/python
"""
This python code is the start of my project to create a status checker
for the various websites we employ at work. Ideally it will be easily extensible
with more websites, and give detailed statistics.
qrazi.sivlingworkz@gmail.com
"""

"""
Import for ePing.py specific classes
"""
from classes.ActionController import ActionController

"""
#create the ActionController. Right now this will imediately check
#all urls in the config file, log any problems and send alerts if necessary.
"""
ac = ActionController()


