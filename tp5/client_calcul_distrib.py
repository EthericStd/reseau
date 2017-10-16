import socket
import select
import math
import sys
import queue
import threading

def add_input(input_queue):
	while True:
		input_queue.put(sys.stdin.read(1))

input_queue=queue.Queue()
t=threading.Thread(target=add_input, args=(input_queue,))
t.deamon=True
t.start()


host="0.0.0.0"
port=5000
	
			
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

print("Connected on port : ".format(port))

c=""
j=0
wait_go=True
while wait_go:
	r, w, e = select.select([client], [], [], 0.05)
	for s in r:
		try:
			msg=s.recv(1024)
		except:
			s.close()
		msg=msg.decode().strip().upper()
		if msg[:2]=="GO":
			wait_go=False
	if not input_queue.empty():
		j+=1
		c+=input_queue.get()
		if j==1 and c!="g":
			c=""
			j=0
		if j==2 and c=="go":
			client.send(c.encode())

k=int(msg[2:])
h=k+100
if k==0:
	k=1
	h=100
summ=0
for i in range(k,h):
	summ+=math.sqrt(i)

msg=str(summ).encode()
client.send(msg)



client.close()
