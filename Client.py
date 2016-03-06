
############################################################################################################################################
#                                                       Client side of client to client communication                                         #

MYPORT = 8080                                          # port for client sever commuication 
IP_REQUEST_PORT = 9000                                 # Port for requesting server for its ip                    
IP_RECEVE_PORT = 7000                                  # port for receving the servers ip as respoce
host = ""
my = ""


import os,sys
import socket
import thread

def getmyip():                                                             #
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)               #
        s.connect(("10.0.1.1",8000))                                       # 
        myip = s.getsockname()[0]                                          #
        s.close()                                                          #
        return myip                                                        #


def dspMsg():                                        #
	while True:                                   #
		s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		s.bind(("",9090))         #
		data,addr = s.recvfrom(1024)          #  function used by a thread to display the msg sent from the client
		print ">>" + str(data)                #
		pass                                  #



def sendMsg():                                       #
	while True:                                   #
		message = raw_input("")
		s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)         #
		if message == "quit()":               #  function used by a thred to send the msg to the server
			s.close()                     #
			os._exit(1)                   #
		s.sendto(message,(host,MYPORT))       #
		pass                                  #



def getserver(name ):
	s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)         #
	s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)       #
	s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)     #
	s.sendto(name, ('<broadcast>', IP_REQUEST_PORT))            #
	s.close()                                                   #
	s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)         #
	s.bind(("",IP_RECEVE_PORT))                                 #this function broadcasts that it wants the ip of server , receves the 
	data = ""                                                   #ip when the server replyes and returns it .
	while not len(data):                                        #
		data, addr = s.recvfrom(1024)                       #
		pass                                                #
	print data                                                  #
	sip = addr[0]                                               #
	print sip                                                   #
	s.close()                                                   #
	return sip                                                  #



def main():
	
	name = raw_input("enter your name :")	
	thread.start_new_thread(dspMsg,()) #thread used for desplaying the msgs
	port = MYPORT
	host = getserver(name)
	my = getmyip()
	print "message formate : <username>:<message>"
	thread.start_new_thread(sendMsg,())#thread used for sending msgs
	while 1:
		pass



if __name__ == '__main__':
	main()
