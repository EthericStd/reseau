import socket
import select
import sys
import queue
import threading

def add_input(input_queue):
	while True:
		input_queue.put(sys.stdin.read(1))
		

def insert(index, sequence):
	if sequence==[]:
		return [index]
	elif index<=sequence[0]:
		return [index] + sequence
	else:
		return [sequence[0]] + insert(index, sequence[1:len(sequence)])


def merge(subSequence1,subSequence2):
	if subSequence1==[]:
		return subSequence2
	elif subSequence2==[]:
		return subSequence1
	else:
		return merge(subSequence1[1:len(subSequence1)],insert(subSequence1[0], subSequence2))


def mergeSort(sequence):
	n=len(sequence)
	if len(sequence)==0 or len(sequence)==1:
		return sequence
	else:
		return merge(mergeSort(sequence[0:n//2]),mergeSort(sequence[n//2:n]))


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


msg=msg[3:-1]
t=msg.split(',')
i=0
N=len(t)
while i<N:
	t[i]=int(t[i])
	i+=1

t=mergeSort(t)
msg=str(t).encode()
client.send(msg)



client.close()
