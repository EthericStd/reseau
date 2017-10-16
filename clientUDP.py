#!/usr/bin/python
# -*- coding: utf-8 -*-
 
import socket
import struct

adresse=("lsis.univ-tln.fr",37)
socketUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# envoi de la requête au serveur
requete = struct.pack("x")
socketUDP.sendto(requete, adresse)
# réception et affichage de la réponse
rep, addr = socketUDP.recvfrom(4)
t = struct.unpack('I', rep)           #retourne un tuple de 4 octets convertis en entiers non signés
print(t[0])
t = socket.ntohl(t[0])                  #convertion du standard réseau vers l'hôte
print(t)
print(time.ctime(t - 2208988800))       #on fait en sorte que ça affiche le nombre de secondes depuis le 1er janvier 1970

# fermeture de la connexion
socketUDP.close()
print ("fin du client UDP")
