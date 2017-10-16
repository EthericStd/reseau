import socket
import select
import random


def cut(t, n):
	indexs=[0]
	N=len(t)
	for i in range(n):
		indexs+=[(N//n)*(i+1)]
	m=len(t)%n
	for i in range(m):
		for i in range(i+1,n+1):
			indexs[i]+=1
	tab=[]
	for i in range(len(indexs)-1):
		tab+=[t[indexs[i]:indexs[i+1]]]
		j=i
	return tab


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


t=[]
for i in range(100):
	t+=[random.randrange(99)]
print("la liste non triee : {}".format(t))

t=cut(t, len(connections))
for i,s in enumerate(connections):
	msg="go"+str(t[i])
	print("on envoie : {}".format(t[i]))
	s.send(msg.encode())

tab=[]
nb_error=0
for s in connections:
	try:
		msg=s.recv(1024)
	except:
		s.close()
		nb_error+=1
	msg=msg.decode().strip()
	msg=msg[3:-1]
	t=msg.split(',')
	i=0
	N=len(t)
	while i<N:
		t[i]=int(t[i])
		i+=1
	tab+=[t]

for i in range(1, len(tab)):
	tab[0]=merge(tab[0], tab[i])

print("La liste triee : {}".format(tab[0]))
print("{} client(s) n'a/n'ont pas repondu(s)".format(nb_error))
server.close()
