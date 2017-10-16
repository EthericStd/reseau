#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket

socketFTP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketFTP.connect(("192.168.56.101", 21))
etat = 0

for line in socketFTP.makefile('r'):   
    if ((etat == 0) and line.startswith("220")):
        s.send("USER user\n".encode('UTF-8'))
        etat = 1
    elif ((etat == 1) and line.startswith("331")):
        s.send("PASS user\n".encode('UTF-8'))
        etat = 2
    elif ((etat == 2) and line.startswith("230 User logged in")):			#On précise car il peut y avoir plusieurs phrases.
        s.send("SYST\n".encode('UTF-8'))
        etat = 3
    elif (etat == 3):
        print(line)
        s.send("QUIT\n".encode('UTF-8'))		#On affiche le résultat et on quitte.
s.close()
