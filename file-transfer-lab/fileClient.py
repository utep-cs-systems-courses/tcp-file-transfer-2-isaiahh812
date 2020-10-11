#! /usr/bin/env python3

import socket, sys, re, os

sys.path.append("../lib")  # for params
import params

from framedSock import framedSend, framedReceive


switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--debug'), "debug", False),  # boolean (set if present)
    (('-?', '--usage'), "usage", False),  # boolean (set if present)

)

progname = "framedClient"



paramMap = params.parseParams(switchesVarDefaults)
server, usage, debug = paramMap["server"], paramMap["usage"], paramMap["debug"]

if usage:
    params.usage()


serverHost, serverPort = re.split(":", server)
serverPort = int(serverPort)



fileName = input("Enter the file name: ")

addrFamily = socket.AF_INET
socktype = socket.SOCK_STREAM
addrPort = (serverHost, serverPort)

s = socket.socket(addrFamily, socktype)

if s is None:
    print('could not open socket')
    sys.exit(1)

s.connect(addrPort)

try:

    fileSize = os.path.getsize(fileName)

    if fileSize == 0:
        print("The file you inputed is empty")

    fileSize = str(fileSize)
    info = ((fileName + ":" + fileSize).encode())
    framedSend(s, info, debug)

    with open(fileName, "rb") as sentFile:
        for data in fileName:
            data = sentFile.read(1024)

            if data == "":
                break
            framedSend(s, data, debug)
    print("file has been sent")
except FileNotFoundError:
    print("The file doesn't exist")
