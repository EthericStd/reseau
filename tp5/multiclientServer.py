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

	while True:
		data = conn.recv(1024).decode('UTF-8')
		reply = 'Recu: ' + data
		if data.upper().strip() == "DATA":
			l=[]
			data1 = conn.recv(1024).decode('UTF-8')
			while data1.strip()!="":
				l+=[int(data1)]
				data1 = conn.recv(1024).decode('UTF-8')
				
		elif data.upper().strip() == "SUM":
			reply1=str(sum(l))
			conn.sendall(reply1.encode('UTF-8'))
			
		elif data.upper().strip() == "MIN":
			reply1=str(min(l))
			conn.sendall(reply1.encode('UTF-8'))
		
		elif data.upper().strip() == "MAX":
			reply1=str(max(l))
			conn.sendall(reply1.encode('UTF-8'))
		
		elif data[:4].upper().strip() == "HEAD":
			reply1=str(l[:int(data[5])])
			conn.sendall(reply1.encode('UTF-8'))
			
		elif data[:4].upper().strip() == "TAIL":
			reply1=str(l[int(data[5])+1:])
			conn.sendall(reply1.encode('UTF-8'))
		
		elif data[:8].upper().strip() == "INTERVAL":
			reply1=str(l[int(data[9])+1:int(data[11])])
			conn.sendall(reply1.encode('UTF-8'))
		
		elif data.upper().strip() == "FIN" or data.strip() == "":
			print(data)
			break

		conn.sendall(reply.encode('UTF-8'))
	print(2)
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
