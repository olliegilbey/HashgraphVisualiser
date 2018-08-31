#
# https://code.tutsplus.com/tutorials/charting-using-plotly-in-python--cms-30286
#

from flask import Flask, render_template
import numpy as np
import dynamicgraph 

app = Flask(__name__)

@app.route('/test')
def chartTest():
    d = dynamicgraph.DynamicUpdate()
    d()
    
    graphJSON = ""
    for i in range(90):
        graphJSON = d.update(i, np.sin(i))
    
    print "_________________________________________"
    print graphJSON

    return render_template('untitled.html', name = 'Live Visualizer',
            graphJSON = graphJSON)


if __name__ == '__main__':
    app.run(debug = True)

