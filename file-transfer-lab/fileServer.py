#! /usr/bin/env python3

import sys

sys.path.append("../lib")  # for params
import re, socket, params, os

switchesVarDefaults = (
    (('-l', '--listenPort'), 'listenPort', 50001),
    (('-d', '--debug'), "debug", False),  # boolean (set if present)
    (('-?', '--usage'), "usage", False),  # boolean (set if present)
)

progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # listener socket
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("listening on:", bindAddr)
os.chdir("./ServerFiles")

while True:
    sock, addr = lsock.accept()

    from framedSock import framedSend, framedReceive

    file = (framedReceive(sock, debug)).decode()
    fileName, fileSize = file.split(":")
    fileSize = int(fileSize)

    if not os.fork():
        print("new child process handling connection from", addr)

        while True:
            with open(fileName, "w+b") as newFile:
                count = 0
                while count < fileSize:
                    payload = framedReceive(sock, debug)
                    data = bytes(payload)

                    if payload == b'':
                        break

                    newFile.write(data)
                    count += 1
            newFile.close()
            if debug: print("rec'd: ", payload)

            if payload is b'':
                print("The file was received")

            sys.exit(0)