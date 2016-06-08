### About:

I started this project because the company I currently work for employs 
several websites which tend to be badly reachable. Our maintance guys will
get an alert by SMS when the servers is unpingable, but as it happens, the
server itself remains pingable. The sites just don't give any output.
This small program checks the urls, and reports any HTTP error status or timeout
problems.


### Installation:

- Install Python 2.6
- Fill in all the settings in the config.cfg file
- Run eping.py by:
    - double clicking from any desktop environment
    - typing \installeddirectory\eping.py from the commandline
    - Schedule the running of eping.py with cron or Windows Task Scheduler
  Most practical is of course to create a cronjob or schedule a task 
  (*nix and Windows respectively) with a desired period.
  
### ToDo:
- Daemonize eping.py? Then no need to use cronjob/taskscheduler
- Customizable e-mail/log text's

### Changelog:
#### v0.07 - 2010/04/19
- Expanded the database setup. 
- Added an extra layer of checking before sending an alert. Now when an error is
encountered, ePing.py will log this event. When the next check encounters again
an error, the alert will be send. If this next run did not encounter an error,
ePing.py assumes it was just a hickup and lowers the threatlevel.

#### v0.06 - 2010/02/07
- Changed logging from textfile to database 

#### v0.051 - 2009/11/6
- Fixed extended timeout function

#### v0.05 - 2009/11/6
- Working (properly verified now!) threaded checking of websites so that the
maximum amount of time on run takes is now no longer then the default timeout
and some seconds for other tasks, instead of (default
timeout + extended timeout) * amount of websites to be checked.

#### v0.04 - 2009/10/21
- Checking of HTTP header status is now threaded, so interval of ePing.py
execution can be as tight as the defined timeout values combined.
- Cleaned up sourcecode by putting each class in a separate *.py
- When only default timeout is hit, this event will be put in log with value 
of default timeout

#### v0.03 - 2009/08/28
- The timeout is now configurable in the config file. Default timeout is the 
timeout in seconds to be used. Extended will be used when default has been 
surpassed

#### v0.02 - 2009/07/30
- If timeout is encountered, try again with timeout of 30 seconds. Only email
if this timeout is also reached.

#### v0.01 - 2009/07/23 
- the very first public release!
