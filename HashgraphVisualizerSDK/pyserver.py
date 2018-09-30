import socket
import random
from threading import *
import re
from base64 import b64encode
from hashlib import sha1
import time
#
# @see
# https://stackoverflow.com/questions/21233340/sending-string-via-socket-python
# @see
# https://stackoverflow.com/questions/10152290/python-websocket-handshake-rfc-6455
#socket_path = '/tmp/node-python-sock'

websocket_answer = (
        'HTTP/1.1 101 Switching Protocols',
        'Upgrade: websocket',
        'Connection: Upgrade',
        'Sec-WebSocket-Accept: {key}\r\n\r\n',
)

GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "127.0.0.1"
port = 5000

print (host)
print (port)
#client.connect(socket_path)
#client.send(b'python connected')

serversocket.bind((host, port))
serversocket.listen(5)
print("socket listening")

#accept connections from outside
print("waiting for client to connect")
(clientsocket, address) = serversocket.accept()
print("client accepted. yayayayayayay")
text = clientsocket.recv(1024)
print("received from client: ", text)

def EncodeWebSockSend(socket,data):
    bytesFormatted = bytearray()
    bytesFormatted.append(0x81) #129 in decimal, indicates text format
    print("bytesFormatted", bytesFormatted)
    bytesRaw = data.encode()
    print("bytesRaw of text", bytesRaw)
    bytesLength = len(bytesRaw)
    if bytesLength <= 125 :
        bytesFormatted.append(bytesLength)
    elif bytesLength >= 126 and bytesLength <= 65535 :
        bytesFormatted.append(126)
        bytesFormatted.append(( bytesLength >> 8 ) & 255 )
        bytesFormatted.append(bytesLength & 255 )
    else :
        bytesFormatted.append(127)
        bytesFormatted.append( ( bytesLength >> 56 ) & 255 )
        bytesFormatted.append( ( bytesLength >> 48 ) & 255 )
        bytesFormatted.append( ( bytesLength >> 40 ) & 255 )
        bytesFormatted.append( ( bytesLength >> 32 ) & 255 )
        bytesFormatted.append( ( bytesLength >> 24 ) & 255 )
        bytesFormatted.append( ( bytesLength >> 16 ) & 255 )
        bytesFormatted.append( ( bytesLength >>  8 ) & 255 )
        bytesFormatted.append( bytesLength & 255 )

    #bytesFormatted = bytes(bytesFormatted)
    bytesFormatted.extend(data)
    print("bytesFormatted", bytesFormatted)
    socket.send(bytesFormatted) 

key = (re.search('Sec-WebSocket-Key:\s+(.*?)[\n\r]+', text)
    .groups()[0]
    .strip())

response_key = b64encode(sha1(key + GUID).digest())
response = '\r\n'.join(websocket_answer).format(key=response_key)

print response
clientsocket.send(response)
print("------------response sent -----------")

# on open reply
print("------------Received from Client: ---------------")
print clientsocket.recv(1024)
 
parentx = 1
parenty = 0
while 1:
    nodex = random.randint(1,5)
    nodey = parenty + 1
    txt = "" + str(parentx) + ";" + str(parenty) + ";" + str(nodex) + ";"+str(nodey)
    EncodeWebSockSend(clientsocket, txt)
    parentx = nodex;
    parenty = nodey;
    #clientsocket.send('hello from server')
    print("-----------hello from server sent-------------")
    time.sleep(1)
#while 1:
    #print("running")
    #now do something with the clientsocket
    #in this case, we'll pretend this is a threaded server
#    serversocket.send(b'Something sent')
    #client.send('some message')
    #serversocket.emit('connection')
    #serversocket.flush()
#    print('something sent')

#client.close()
print("done")
