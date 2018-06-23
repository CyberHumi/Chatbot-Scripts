#################
# Info
#################
# Description: Nanoleaf Aurora Effect Changer application
# Created by: CyberHumi - twitch.tv/CyberHumi, twitter.com/CyberHumiDE
# Version: 1.0

#---------------------------------------
#	Import Libraries
#---------------------------------------
import sys
import os
import json
import codecs
from nanoleaf import Aurora


#---------------------------------------
#	Set Variables
#---------------------------------------
path = os.path.dirname(__file__)
settingsFile = "NAEC.json"
settings = {}


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
#	Nanoleaf Aurora actions
#---------------------------------------
my_aurora = Aurora(settings["nanoleaf"], settings["nanoleaf_token"])
if len(sys.argv) > 1:
    my_aurora.on = True
    my_aurora.effect = sys.argv[1]
else:
    my_aurora.on = False