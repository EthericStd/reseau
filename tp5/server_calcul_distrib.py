import socket
import select

connections=[]
host="0.0.0.0"
port=5000
	
			
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(10)

print("Server started on port : {}".format(port))

wait_go=True
while wait_go:
	r, w, e = select.select([server], [], [], 0.05)
	for s in r:
		client, addr=s.accept()
		connections+=[client]
		
	r, w, e = select.select(connections, [], [], 0.05)
	for s in r:
		try:
			msg=s.recv(1024)
		except:
			s.close()
		if msg.decode().strip().upper()=="GO":
			wait_go=False

	
for i,s in enumerate(connections):
	msg="go"+str(100*i)
	s.send(msg.encode())

summ=0
nb_error=0
for s in connections:
	try:
		msg=s.recv(1024)
	except:
		s.close()
		nb_error+=1
	msg=msg.decode().strip()
	summ+=float(msg)

print("Somme des racines de 1 à {} = {}".format(len(connections)*100, summ) )
print("{} client(s) n'a/n'ont pas repondu(s)".format(nb_error))
server.close()
