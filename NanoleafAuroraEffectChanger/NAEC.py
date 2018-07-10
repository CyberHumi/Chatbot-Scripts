#---------------------------------------
#	Import Libraries
#---------------------------------------
import sys
import os
import json
import codecs
import re
import websocket
try:
    import thread
except ImportError:
    import _thread as thread
import time
from nanoleaf import Aurora


#---------------------------------------
#	[Required]	Script Information
#---------------------------------------
ScriptName = "NA Effect Changer"
Website = "https://www.twitch.tv/CyberHumi"
Creator = "CyberHumi"
Version = "1.1"
Description = "Nanoleaf Aurora Effect Changer"


#---------------------------------------
#	Set Variables
#---------------------------------------
path = os.path.dirname(__file__)
settingsFile = "NAEC.json"
apiFile = "API_Key.js"
settings = {}
auth = {}
res = {}


print("")
print("#####################################################")
print("# Nanoleaf Aurora Effect Changer - Websocket cleint #")
print("#####################################################")
print("")
print("Python version: " + sys.version)
print("")


#---------------------------------------
#	Get settings
#---------------------------------------
try:
    with codecs.open(os.path.join(path, settingsFile), encoding='utf-8-sig', mode='r') as file:
        settings = json.load(file, encoding='utf-8-sig')
        print ("read settings file: ", path + "\\" + settingsFile)
except:
    print("Unexpected error:", sys.exc_info())
    sys.exit("cannot read settings file")
    pass

	
#---------------------------------------
#	Get API key
#---------------------------------------
try:
    with codecs.open(os.path.join(path, apiFile), encoding='utf-8-sig', mode='r') as file:
        js = file.readlines()
    print ("read API file: ", path + "\\" + apiFile)
    parts = js[0].split(";")
    matcher_rex = re.compile(r'^.+=\s+"(?P<var>\w+)"')
    matches = matcher_rex.match(parts[0].strip())
    if matches:
       res = matches.groups()
       apiKey = res[0]
       auth.update({
           "api_key": apiKey,
           "events": [
               "EVENT_SUB",
               "EVENT_FOLLOW",
               "EVENT_HOST",
               "EVENT_RAID",
               "EVENT_DONATION",
               "EVENT_CHEER",
               "EVENT_NAEC"			# for chat cmd
           ]
       })
       jsonAuth = json.dumps(auth, separators=(',',':'))
    else:
        sys.exit("> no API Key")
    matcher_rex = re.compile(r'^.+=\s+"(?P<var>.+)"')
    matches = matcher_rex.match(parts[1].strip())
    if matches:
       res = matches.groups()
       apiSocket = res[0].strip()
    else:
        sys.exit("> no API Socket")
except:
    print("Unexpected error:", sys.exc_info())
    sys.exit("cannot read API file")
    pass


#---------------------------------------
#	Nanoleaf Aurora actions
#---------------------------------------
def nanoAction(event,message):
    try:
        host = settings["nanoleaf"]
        token = settings["nanoleaf_token"]
        if event == "naec":
            naec = json.loads(json.loads(message, encoding='utf-8')["data"])
            effect_new = naec["effect_new"]
            duration = int(naec["effect_duration"])
            effect_default = naec["effect_default"]
            parameter = naec["effect_parameter"]
        elif settings[event+"_effect"] != '':
            effect_new = settings[event+"_effect"]
            duration = int(settings[event+"_effectduration"])
            effect_default = settings["default_effect"]
        else:
            return
        my_aurora = Aurora(host, token)
        my_aurora.on = True
        my_aurora.effect = effect_new
        print("change effect to '" + effect_new + "' for " + str(duration) + " seconds")
        if duration > 0:
            time.sleep(duration)
            my_aurora.effect = effect_default
            print("change effect to '" + effect_default + "'")
    except:
        pass

print("")

#---------------------------------------
#	functions
#---------------------------------------
def on_message(ws, message):
    event = json.loads(message)["event"].split("_")[1].lower()
    print("event: " + event)
    nanoAction(event,message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### websocket closed ###")

def on_open(ws):
    def run(*args):
        print("### open websocket ###")
        print("## connect to "+ apiSocket)
        print("")
        print("+------------------------------------------------+")
        print("| DO NOT CLOSE THIS COMMAND PROMPT               |")
        print("+------------------------------------------------+")
        print("")
        print("Event log")
        print("=========")
        ws.send(jsonAuth)
        while True:
            time.sleep(1)
        ws.close()
        print("thread terminating...")
    thread.start_new_thread(run, ())

	
#---------------------------------------
#	Open websocket
#---------------------------------------
if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(apiSocket,
                             on_message = on_message,
                             on_error = on_error,
                             on_close = on_close
                            )
    ws.on_open = on_open
    ws.run_forever()

