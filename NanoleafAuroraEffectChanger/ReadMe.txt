#################
Info
#################
Description: Nanoleaf Aurora Effect Changer for Streamlabs Chatbot
Created by: CyberHumi - www.twitch.tv/CyberHumi, www.twitter.com/CyberHumiDE
Version: 1.6.1


################
Usage (Windows)
################
https://github.com/CyberHumi/Chatbot-Scripts/wiki/Installation

(1) Download the current Streamlabs Chatbot version: https://streamlabs.com/chatbot

(2) Download and install Python 2.7.13 since that's needed for Chatbot and the Script features:
    https://www.python.org/ftp/python/2.7.13/python-2.7.13.msi

(3) Open the Streamlabs Chatbot and go to the "Scripts" tab in the left sidebar.
    Click on the cogwheel in the top right and set your Python directory to the `Lib` folder where you installed Python
    (By default it should be `C:\Python27\Lib`).

(4.1) Download and install Python 3.6 or newer for nanoleaf interface:
      https://www.python.org/downloads/
(4.2) Download and install nanoleaf interface (C:\Python36\Scripts\pip install nanoleaf --upgrade)
      If necessary upgrade pip (C:\Python36\python -m pip install --upgrade pip)
(4.3) Download and install websocket-client (C:\Python36\Scripts\pip install websocket-client)

(5) Get a Nanoleaf Aurora auth. token:
    Start -> Python 3.6 -> IDLE (Python 3.6 64-bit)

    >>> from nanoleaf import setup
    >>> ipAddressList = setup.find_auroras()
    >>> print(ipAddressList)
    ['192.168.x.y']

    Press and hold the Nanoleaf Aurora power button for 5-7 seconds first! (Light will begin flashing)

    >>> token = setup.generate_auth_token("192.168.x.y")
    >>> print(token)
    nnnnnnnnnnnnnnnnnnnnnnnnn

    Note the IP and token. You need them later.
    Repeat this step for a 2nd Nanoleaf device.

(6) Import the "NA Effect Changer" script into the SL Chatbot. You can use the Import function per button on the top right in the "Scripts" tab.
   (By default it should be `C:\Users\<Username>\AppData\Roaming\Streamlabs\Streamlabs Chatbot\Services\Scripts`)

(7) Go back to the "Scripts" tab in SL Chatbot and rightclick the background and click "Reload Scripts".
    Afterwards the list of installed scripts should appear and you can start configuring those.

(8) Rightclick on the "NA Effect Changer" script and click "Insert API Key".

(9) Customize "NA Effect Changer" parameters.
    Insert Nanoleaf Aurora IP and token from step 5.
    Insert Python3 installation directory. (By default it should be `C:\Python36`)
    (Configure the Nanoleaf Aurora effects with your Android or iOS app)
    Insert effect name and effect duration under the event which should trigger the effect change.

(10) Go back to the `Scripts` tab in Chatbot and rightclick the background and click "Reload Scripts" again.
     This generates the file NAEC_SLCB_CLIENT.bat. You can find it in the script folder.

(11) Execute NAEC_SLCB_CLIENT.bat while Streamlabs Chatbot is running. Do not close the Command Prompt window.


###############
Version History
###############
1.0:
  ~ First Release version
1.1:
  ~ add Chat command
    chatCmd effectName [durationInSeconds]
    e.g. !nl Flames
         !nl Color Burst 10
1.2:
  ~ add YT sub, MX sub, MX follow and MX host support
1.2.1:
  ~ fix encoding issue
1.3:
  ~ add max. duration for chat command
  ~ add min. viewers for host event
  ~ add min. bits for cheer event
  ~ add automatic settings reload after update
  ~ remove Raid from UI (is not yet implementet in SLCB)
1.3.1:
  ~ fix chat command with 0 cost
1.4:
  ~ hotfix, prevents deadlock between NAEC.py and SLCB by using a msg queue and a seperate thread for Nanoleaf actions
1.4.1:
  ~ fix problem when generating new NAEC_SLCB_CLIENT.bat
1.5:
  ~ add 2nd Nanoleaf Aurora device support
  ~ fix host and cheer alert (wrong variable name)
1.5.1
  ~ add Weblinks
1.6
  ~ add additional chat commands option
1.6.1
  ~ fix 10th additional chat command


###############
FAQ
###############
Q: Why do I need Python version 2.7 and version 3.6?
A: Streamlabs Chatbot is only compatible with Python 2.7, no other version is compatible with the IronPython which is used by the chatbot.
   The nanoleaf interface has been developed under Python 3. Unfortunately the interface is not backward compatible to Python version 2.7.

Q: How can I change the effect permanently?
A: Set the duration to '0'

Q: The Event Log shows 'Error 404: Resource not found!'
A: Check the effect name. The effect must exist on your Nanoleaf Aurora. The name is case-sensitive!
   Doesn't work with "Basic" scenes.

Q: On step 5 I got the following message: 'OSError: [WinError 10013] An attempt was made to access a socket in a way forbidden by its access permissions'
A: Check your firewall settings. The communication to the Nanoleafs occur via port 16021.

Q: I get the following message:
   "HTTPConnectionPool(host='192.168.x.y', port=16021): Max retries exceeded with url: /api/v1//state
   (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x0000017EB352A128>: Failed to establish a new connection: [Errno 11001] getaddrinfo failed'))"
A: The connection token is wrong or missing.

Q: SLCB crashes when I use this script. What can I do?
A; Clear the SLCB cache directory.


###############
License
###############
MIT License

Copyright (c) 2018 CyberHumi - www.twitch.tv/CyberHumi
Original version at: https://github.com/CyberHumi/Chatbot-Scripts

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
