#---------------------------------------
#   Import Libraries
#---------------------------------------
import clr
clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")
import os
import json
import codecs


#---------------------------------------
#   [Required]	Script Information
#---------------------------------------
ScriptName = "Nanoleaf Integration"
Website = "https://www.twitch.tv/CyberHumi"
Creator = "CyberHumi"
Version = "1.0"
Description = "Nanoleaf Integration for Streamlabs Chatbot"

#---------------------------------------
#   Set Variables
#---------------------------------------
configFile = "NI4SLCB.json"
settings = {}

#---------------------------------------
#   read config file
#---------------------------------------
def readConfigFile():
    global settings, configFile

    path = os.path.dirname(__file__)
    try:
        with codecs.open(os.path.join(path, configFile), encoding='utf-8-sig', mode='r') as file:
            settings = json.load(file, encoding='utf-8-sig')
    except:
        settings = {
            "chat_command": "!nl",
            "chat_brightness": True,
            "chat_command_permission": "Moderator",
            "chat_command_onEvent": "$username changed Nanoleaf light effect",
            "chat_command_costs": 0,
            "chat_command_cooldown": 5,
            "chat_command_onCooldown": "$username, the command is still on cooldown for $cd seconds!",
            "chat_command_usercooldown": 5,
            "chat_command_onUserCooldown": "$username the command is still on user cooldown for $cd seconds!",
            "chat_command_responseNotEnoughPoints": "It seems $username has not enough $currency.",
            "chat_cmd1": "",
            "chat_cmd2": "",
            "chat_cmd3": "",
            "chat_cmd4": "",
            "chat_cmd5": "",
            "chat_cmd6": "",
            "chat_cmd7": "",
            "chat_cmd8": "",
            "chat_cmd9": "",
            "chat_cmd10": ""
        }

#---------------------------------------
#   [Required] Initialize Data / Load Only
#---------------------------------------
def Init():
    global settings
    path = os.path.dirname(__file__)
    readConfigFile()
    return

def Execute(data):
    global settings, userId, username, ScriptName

    chatCommand = {
        "command": settings["chat_command"],
        "effectName": "",
        "brightness": -1,
        "name": data.User,
        "display_name": data.UserName
    }

    cmds = [ settings["chat_command"], settings["chat_cmd1"], settings["chat_cmd2"], settings["chat_cmd3"], settings["chat_cmd4"], settings["chat_cmd5"], settings["chat_cmd6"], settings["chat_cmd7"], settings["chat_cmd8"], settings["chat_cmd9"], settings["chat_cmd10"] ]
    if data.IsChatMessage() and Parent.HasPermission(data.User, settings["chat_command_permission"], "") and data.GetParam(0) in cmds:
        tempResponseString = ""
        userId = data.User
        username = data.UserName
        cd = ""

        effect_new = ""
        # master chat command
        if data.GetParam(0) == settings["chat_command"]:
            chatCommand["command"] = "MASTER"
            for x in range(1, data.GetParamCount()):
                if settings["chat_brightness"] and x == data.GetParamCount()-1:
                    try:
                        chatCommand["brightness"] = int(data.GetParam(x))
                    except:
                        effect_new += data.GetParam(x) + " "
                else:
                    effect_new += data.GetParam(x) + " "
        # additional chat command
        else:
            for x in range(1,11):
                if data.GetParam(0) == settings["chat_cmd"+str(x)]:
                   chatCommand["command"] = "CMD"+str(x)
                   if settings["chat_brightness"] and data.GetParamCount()>1:
                    try:
                        chatCommand["brightness"] = int(data.GetParam(1))
                    except:
                        pass
                   break;
        if chatCommand["brightness"] < 0 or chatCommand["brightness"] > 100:
            chatCommand["brightness"] = -1;
        effect_new = effect_new.strip()
        if effect_new != "":
            chatCommand["effectName"] = effect_new

        # Check if the User has enough points
        if settings["chat_command_costs"] > Parent.GetPoints(userId):
            tempResponseString = settings["chat_command_responseNotEnoughPoints"]
            tempResponseString = tempResponseString.replace("$currency", str(Parent.GetCurrencyName()))
        # Check if there is a cooldown active
        elif settings["chat_command_usercooldown"] and (Parent.IsOnCooldown(ScriptName, "CMD") or Parent.IsOnUserCooldown(ScriptName, "CMD", userId)):
            if Parent.GetCooldownDuration(ScriptName, "CMD") > Parent.GetUserCooldownDuration(ScriptName, "CMD", userId):
                cd = Parent.GetCooldownDuration(ScriptName, "CMD")
                tempResponseString = settings["chat_command_onCooldown"]
            else:
                cd = Parent.GetUserCooldownDuration(ScriptName, "CMD", userId)
                tempResponseString = settings["chat_command_onUserCooldown"]
            tempResponseString = tempResponseString.replace("$cd", str(cd))
        else:
            if int(settings["chat_command_costs"]) > 0:
                Parent.RemovePoints(userId, username, settings["chat_command_costs"])

            # send effect change request
            Parent.BroadcastWsEvent("EVENT_CHATCMD", json.dumps(chatCommand, encoding='utf-8-sig'))
            tempResponseString = settings["chat_command_onEvent"]

            Parent.AddUserCooldown(ScriptName, "CMD", userId, settings["chat_command_usercooldown"])
            Parent.AddCooldown(ScriptName, "CMD", settings["chat_command_cooldown"])

        tempResponseString = tempResponseString.replace("$username", str(username))
        tempResponseString = tempResponseString.replace("$user", str(username))
        Parent.SendStreamMessage(tempResponseString)
    return

def Tick():
    return

#---------------------------
#   [Optional] Reload Settings (Called when a user clicks the Save Settings button in the Chatbot UI)
#---------------------------
def ReloadSettings(jsonData):
    readConfigFile()
    return

#---------------------------
#   [Optional] ScriptToggled (Notifies you when a user disables your script or enables it)
#---------------------------
def ScriptToggled(state):
    if( state ):
        readConfigFile()
    return


#---------------------------
#   Weblinks
#---------------------------
def OpenWebsiteGitHub():
    os.startfile("https://github.com/CyberHumi/NI4SLCB")
    return

def OpenWebsiteGitHubInstallation():
    os.startfile("https://github.com/CyberHumi/NI4SLCB/wiki/Installation")
    return

def OpenWebsiteTwitter():
    os.startfile("https://twitter.com/CyberHumiDE")
    return

def OpenWebsiteTwitch():
    os.startfile("https://www.twitch.tv/cyberhumi")
    return

def OpenWebsiteDiscord():
    os.startfile("https://discord.gg/UYpvv55")
    return

