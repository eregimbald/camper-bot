#!/usr/bin/python2.7

import sqlite3
import time
import calendar
import datetime
import os
import sys
import re

db = "./camper.db".format(os.path.dirname(__file__))

conn = sqlite3.connect(db)
c = conn.cursor()

#t1 = int(time.time())
#t3 = time.localtime(t1)

#print str(calendar.month_abbr[t3.tm_mon]) + " " + str(t3.tm_mday) + " " + str(t3.tm_hour) + ":" + str(t3.tm_min)
################################################################################################
def maketimestamp():
    tsnow = datetime.now()
    timenow = (tsnow.strftime('%Y-%m-%dT%H:%M:%S'))
    return timenow

# REGEXP for SQlite3
def regexp(expr, item):
    reg = re.compile(expr)
    return reg.search(item) is not None

def remake():
    print "remake"
     #filters(id INTEGER PRIMARY KEY, date text, count text, filter text, day1 text, day2 text, day3 text);
    c.execute("ALTER TABLE critical RENAME TO old")
    c.execute("CREATE TABLE critical (id INTEGER PRIMARY KEY, date text, count text, filter text, description text)")
    c.execute("INSERT INTO critical (id, date, count, filter) SELECT id, date, count, filter FROM old")
    c.execute("DROP table old")

def new():
    print "new"
#    c.execute("drop table bgp_state")
#    c.execute("drop table bgp_neighbor")
#CREATE TABLE throttle (id INTEGER PRIMARY KEY, message text, latest text, time text, counter integer);
    c.execute("CREATE TABLE quotes (user text, quote text)")

def load(mylist):
    print "load"
    for i in mylist:
        c.execute("INSERT INTO providers (provider) VALUES (?)",(i,))

def dictload(mydict):
    print "dictload"
    #db_rows = c.execute("SELECT * FROM datacenters")
    #db_rows = db_rows.fetchall()
    for key, value in mydict.iteritems():
        query = "UPDATE datacenters SET city = '{1}' WHERE datacenter = '{0}'".format(key, value)
        print query
        c.execute(query)


################################################################################################

dev_list = ["rtr-wan-bos1",
            "rtr-wan-bos2",
            "rtr-inet-bos1",
            "rtr-vpn-bos2",
            "sw-core-bos-c",
            "sw-edge-bos-d",
            "rtr-nni-bos1",
            "rtr-edge-bos1",
            "rtr-cpe-bos1"]

providerlist = ["zayo",
                "gtt",
                "ntt",
                "century link",
                "clink",
                "hibernia",
                "sprint",
                "wind",
                "masergy",
                "epsilon",
                "bt",
                "comcast",
                "voxbone",
                "amazon",
                "aws",
                "level3",
                "level (3)",
                "xo",
                "gamma",
                "inap",
                "pnap",
                "colt"]

dclist = {"bos":"boston",
          "sjo":"san jose",
          "sfo":"san francisco",
          "ash":"ashburn",
          "nje":"new jersey",
          "lon":"london",
          "fra":"frankfurt",
          "hkg":"hong kong",
          "sin":"singapore",
          "syd":"sydney"}

###Main###
new()
#remake()
#load(providerlist)
#dictload(dclist)

conn.commit()
conn.close()
print "Work complete on: {0}".format(db)
