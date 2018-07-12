#################
Info
#################
Description: Nanoleaf Aurora Effect Changer for Streamlabs Chatbot
Created by: CyberHumi - twitch.tv/CyberHumi, twitter.com/CyberHumiDE
Version: 1.1


################
Usage (Windows)
################
(1) Download the current Streamlabs Chatbot version: https://streamlabs.com/chatbot

(2) Download and install Python 2.7.13 since that's needed for Chatbot and the Script features: 
    https://www.python.org/ftp/python/2.7.13/python-2.7.13.msi 

(3) Open the Streamlabs Chatbot and go to the "Scripts" tab in the left sidebar.
    Click on the cogwheel in the top right and set your Python directory to the `Lib` folder where you installed Python 
    (By default it should be `C:\Python27\Lib`).

(4.1) Download and install Python 3.6 or newer for nanoleaf interface:
      https://www.python.org/ftp/python/3.6.0/python-3.6.0-amd64.exe
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

(6) Copy the "NA Effect Changer" script you want to use into the folder from the SL Chatbot. You can also use the Import function per button on the top right in the "Scripts" tab.
   (By default it should be `C:\Users\<Username>\AppData\Roaming\Streamlabs\Streamlabs Chatbot\Services\Scripts`)

(7) Go back to the "Scripts" tab in SL Chatbot and rightclick the background and click "Reload Scripts".
    Afterwards the list of installed scripts should appear and you can start configuring those.

(8) Rightclick on the "NA Effect Changer" script and click "Insert API Key".
	
(9) Customize "NA Effect Changer" parameters.
    Insert Nanoleaf Aurora IP and token from step 5.
	(Configure the Nanoleaf Aurora effects with your Android or iOS app)
	Insert effect name and effect duration under the event which should trigger the effect change.

(10) Go back to the `Scripts` tab in Chatbot and rightclick the background and click "Reload Scripts" again.

(11) Execute NAEC_WSclient.bat while Streamlabs Chatbot is running. Do not close the Command Prompt window.


###############
Version History
###############
1.0:
  ~ First Release version
1.1:
  ~ add Chat command
    chatCmd effectName [durationInSeconds]
	e.g. !naec Daylight
	     !naec Color Burst 10


###############
FAQ
###############
Q: How can I change the effect permanently?
A: Set the duration to '0'

Q: The Event Log shows 'Error 404: Resource not found!'
A: Check the effect name. The effect must exist on your Nanoleaf Aurora. The name is case-sensitive!


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
