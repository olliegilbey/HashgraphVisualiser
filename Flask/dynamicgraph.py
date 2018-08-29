import plotly as py
import plotly.graph_objs as go
import plotly.tools as tls

print py.__version__

class DynamicUpdate():
    x_data = []
    y_data = []

    def on_launch(self):
        global x_data, y_data
        y_data = []
        x_data = []
    
    def update(self, newx, newy):
        global x_data, y_data
        x_data += [newx]
        y_data += [newy]

        data = [ go.Scatter(
                    x = x_data,
                    y = y_data) ]
        
        plot_str = py.offline.plot(data, include_plotlyjs=False, output_type='div')
        return plot_str

    def __call__(self):
        global x_data, y_data
        self.on_launch()
        print "x = [] = ", x_data
        print "y = [] = ", y_data
