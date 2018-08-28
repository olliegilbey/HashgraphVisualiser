from flask import Flask, render_template
import numpy as np
import pandas
import matplotlib.pyplot as plt

#import dynamic_graph as dg 

app = Flask(__name__)

@app.route('/test')
def chartTest():
    d = dg.DynamicUpdate()
    d()
    lnprice=np.log(price)
    plt.plot(lnprice)   
    plt.savefig('/static/images/new_plot.png')
    return render_template('untitled1.html', name = 'new_plot',
            url='/static/images/new_plot.png')


if __name__ == '__main__':
    app.run(debug = True)

