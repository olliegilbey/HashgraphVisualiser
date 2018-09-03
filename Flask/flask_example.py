# 
# https://code.tutsplus.com/tutorials/charting-using-plotly-in-python--cms-30286
#

from flask import Flask, render_template, request
from flask import request
import numpy as np
import dynamicgraph

app = Flask(__name__)

@app.route('/test', methods=['GET','POST'])
def chartTest():

    number_of_nodes = 0
    d = dynamicgraph.DynamicUpdate()
    d()

    graphJSON = ""
    for i in range(90):
        graphJSON = d.update(i, np.sin(i))

    print "_________________________________________"
    print graphJSON


    print("FORM:")
    print(request.form)
    # For button and slider handling
    if request.method == 'POST':
        number_of_nodes = request.values.get('slider')
        print "Number of Nodes: " + number_of_nodes
        #print number_of_nodes
        if request.form.get('Stop') == 'Stop':
            # pass
            print("Stop Pressed")
        elif  request.form.get('Start') == 'Start':
            # pass # do something else
            print("Start Pressed")
        else:
            print("Nothing Happened")



    return render_template('untitled.html', name = 'Live Visualizer',
            graphJSON = graphJSON)



if __name__ == '__main__':
    app.run(debug = True)
