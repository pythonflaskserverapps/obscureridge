###################################################

import threading, time

import websocket

from queue import Queue
import json

###################################################

from obscureridge import lichess

###################################################

KEEPALIVE_SLEEP = 3
MAX_KEEPALIVE_SECS = lichess.MAX_TOURNEY_LENGTH_MINS * 60

###################################################

class Message:
    def __init__(self, kind, data):
        self.kind = kind
        self.data = data

    def __repr__(self):
        return "{}".format(self.__dict__)

class Chatbot:
    def __init__(self,
        lila2,
        tid
    ):
        self.lila2 = lila2
        self.tid = tid
        self.tourneychaturl = lichess.tourneychaturl(self.tid)
        print("initialized chatbot {} {}".format(self.tid, self.tourneychaturl))

    def talkhandler(self, user, msg):
        print("message {} : {}".format(user, msg))

    def crowdhandler(self, nb, users, anons):
        print("crowd {} : users = {} , anons = {}".format(nb, " ".join(users), anons))

    def messagehandler_thread_target(self):
        while self.alive:            
            try:
                message = self.messagequeue.get(timeout = KEEPALIVE_SLEEP)                                
                if message.kind == "message":
                    self.talkhandler(message.data["u"], message.data["t"])
                if message.kind == "crowd":
                    self.crowdhandler(message.data.get("nb", 0), message.data.get("users", []), message.data.get("anons", 0))
            except:
                pass
        print("message handler thread terminated for {}".format(self.tid))

    def keepalive_thread_target(self):        
        while self.keepalivecnt > 0:            
            self.ws.send("null")
            time.sleep(KEEPALIVE_SLEEP)
            self.keepalivecnt -= 1
        self.ws.close()
        print("keep alive thread terminated for {}".format(self.tid))

    def shutdown(self):
        self.keepalivecnt = 0

    def on_open(self):
        print("socket for {} opened".format(self.tid))
        threading.Thread(target = self.keepalive_thread_target).start()
        threading.Thread(target = self.messagehandler_thread_target).start()

    def on_message(self, message):
        try:
            mobj = json.loads(message)
            kind = mobj["t"]
            data = mobj["d"]            
            self.messagequeue.put(Message(kind, data))
        except:
            pass

    def startup_thread_target(self):
        print("starting up chatbot for {}".format(self.tid))

        self.keepalivecnt = int(MAX_KEEPALIVE_SECS / KEEPALIVE_SLEEP)        

        self.alive = True

        self.messagequeue = Queue()

        self.ws = websocket.WebSocketApp(self.tourneychaturl,        
            on_open = self.on_open,        
            on_message = self.on_message,
            cookie = "lila2={}".format(self.lila2)
        )

        self.ws.run_forever(
            host = "socket.lichess.org",
            origin = "https://lichess.org"
        )

        print("socket terminated for {}".format(self.tid))

        self.alive = False

    def startup(self):
        threading.Thread(target = self.startup_thread_target).start()

###################################################