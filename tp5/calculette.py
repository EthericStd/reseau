import socket
import sys
import threading


HOST = '0.0.0.0'
PORT = 2004

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
	s.bind((HOST, PORT))
except socket.error as msg:
	print("Bind failed. Error Code : " + str(msg[0]) + " Message " + msg[1])
	sys.exit()
s.listen(10)

print("Serveur en écoute sur " + HOST + ":" + str(PORT))


# Cette fonction sera utilisée dans les threads qui traiteront les connections
def clientthread(conn):
	conn.send(("Hello from " + HOST + ":" + str(PORT) + "\n").encode('UTF-8'))
	l=[]
	while True:
		n=len(l)
		data = conn.recv(1024).decode('UTF-8').upper().strip()
		reply1=None
		if data == "ADD":
			l[n-2]=l[n-1]+l[n-2]
			l.pop(n-1)
		elif data == "MUL":
			l[n-2]=l[n-1]*l[n-2]
			l.pop(n-1)
		elif data == "DIV":
			l[n-2]=l[n-1]/l[n-2]
			l.pop(n-1)
		elif data == "MOD":
			l[n-2]=l[n-1]%l[n-2]
			l.pop(n-1)
		
		elif data == "LIST":
			reply1=str(l)
			
		elif data == "POP":
			reply1=str(l[n-1])
			l.pop(n-1)
		
		elif data == "FIN" or data.strip() == "":
			print(data)
			break
		
		else:
			l+=[int(data)]
		
		if reply1 != None:
			reply1+="\n"
			conn.sendall(reply1.encode('UTF-8'))
	conn.close()

# La boucle d'attente des connexions
while True:
	try:
		conn, addr = s.accept()
		print('Connection de ' + addr[0] + ':' + str(addr[1]))

		t = threading.Thread(None, clientthread, None, (conn,), {})
		t.start()

	except KeyboardInterrupt:
		print("Stop.\n")
		break

s.close()
