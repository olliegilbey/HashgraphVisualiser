# server.py 
import socket                                         
import time

# create a socket object
serversocket = socket.socket(
	        socket.AF_INET, socket.SOCK_STREAM) 

# get local machine name
host = socket.gethostname()                           
print host
port = 8000
# bind to the port
serversocket.bind((host, port))                                  
print "binded"
# queue up to 5 requestis
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.listen(5)                                           
print "While"
while True:
    # establish a connection
    print "before con"
    clientsocket,addr = serversocket.accept()      
    print "aft con"
    print("Got a connection from %s" % str(addr))
    currentTime = time.ctime(time.time()) + "\r\n"
    clientsocket.send(currentTime.encode('ascii'))
    clientsocket.close()
