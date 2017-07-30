__repo__ = "https://github.com/tsukle/twpy"
__license__ = """
Copyright (c) 2017 Emilis Tobulevicius
Modified version (c) 2017 Steven Smith
 - Removed bulky comments, colorama, database support

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
"""

import socket
import json
from time import sleep

s = socket.socket()

with open("settings.json") as data:
    opt = json.load(data)

def connect():
    s.connect(("irc.twitch.tv", 6667))
    s.send(("CAP REQ :twitch.tv/membership\r\n").encode())
    s.send(("CAP REQ :twitch.tv/commands\r\n").encode())
    s.send(("CAP REQ :twitch.tv/tags\r\n").encode())
    s.send(("PASS " + opt["authkey"] + "\r\n").encode())
    s.send(("NICK " + opt["username"] + "\r\n").encode())
    s.send(("JOIN #" + opt["channel"] + "\r\n").encode())
    return s

def chat():
    display = "".encode()
    con = connect()

    while True:
        display = con.recv(1024)
        display = display.decode()
        message = display.split("\n")
        display = display.encode()
        display = message.pop()

        for line in message:
            response = info(line)
            if(response["display-name"] == "twitch" or response["display-name"].lower() == opt["username"]):
                continue
            yield response

def send(message, sp = None):
    construct = "PRIVMSG #" + opt["channel"] + (" :/me " if sp else " :") + message + "\r\n"
    s.send((construct).encode())
    sleep(1.5)

def afk():
    construct = "PONG :tmi.twitch.tv\r\n"
    s.send((construct).encode())


def info(uin):
    if(uin.startswith("@badges")):
        info = {} #This will be returned eventually.

        inputSplit = uin.split(" ", 1)
        inputTags = inputSplit[0]
        inputOther = inputSplit[1]
        inputMessage = inputSplit[1].split(":")

        #This is a check to stop these messages from being sent to chat.
        if(":jtv MODE" in uin or "GLOBALUSERSTATE" in uin or "USERSTATE" in uin or "ROOMSTATE" in uin or "JOIN #" in uin or "tmi.twitch.tv 353" in uin or "tmi.twitch.tv 366" in uin):
            info["display-name"] = "twitch"
        
        elif(uin.startswith("PING")):
            afk()
        
        # Gets the message sent and the channel it was sent from.
        elif(len(inputMessage) >= 3):
            msgInit = ":".join(inputMessage[2:])
            message = msgInit.split("\r")[0]
            info["message"] = message

            if(message.startswith("ACTION")):
                info["action-message"] = True
            
            else:
                info["action-message"] = False

            chanInit = inputMessage[1]
            strSplit = chanInit.split(" ")
            chanTear = strSplit[2].split("#")
            channel = chanTear[1]
            info["channel"] = channel

        # Splits remaining tags into the dictionary so they can all be called.
        tags = inputTags.split(";")
        for i, t in enumerate(tags):
            obj = t.split("=")
            objTitle = obj[0]
            objValue = obj[1]
            info[objTitle] = objValue

            if(i >= len(tags) - 1):
                if(info["user-type"] == ""):
                    info["user-type"] = "all"
                    return info
                else:
                    return info

    else:
        info = {} #This gets returned.
        # Returns the display-name twitch as all of the messages are from the IRC connection. Dealt with later.
        inputSplit = uin.split(" ")

        info["message"] = ""
        info["channel"] = ""
        info["sent-ts"] = ""
        info["user-id"] = ""
        info["@badges"] = ""
        info["display-name"] = "twitch"
        info["mod"] = "0"
        info["subscriber"] = "0"
        info["user-type"] = ""
        
        return info
