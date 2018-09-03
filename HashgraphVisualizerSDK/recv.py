import socket
import dummy as visualiser
from flask import Flask, render_template
from flask import request
import dynamicgraph
import thread

app = Flask(__name__)
graphJSON = ""
d = dynamicgraph.DynamicUpdate()
d()

@app.route('/test', methods=['GET','POST'])
def routeTest():
    number_of_nodes = 4
    global graphJSON

    print("FORM:")
    print(request.form)
    # For button and slider handling

    if request.method == "POST":
        number_of_nodes = request.values.get('slider')
        print "Number of Nodes Showing: " + number_of_nodes
        #print the number of nodes
        if request.form.get('Stop') == 'Stop':
            print("Stop Pressed")
        elif request.form.get('Start') == 'Start':
            print("Start Pressed")
        else:
            print("Slider Changed or Nothing")

    return render_template('untitled.html',SliderVal = number_of_nodes, name = 'Live Visualizer',
            graphJSON = graphJSON)


def charTest(sx, sy, rx, ry):
    global graphJSON
    graphJSON = d.update(sx, sy)
    graphJSON = d.update(rx, ry)
    graphJSON = d.update(None, None)
    #print graphJSON

   # Run the flask app in a separate thread
def flaskThread():
    app.run()

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
            
            thread.start_new_thread(flaskThread,())

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
                    charTest(sid, sic, rid, ric)
            s.close()
            break
        except Exception as e:
            pass

if __name__ == '__main__':
    receivePackets()

