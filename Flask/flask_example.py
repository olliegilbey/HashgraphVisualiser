from flask import Flask, render_template
import numpy as np
import pandas
import dynamicgraph 

app = Flask(__name__)

@app.route('/test')
def chartTest():
    d = dynamicgraph.DynamicUpdate()
    d()

    for i in range(180):
        graph_html = d.update(i, np.sin(i))

    return render_template('untitled.html', name = 'Live Visualizer',
            url=graph_html)


if __name__ == '__main__':
    app.run(debug = True)

