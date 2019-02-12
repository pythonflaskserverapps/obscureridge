###################################################

from obscureridge import lichess
from obscureridge.urllibutils import geturljson
from obscureridge.chatbot import Chatbot

from os import environ
import time

###################################################

def getallfeaturedtourneys(kinds = ["created", "started"]):
    alltourneys = geturljson(lichess.getalltourneysurl())    
    allfeaturedtourneys = []
    for kind in kinds:
        tourneys = alltourneys[kind]
        for tourney in tourneys:
            createdby = tourney["createdBy"]
            name = tourney["fullName"]
            if ( createdby == lichess.FEATURED_TOURNEY_CREATOR ) and ( name == lichess.FULL_FEATURED_TOURNEY_NAME ):
                allfeaturedtourneys.append(tourney)
    return allfeaturedtourneys

###################################################

def startup():
    chatuserlila2 = environ.get("CHATUSERLILA2", None)

    tourneys = getallfeaturedtourneys()

    if len(tourneys) > 0:
        tourney = tourneys[0]
        tid = tourney["id"]
        print("found tourney {}".format(tid))
    else:
        print("could not find tourney")

    chatbot = Chatbot(chatuserlila2, tid)

    chatbot.startup()

    time.sleep(60)

    chatbot.shutdown()

###################################################