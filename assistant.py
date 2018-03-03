#!/usr/bin/python2.7

# V1.00
# Slack Assistant
# Tally-up tracking
# Date-time tracking
# Auto-meeting
# Webhook
# log quote

import syslog
import sqlite3
import re
import os
import time
import datetime
import sys
from daemonize import Daemonize
from slackclient import SlackClient

# Setting up the RTM API
from prodtoken import token
sc = SlackClient(token)
avatar = ":metro-robo:"

# Setting up the Web API
import json
import requests
url = "https://hooks.slack.com/services/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"
headers={'Content-Type': 'application/json'}

######################### TESTMODE
testmode = False
###################################################################### SQL and Slack token
if testmode == True:
    pid = "/tmp/sassist-qa.pid"
    app = "assistant-qa"
    nickname = "Camper"
    dump = "#dump"
    channel = "#planif"
else:
    pid = "/tmp/sassist.pid"
    app = "assistant"
    nickname = "Camper"
    dump = "#dump"
    channel = "#planif
###################################################################### Others
wakka = "^\.\.(|\s)"

########################################################################################
# Functions()
########################################################################################

# This function generates a timestamp
def maketimestamp():
    tsnow = datetime.datetime.now()
    timenow = (tsnow.strftime('%Y-%m-%d-%H:%M:%S'))
    return timenow

# This function sends messages to Slack
def slackmsg(msg):
    #data = "{'text':'{0}'}".format(msg)
    #req = requests.get(url,headers=headers,json=data)
    sc.api_call("chat.postMessage", username=nickname, channel=channel, text=msg, icon_emoji=avatar)

# This functions parses the commands
def command_parse(text):

    conn = sqlite3.connect("./camper.db".format(db_path))
    print "DB OK"

    if re.search(wakka + "aide", text) is not None:
        slackmsg("Salope!")





########################################################################################
def main():
    print "start"
    try:
        print "trying"
        if sc.rtm_connect():
            print "open"
            while True:
                for item in sc.rtm_read():
                    message = item.get("text")
                    message = message.encode("utf-8") if message else ""
                    if re.search(r'^\.\.',message):
                        command_parse(message)
                time.sleep(0.5)
        else:
            print "not open "
    except (SystemExit, KeyboardInterrupt):
        raise
    except Exception, e:
        sc.api_call("chat.postMessage", username=nickname, channel=dump, text="{0}".format(e), icon_emoji=avatar)

########################################################################################
#main()
########################################################################################
#if testmode ==  True:
main()
#else:
#    daemon = Daemonize(app=app, pid=pid, action=main)
#    daemon.start()
