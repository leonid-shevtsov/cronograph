### cronograph 

Collect, view and analyze cronjob execution logs

## Usage

Log execution of given <cronjob>

    cronograph [path-to-sqlite3-database] <cronjob>
    
Start server on given port (default is 8080)

    cronograph serve [path-to-sqlite3-database] [port]

Default database file used is ~/.cronograph.sqlite3

## Installation

Requires [python](http://python.org).

    `sudo apt-get install python`

If you want to run the built-in server, you'll need [web.py](http://webpy.org), too:

    `sudo easy_install web.py`

Then, drop `cronograph` to some location and instrument your `crontab`:

    0 0 * * * /home/user/bin/cronograph rsnapshot daily

---

Weekend hack by [Leonid Shevtsov](http://leonid.shevtsov.me)
