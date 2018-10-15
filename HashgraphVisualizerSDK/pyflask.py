
import socket
from flask import Flask, render_template
app = Flask(__name__)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

@app.route("/")
def hello():
    return render_template('untitled.html', SliderVal = 4, name =
            'Live Visualizer', graphJSON = "")

@app.route("/dapp")
def dapp():
	return render_template('dapp.html', TokenVal = 100, name ='Vote DApp')


app.run(host='0.0.0.0', port=5001)
