############################################################################################################################################
#                                                       Server side of client to Client communication                                         #


IP_REQUEST_PORT = 9000                                           # port used for accepting client's request for server's ip
IP_SEND_PORT = 7000	                                         # port used for sending servers ip
MYPORT = 8080                                                    # port for reciving msgs from client
SENDPORT = 9090                                                  # port for sending msgs to clients
lis=[]                                                           # List of all client's sockets which are connected to server
users = {}                                                       # dictinory of all users and there ip's
host = ''


import sys,os
import socket 
import thread


def sendip():
	global lis
	global users
	global host
	while True:
		s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)        #  
		s.bind(("0.0.0.0",IP_REQUEST_PORT))                        #  
		data = ""                                                  #
		data, addr = s.recvfrom(1024)                   	   #
		print data , addr                                          #
		users[data]=addr[0] #adding a user to the dictionary                         
		lis.append(addr[0])
		s.close()


		s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)        #
		s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)	   #
		s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)    #  server replying the client with its ip
		s.sendto("server my ip:", ('<broadcast>', IP_SEND_PORT))   #
		s.close()                                                  #
		pass                                                       #
		c = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #

		##### Server gives  all the users the updated user list #######  
		msg = "List of users ->\n"
		for  name,ip in users.items():
			msg+= name +" "+ip+"\n"
		for ip in lis:													
			print ip
			print "sending message to %s"%ip
			c.sendto(msg,(ip,SENDPORT))

		c.close()

##### Server receves the msge from the client and forwords it to the respective client based on the username given #####

def dspMsg(): 
	global MYPORT
	global lis
	global users
	global host
                                                            #
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.bind(("0.0.0.0",MYPORT)) 	                                  #
	while True:             
		data,addr = s.recvfrom(1024)
		print data                                                #
		if len(data):
			sendMsg(data,addr[0]) 


def sendMsg(data,addr):                                                   #
	global lis
	global users
	global host
	print " >>"+ str(data)
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	l = data.split(":")
	if users[l[0]] in lis:
		msg = "message :" + l[1]
		s.sendto(msg,(users[l[0]],SENDPORT))
	s.close()                                                         #



                                                       
		                                       


def getmyip():                                                             #
	global lis
	global users
	global host
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)               #
	s.connect(("10.0.1.1",8000))                                       # finds the servers ip and returns it
	myip = s.getsockname()[0]                                          #
	s.close()                                                          #
	return myip                                                        #


def Main():
	global lis
	global users
	global host
	thread.start_new_thread(sendip,()) #Thread which runs sendip function
	host = getmyip()
	thread.start_new_thread(dspMsg,()) #Thread which runs dspMsg function
	while 1:
		pass	
	

if __name__ == '__main__':   
	Main()
