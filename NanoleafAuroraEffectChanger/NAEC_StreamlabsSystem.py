#---------------------------------------
#	Import Libraries
#---------------------------------------
import clr
clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")
import os
import json
import codecs


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
configFile = "NAEC.json"
settings = {}

#---------------------------------------
#   [Required] Initialize Data / Load Only
#---------------------------------------
def Init():
    global settings, configFile

    path = os.path.dirname(__file__)
    try:
        with codecs.open(os.path.join(path, configFile), encoding='utf-8-sig', mode='r') as file:
            settings = json.load(file, encoding='utf-8-sig')
    except:
        settings = {
            "chat_command": "!naec",
            "chat_command_permission": "Moderator",
            "chat_command_onEvent": "$username changed Nanoleaf Aurora light effect",
            "chat_command_costs": 0,
            "chat_command_cooldown": 5,
            "chat_command_onCooldown": "$username, the command is still on cooldown for $cd seconds!",
            "chat_command_usercooldown": 5,
            "chat_command_onUserCooldown": "$username the command is still on user cooldown for $cd seconds!",
            "chat_command_responseNotEnoughPoints": "It seems $username has not enough $currency to play the game."
        }
    return

def Execute(data):
    global settings, userId, username, ScriptName

    naecEvent = {
        "effect_default": settings["default_effect"],
        "effect_new": settings["default_effect"],
        "effect_duration": settings["chat_command_default_effect_duration"],
        "effect_parameter": ""
    }

    if data.IsChatMessage() and data.GetParam(0).lower() == settings["chat_command"] and Parent.HasPermission(data.User, settings["chat_command_permission"], ""):
        tempResponseString = ""
        userId = data.User			
        username = data.UserName
        cd = ""

        effect_new = ""
        for x in range(1, data.GetParamCount()):
            if x == data.GetParamCount()-1:
                try:
                    naecEvent["effect_duration"] = int(data.GetParam(x))
                except:
                    pass
            else:
                effect_new += data.GetParam(x) + " "
        effect_new = effect_new.strip()
        if effect_new != "":
            naecEvent["effect_new"] = effect_new
			   
        # Check if the User has enough points
        if settings["chat_command_costs"] > Parent.GetPoints(userId):
            tempResponseString = settings["chat_command_responseNotEnoughPoints"]
            tempResponseString = tempResponseString.replace("$currency", str(Parent.GetCurrencyName()))
        # Check if there is a cooldown active 
        elif settings["chat_command_usercooldown"] and (Parent.IsOnCooldown(ScriptName, settings["chat_command"]) or Parent.IsOnUserCooldown(ScriptName, settings["chat_command"], userId)):
            if Parent.GetCooldownDuration(ScriptName, settings["chat_command"]) > Parent.GetUserCooldownDuration(ScriptName, settings["chat_command"], userId):
                cd = Parent.GetCooldownDuration(ScriptName, settings["chat_command"])
                tempResponseString = settings["chat_command_onCooldown"]
            else:
                cd = Parent.GetUserCooldownDuration(ScriptName, settings["chat_command"], userId)
                tempResponseString = settings["chat_command_onUserCooldown"]
            tempResponseString = tempResponseString.replace("$cd", str(cd))
        else:
            Parent.RemovePoints(userId, username, settings["chat_command_costs"])

            # send effect change request
            Parent.BroadcastWsEvent("EVENT_NAEC", json.dumps(naecEvent, encoding='utf-8'))
            tempResponseString = settings["chat_command_onEvent"]

            Parent.AddUserCooldown(ScriptName, settings["chat_command"], userId, settings["chat_command_usercooldown"])
            Parent.AddCooldown(ScriptName, settings["chat_command"], settings["chat_command_cooldown"])

        tempResponseString = tempResponseString.replace("$username", str(username))
        tempResponseString = tempResponseString.replace("$user", str(username))
        Parent.SendStreamMessage(tempResponseString)
    return

def Tick():
    return
