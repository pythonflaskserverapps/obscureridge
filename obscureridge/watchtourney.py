###################################################

from obscureridge import lichess

from obscureridge.urllibutils import geturljson

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
