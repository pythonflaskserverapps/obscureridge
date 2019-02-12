###################################################

from obscureridge import lichess
from obscureridge.urllibutils import geturljson
from obscureridge.chatbot import Chatbot

from os import environ
import time
import random

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

class MyChatbot(Chatbot):
    def __init__(self, lila2, tid):
        super().__init__(lila2, tid)

    def talkhandler(self, user, msg):
        print("MY message {} : {}".format(user, msg))

    def crowdhandler(self, nb, users, anons):
        print("MY crowd {} : users = {} , anons = {}".format(nb, " ".join(users), anons))

    def gamefinishedhandler(self, gid):                
        gobj = self.games[gid]
        ratingbias = gobj["ratingBias"]
        score = gobj["score"]
        nomoves = len(gobj["moves"])
        whitename = gobj["whiteName"]
        whiterating = gobj["whiteRating"]
        blackname = gobj["blackName"]
        blackrating = gobj["blackRating"]
        rs = ratingbias * score        
        if ( rs < -100 ) and ( nomoves > 1 ):            
            upset = whitename            
            upsetloser = blackname
            if score < 0:
                upset = blackname
                upsetloser = whitename            
            self.say(random.choice([
                "what a game {} against {}".format(upset, upsetloser),
                "wow {} defeats {}".format(upset, upsetloser),
                "unbelievable {} beating {} higher rated".format(upset, abs(ratingbias))
            ]))
            if upset == blackname:
                self.say("with black!")            

def startup():
    chatuserlila2 = environ.get("CHATUSERLILA2", None)

    tourneys = getallfeaturedtourneys()

    if len(tourneys) > 0:
        tourney = tourneys[0]
        tid = tourney["id"]
        print("found tourney {}".format(tid))
    else:
        print("could not find tourney")

    chatbot = MyChatbot(chatuserlila2, tid)

    chatbot.startup()

    time.sleep(600)

    chatbot.shutdown()

###################################################