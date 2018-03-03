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
import traceback
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

###################################################################### Vars
pid = "/tmp/sassist.pid"
app = "assistant"
nickname = "Metro"
dump = "#dump"
channel = "#planif"
wakka = "^\.\.(|\s)"

###################################################################### Traceback to Slack
def report_exception(exc_type, exc_value, exc_tb):
    sc.api_call("chat.postMessage", username=nickname, channel=dump, icon_emoji=avatar, text="{0}\n{1}\n{2}".format(
        exc_type,exc_value,''.join(traceback.format_tb(exc_tb))))

def custom_excepthook(exc_type, exc_value, exc_tb):
    report_exception(exc_type, exc_value, exc_tb)
    sys.__excepthook__(exc_type, exc_value, exc_tb)  # run standard exception hook

sys.excepthook = custom_excepthook

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

    conn = sqlite3.connect("./camper.db")
    print "DB OK"

    if re.search(wakka + "aide", text) is not None:
        slackmsg("1")

    if re.search("{0}aide".format(wakka), text) is not None:
        slackmsg("2")

    if re.search("^\.\.(|\s)aide", text) is not None:
        slackmsg("3")



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
        raise RuntimeError(e)

########################################################################################
#main()
########################################################################################
#if testmode ==  True:
main()
#else:
#    daemon = Daemonize(app=app, pid=pid, action=main)
#    daemon.start()
