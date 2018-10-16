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
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
awshost = "18.222.162.68"
awsport = 2738
host = "127.0.0.1"
port = 5000

print (host)
print (port)
#client.connect(socket_path)
#client.send(b'python connected')
serversocket.bind((host, port))
serversocket.listen(5)
socket.connect((awshost, awsport))

print("socket listening")

#accept connections from outside
print("waiting for client to connect")
(clientsocket, address) = serversocket.accept()
print("client accepted. yayayayayayay")
text = clientsocket.recv(1024)
print("received from client: ", text)

def EncodeWebSockSend(socket, data):
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

#TEMPORARY CODE USED TO GENERATE PREDICTABLE OUTPUT COORDINATES
#node1 = [0, 0]
#node2 = [1, 0]
#node3 = [2, 0]
#node4 = [3, 0]
#nodes = [node1, node2, node3, node4]
#t = 0
##########

#while 1:
    #TEMPORARY CODE USED TO GENERATE PREDICTABLE OUTPUT COORDINATES
#    randNode = random.randint(0,3)
#    randDest = random.randint(0,3)
#    randCons = random.randint(0,10)
#    cons = 0
#    if randCons >= 7:
#        cons = 1
#    t = t + 1
#    dest = [randDest, t]
#    out = str(nodes[randNode][0]) + ";" + str(nodes[randNode][1]) + ";"
#    nodes[randNode] = dest
#    out = out + str(nodes[randNode][0]) + ";" + str(nodes[randNode][1]) + ";" + str(cons)
#    print(out)
#    EncodeWebSockSend(clientsocket, out)
###############

while 1:
    txt = socket.recv(2048) #"" + str(parentx) + ";" + str(parenty) + ";" + str(nodex) + ";"+str(nodey)+";1"
    print txt;
    contents = txt.split("\n");
    for cont in contents:
            EncodeWebSockSend(clientsocket, cont)
    #clientsocket.send('hello from server')
    print("-----------hello from server sent-------------")
    time.sleep(0.5)

print("done")
