############################################################################################################################################
#                                                       Server side of client to Client communication                                         #


IP_REQUEST_PORT = 9000                                           # port used for accepting client's request for server's ip
IP_SEND_PORT = 7000	                                         # port used for sending servers ip
MYPORT = 8080                                                    # port for server client communication
NoClients =  3                                                   # number of clients which server accept
lis=[]                                                           # List of all client's sockets which are connected to server
users = {}
host = ''


import sys,os
import socket 
import thread


def sendip():
	while True:
		s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)        #  
		s.bind(("",IP_REQUEST_PORT))                               #  
		data = ""                                                  #
		while not len(data):                                       #  Server Waiting For the request from the client for it's IP
			data, addr = s.recvfrom(1024)                      #
		print data                                                 #
		users[data]=addr[0]
		lis.append(addr[0])
		s.close()


		s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)        #
		s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)	   #
		s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)    #  server replying the client with its ip
		s.sendto("server my ip:", ('<broadcast>', IP_SEND_PORT))   #
		s.close()                                                  #
		pass                                                       #

		for ip in lis:
			msg = "the list of users is \n"                                                  #
			c = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #  
			for  name,ip in users.items():
				msg+= name +" "+ip+"\n"
			c.sendto(msg,(ip,9090))
			c.close()



def dspMsg():                                                             #
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.bind((host,MYPORT))               #
	while True:             
		data,addr = s.recvfrom(1024)                                        #
		print " >>"+ str(data)
		if len(data):
			sendMsg(data) 


def sendMsg(data):                                    #
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	l = data.split(":")
	msg = "message from " + l[0] + ":" + l[1]
	s.sendto(msg,(users[l[0]],9090))                                      #



                                                             #
		                                      #    connected to the server


def getmyip():                                                             #
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)               #
	s.connect(("10.0.1.1",8000))                                       # finds the servers ip and returns it
	myip = s.getsockname()[0]                                          #
	s.close()                                                          #
	return myip                                                        #


def Main():
	thread.start_new_thread(sendip,()) #Thread which runs sendip function
	host = getmyip()
	thread.start_new_thread(dspMsg,()) #Thread which runs dspMsg function
	while 1:
		pass	
	

if __name__ == '__main__':   
	Main()
