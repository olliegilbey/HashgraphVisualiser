import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.tools as tls
import json
import numpy as np

print plotly.__version__

class DynamicUpdate():
    y_data = []
    x_data = []
    
    def on_launch(self):
        global x_data
        global y_data
        y_data = []
        x_data = []
    
    def update(self, newx, newy):
        global x_data
        global y_data

        x_data =  np.append(x_data, newx)
        y_data =  np.append(y_data, newy)
        
        #print "x = [] = ", x_data
        #print "y = [] = ", y_data
        
        data = [ go.Scatter(
                    x = x_data,
                    y = y_data) ]
        graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder) 
        #print graphJSON
        #plot_str = py.offline.plot(data, include_plotlyjs=False, output_type='div')
        return graphJSON

    def __call__(self):
        global x_data, y_data
        self.on_launch()
        print "x = [] = ", x_data
        print "y = [] = ", y_data
