import socket
import select

CONNECTION_LIST = {}
RECV_BUFFER = 4096
HOST = "0.0.0.0"
PORT = 5000


def broadcastToClients(the_sock, message):
	print(message)
	message+="\n"
	for sock in CONNECTION_LIST.values():
		if sock != server_socket and sock != the_sock:
			sock.send(message.encode('UTF-8'))


def get2ndspace(data):
	ctr=0
	for i,w in enumerate(data):
		if w==" ":
			ctr+=1
			if ctr==2:
				return i
	return 4
			
			
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(10)

CONNECTION_LIST[0]=server_socket

print("Chat server started " + HOST + ":" + str(PORT))

d_nick={}

while 1:
	try:
		read_sockets, write_sockets, error_sockets = select.select(CONNECTION_LIST.values(), [], [])

		for sock in read_sockets:
			if sock == server_socket:
				sockfd, addr = server_socket.accept()
				CONNECTION_LIST[addr]=sockfd
				msg="Client "+str(sockfd.getpeername())+" connected"
				broadcastToClients(sockfd, msg)

			else:
				try:
					data = sock.recv(RECV_BUFFER).decode('UTF-8').strip()
					if data:
						if data.upper()[:8]=="NICKNAME":
							if CONNECTION_LIST.__contains__(data[9:]):
								sock.send("The nickname is actually reserved\n".encode('UTF-8'))
							else:
								d_nick[sock.getpeername()]=data[9:]
								CONNECTION_LIST[data[9:]]=CONNECTION_LIST[sock.getpeername()]
								CONNECTION_LIST.__delitem__(sock.getpeername())
						elif data.upper()[:3]=="MSG":
							i=get2ndspace(data)
							if CONNECTION_LIST.__contains__(data[4:i]):
								if d_nick.__contains__(sock.getpeername()):
									msg=d_nick[sock.getpeername()]+" whisper to you :"+data[i:]+"\n"
								else:
									msg="("+ sock.getpeername()[0]+", "+str(sock.getpeername()[1])+")"+" whisper to you :"+data[i:]+"\n"
								CONNECTION_LIST[data[4:i]].send(msg.encode('UTF-8'))
							else:
								sock.send("The nickname doesn't exist\n".encode('UTF-8'))
						else:
							if d_nick.__contains__(sock.getpeername()):
								broadcastToClients(sock, d_nick[sock.getpeername()]+" : "+data)
							else:
								addr="("+ sock.getpeername()[0]+", "+str(sock.getpeername()[1])+")"
								broadcastToClients(sock, addr+" : "+data)

				except:
					if d_nick.__contains__(sock.getpeername()):
						msg="Client "+d_nick[sock.getpeername()]+" is offline"
						CONNECTION_LIST.__delitem__(d_nick[sock.getpeername()])
						d_nick.__delitem__(sock.getpeername())
						
					else:
						msg="Client "+"("+ sock.getpeername()[0]+", "+str(sock.getpeername()[1])+")"+" is offline"
						CONNECTION_LIST.__delitem__(sock.getpeername())
					
					broadcastToClients(sock, msg)	
					sock.close()
					continue

	except KeyboardInterrupt:
		print("Stop.")
		break

server_socket.close()
