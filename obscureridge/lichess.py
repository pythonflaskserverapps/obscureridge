###################################################

from os import environ

###################################################

API_URL = "https://lichess.org/api"

###################################################

def getalltourneysurl():
    return "{}/tournament".format(API_URL)

###################################################

FEATURED_TOURNEY_NAME = environ.get("FEATUREDTOURNEY", "AtomicChessBot Blitz Tourney")

def fulltourneyname(tourneyname):
    return tourneyname + " Arena"

FULL_FEATURED_TOURNEY_NAME = fulltourneyname(FEATURED_TOURNEY_NAME)

FEATURED_TOURNEY_CREATOR = environ.get("FEATUREDTOURNEYCREATOR", "handywebprojects")

###################################################
