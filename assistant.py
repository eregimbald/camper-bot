#!/usr/bin/python2.7
#coding=utf-8

# V1.00
# Session
# Auto-meeting
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
nickname = "Métro"
dump = "#dump"
channel = "#planif"
wakka = "^\.\.(|\s)"
session = "Chalet Hiver 2018"

###################################################################### Traceback to Slack
def report_exception(exc_type, exc_value, exc_tb):
    sc.api_call("chat.postMessage", username=nickname, channel=dump, icon_emoji=avatar, text="```{0}\n{1}\n{2}```".format(
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
    timenow = (tsnow.strftime('%Y-%m-%d'))
    return timenow

# This function sends messages to Slack
def slackmsg(msg):
    #data = "{'text':'{0}'}".format(msg)
    #req = requests.get(url,headers=headers,json=data)
    sc.api_call("chat.postMessage", username=nickname, channel=channel, text=msg, icon_emoji=avatar)

# Converting user Id to display name
def map_user(user):
    userinfo = sc.api_call("users.info", user=user)
    return userinfo["user"]["profile"]["display_name"]

# This functions parses the commands
def command_parse(text,user):

    conn = sqlite3.connect("./metro.db")
    c = conn.cursor()

    user = map_user(user)

    if re.search(wakka + "aide", text) is not None:
        report  = "*Chaque commande doit être précédée de ..*"
        report += "\nExemple: `..log` OU `.. log`"
        report += "\n..log - Affiche la liste des dépenses"
        report += "\n..log 111.11 sac de patates - Crée une dépense pour un sac de patates à 111.11$ (p.s tu t'es fait fourrer)"
        report += "\n..quote - Affiche la liste des citations"
        report += "\n..quote Alphonse n'importe quoi - Crée une citation au nom d'Alphonse"
        report += "\n..flush - Éfface toutes les dépense au nom de l'utilisateur"

    if re.search(wakka + "quote", text) is not None:
        if re.search(wakka + "quote$", text) is not None:
            db_rows = c.execute("SELECT * FROM quotes")
            db_rows = db_rows.fetchall()
            if db_rows:
                report = "*Voici nos meilleures citations (Je promet rien)*"
                for row in db_rows:
                    report += "\n{0} - *{1}*".format(row[0],row[1])
                slackmsg(report)
            else:
                slackmsg("La list des citations est vide")
        elif re.search(wakka + "quote\s(.*)", text) is not None:
            matches = r.groups()
            quote = matches[1]
            c.execute("INSERT INTO quotes (user, quote) Values (?,?)", (user,quote)
            conn.commit()

    elif re.search(wakka + "log", text) is not None:
        # user, cash, description, session, timestamp
        if re.search(wakka + "log$", text) is not None:
            db_rows = c.execute("SELECT * FROM depenses")
            db_rows = db_rows.fetchall()
            if db_rows:
                report = "*Voici la liste des dépenses*"
                total = float()
                for row in db_rows:
                    report += "\n*{0}* | {1}$ | {2} | {3} | {4}".format(row[0],row[1],row[2],row[3],row[4],)
                    total += float(row[1])
                report += "\n *Total:* {0}$".format(round(total,2))
                slackmsg(report)
            else:
                slackmsg("La list des dépenses est vide")
        elif re.search(wakka + "log " + "(\d{1,4}\.\d{1,2}|\d{1,4})\s(.*)", text) is not None:
            r = re.search(wakka + "log " + "(\d{1,4}\.\d{1,2}|\d{1,4})\s(.*)", text)
            matches = r.groups()
            cash = matches[1]
            desc = matches[2] #if matches[2] else ""

            c.execute("INSERT INTO depenses (user, cash, description, session, timestamp) Values (?,?,?,?,?)", (user,cash,desc,session,maketimestamp()))
            conn.commit()
            #db_rows = c.execute("SELECT * FROM depenses WHERE user = ? AND cash = ?",(user,cash))
            #db_rows = db_rows.fetchall()
            slackmsg("*{0}* a paye {1}$ de {2}".format(user,cash,desc))

        else:
            slackmsg("Votre commande est aussi érronée qu'une jobe de moutarde.")


    elif re.search(wakka + "flush$", text) is not None:
        c.execute("DELETE FROM depenses WHERE user = ?",(user,))
        conn.commit()
        slackmsg("J'ai effacé toutes les dépenses de {0}".format(user))

    elif re.search(wakka + "flush all$", text) is not None:
        if user == "Manu":
            c.execute("DELETE FROM depenses")
            c.execute("DELETE FROM quotes")
            conn.commit()
            slackmsg("J'ai vidé les listes")
        else:
            slackmsg("Bel essai, salope")

    conn.close()

########################################################################################
def main():
    try:
        if sc.rtm_connect():
            while True:
                for item in sc.rtm_read():
                    message = item.get("text")
                    message = message.encode("utf-8") if message else ""
                    user = item.get("user")
                    if re.search(wakka,message):
                        command_parse(message,user)
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
