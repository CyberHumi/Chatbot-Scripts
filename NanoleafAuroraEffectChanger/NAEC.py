#---------------------------------------
#   Import Libraries
#---------------------------------------
import sys
import os
import json
import codecs
import re
import websocket
import threading
try:
    import thread
except ImportError:
    import _thread as thread
import time
import queue
from nanoleaf import Aurora


#---------------------------------------
#   [Required]  Script Information
#---------------------------------------
ScriptName = "NA Effect Changer"
Website = "https://www.twitch.tv/CyberHumi"
Creator = "CyberHumi"
Version = "1.5"
Description = "Nanoleaf Aurora Effect Changer"


#---------------------------------------
#   Set Variables
#---------------------------------------
path = os.path.dirname(__file__)
settingsFile = "NAEC.json"
apiFile = "API_Key.js"
settings = {}
auth = {}
res = {}
wsServer = ""
jsonAuth = ""
space = ""
nl12 = "Nanoleaf Aurora 1 + 2"
nl1 = "Nanoleaf Aurora 1 only"
nl2 = "Nanoleaf Aurora 2 only"

# message queue
BUF_SIZE = 200
q = queue.Queue(BUF_SIZE)


#---------------------------------------
#   Get settings
#---------------------------------------
def readSettings():
    global settings,space
    try:
        with codecs.open(os.path.join(path, settingsFile), encoding='utf-8-sig', mode='r') as file:
            settings = json.load(file, encoding='utf-8-sig')
            print (space + "read settings: " + path + "\\" + settingsFile)
    except:
        print("Unexpected error:", sys.exc_info())
        sys.exit("cannot read settings")
        pass


#---------------------------------------
#   Get API key and prepare JSON for SLCB auth.
#---------------------------------------
def readAPIkey():
    global wsServer, jsonAuth
    try:
        with codecs.open(os.path.join(path, apiFile), encoding='utf-8-sig', mode='r') as file:
            js = file.readlines()
        print ("read API key file: " + path + "\\" + apiFile)
        parts = js[0].split(";")
        matcher_rex = re.compile(r'^.+=\s+"(?P<var>\w+)"')
        matches = matcher_rex.match(parts[0].strip())
        if matches:
            res = matches.groups()
            apiKey = res[0]
            auth.update({
                "api_key": apiKey,
                "events": [
                    "EVENT_SUB",         # Twitch sub
                    "EVENT_MX_SUB",      # Mixer sub
                    "EVENT_YT_SUB",      # YouTube sub
                    "EVENT_FOLLOW",      # Twitch follow
                    "EVENT_MX_FOLLOW",   # Mixer follow
                    "EVENT_HOST",        # Twitch host
                    "EVENT_MX_HOST",     # Mixer host
                    "EVENT_RAID",        # Twitch raid
                    "EVENT_DONATION",    # Mixer/Twitch/YouTube donation
                    "EVENT_CHEER",       # Twitch cheer
                    "EVENT_NAEC",        # chat command
                    "EVENT_NAECUPDATE"   # update settings
                ]
            })
            jsonAuth = json.dumps(auth, separators=(',',':'))
        else:
            sys.exit("> no API Key")
        matcher_rex = re.compile(r'^.+=\s+"(?P<var>.+)"')
        matches = matcher_rex.match(parts[1].strip())
        if matches:
            res = matches.groups()
            wsServer = res[0].strip()
        else:
            sys.exit("> no API Socket")
    except:
        print("Unexpected error:", sys.exc_info())
        sys.exit("cannot read API file")
        pass


#---------------------------------------
#   functions
#---------------------------------------
def on_message(ws, message):
    part = 1
    # for Mixer and YouTube events
    if len(json.loads(message)["event"].split("_")) == 3:
        part = 2
    event = json.loads(message)["event"].split("_")[part].lower()
    q.put(message);
    print("event: > %s (%s in queue)" % (event,q.qsize()))

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### websocket closed ###")

def on_open(ws):
    def run(*args):
        print("")
        print("#####################################################")
        print("# Nanoleaf Aurora Effect Changer - Websocket client #")
        print("#####################################################")
        print("")
        print("### open websocket ###")
        print("## connect to "+ wsServer)
        print("")
        print("+---------------------------------------------------+")
        print("| DO NOT CLOSE THIS COMMAND PROMPT                  |")
        print("+---------------------------------------------------+")
        print("")
        print("Event log")
        print("=========")
        ws.send(jsonAuth)
        while True:
            time.sleep(1)
        ws.close()
        print("thread terminating...")
    thread.start_new_thread(run, ())


class NanoThread(threading.Thread):
    #---------------------------------------
    #   Nanoleaf Aurora actions
    #---------------------------------------
    def nanoAction(message):
        global settings
        print("       < %s in queue" % q.qsize())
        part = 1
        # for Mixer and YouTube events
        if len(json.loads(message)["event"].split("_")) == 3:
            part = 2
        event = json.loads(message)["event"].split("_")[part].lower()
        try:
            host = settings["nanoleaf"]
            token = settings["nanoleaf_token"]
            host2 = settings["nanoleaf2"]
            token2 = settings["nanoleaf2_token"]
            device = nl12
            if event+"_device" in settings:
                device = settings[event+"_device"]
            if event == "connected":
                print("         + devices")
                if host != "":
                    print("           o "+nl1+" ("+host+")")
                if host2 != "":
                    print("           o "+nl2+" ("+host2+")")
                print("         + waiting for events ...")
                return
            elif event == "naec":
                data = json.loads(json.loads(message, encoding='utf-8-sig')["data"])
                effect_new = data["effect_new"]
                duration = int(data["effect_duration"])
                effect_default = data["effect_default"]
                parameter = data["effect_parameter"]
            elif event == "naecupdate":
                readSettings()
                return
            elif settings[event+"_effect"] != '':
                effect_new = settings[event+"_effect"]
                duration = int(settings[event+"_effectduration"])
                effect_default = settings["default_effect"]
                if( event == "host"):
                    data = json.loads(json.loads(message, encoding='utf-8-sig')["data"])
                    if( int(data["viewers"]) < int(settings["host_minviewers"]) ):
                        return
                elif( event == "cheer" ):
                    data = json.loads(json.loads(message, encoding='utf-8-sig')["data"])
                    if( int(data["bits"]) < int(settings["cheer_minbits"]) ):
                        return
            else:
                return
            if( event == "host"):
                print("         + " + event + " (" + str(data["viewers"])+" viewers)")
            elif( event == "cheer" ):
                print("         + " + event + " (" + str(data["bits"])+" bits)")
            else:
                print("         + " + event)
            print("         + actions")
            if host != "" and '1' in device:
                my_aurora = Aurora(host, token)
                my_aurora.on = True
                my_aurora.effect = effect_new
            else:
                print("no '1' in "+device)
            if host2 != "" and '2' in device:
                my_aurora2 = Aurora(host2, token2)
                my_aurora2.on = True
                my_aurora2.effect = effect_new
            if duration>0:
                durationtext = " for " + str(duration) + " seconds"
            else:
                durationtext = ""
            print("           o change effect to '" + effect_new + "'" + durationtext)
            if duration > 0:
                time.sleep(duration)
                if host != "" and '1' in device:
                    my_aurora.effect = effect_default
                if host2 != "" and '2' in device:
                    my_aurora2.effect = effect_default
                print("           o change effect to '" + effect_default + "'")
        except KeyError:
            pass
        except ValueError:
            print("Could not convert data to an integer.")
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

    def run(self):
        while True:
            if not q.full():
                NanoThread.nanoAction(q.get())
        return



#---------------------------------------
#   Open websocket
#---------------------------------------
print("Python version: " + sys.version)
print("NAEC version: " + Version)
print("")
readAPIkey()
readSettings()
space = "       "
print("")
if __name__ == "__main__":
    t = NanoThread(name='nanothread')
    t.start()
    websocket.enableTrace(True)
    while True:
        ws = websocket.WebSocketApp(wsServer,
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close
                                )
        ws.on_open = on_open
        ws.run_forever()
