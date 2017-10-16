#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket
import struct
import time

socketTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(1)
socketTCP.connect(("145.238.203.10", 123))
print(1)
n=socketTCP.recv()
print(1)
t = struct.unpack('I', n)       #retourne un tuple de 4 octets convertis en entiers non signés
print(t[0])
t = socket.ntohl(t[0])                  #convertion du standard réseau vers l'hôte
print(t)
print(time.ctime(t - 2208988800))       #on fait en sorte que ça affiche le nombre de secondes depuis le 1er janvier 1970
socketTCP.close()
