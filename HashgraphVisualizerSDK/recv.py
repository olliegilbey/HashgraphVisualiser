import socket
import dummy as visualiser
from flask import Flask, render_template
import dynamicgraph

app = Flask(__name__)

@app.route('/test')
def charTest(sx, sy, rx, ry):
    d = dynamicgraph.DynamicUpdate()
    d()

    graphJSON = ""
    graphJSON = d.update(sx, sy)
    graphJSON = d.update(rx, ry)

    print graphJSON

    return render_template('untitled.html', name = 'Live Visualizer',
            graphJSON = graphJSON)

def receivePackets():
    TCP_IP = 'localhost'
    TCP_PORT = 54321
    BUFFER_SIZE = 4096  # Normally 1024, but we want fast response

    print "Client Started"
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transactions = []
    print "Waiting for connection..."
    #s.listen(1)
    while 1:
        try:
            s.connect((TCP_IP, TCP_PORT))
            print "Connected!"
            #app.run(debug = True)
            data = s.recv(BUFFER_SIZE)
            while data:
                packet = data.split("\n")
                for p in packet:
                    if p == "":
                        packet.remove(p)
#                    else:
             #           print p
                data  = s.recv(BUFFER_SIZE)
                sid = 0
                sic = 0
                rid = 0
                ric = 0
                for r in packet:
                    raw = r.split(",")
                    for i  in range(0, 6):
                        if i == 1:
                            m = raw[i].split(":")
                            sic = m[1]
                        elif i == 2:
                            m = raw[i].split(":")
                            ric = m[1]
                        elif i == 4:
                            m = raw[i].split(":")
                            sid = m[1]
                        elif i == 5:
                            m = raw[i].split(":")
                            rid = m[1]
                            rid = rid.replace("}", "")
                    print "Sender:({0},{1}), Receiver:({2},{3})".format(sid, sic, rid, ric)
                    #charTest(sid, sic, rid, ric)
            s.close()
            break
        except Exception as e:
            pass

if __name__ == '__main__':
    receivePackets()

