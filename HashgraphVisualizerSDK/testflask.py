import socket
from flask import Flask, render_template, url_for
app = Flask(__name__)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

@app.route("/")
def hello():
    return render_template('dapp.html', SliderVal1 = 0, SliderVal2 = 0, SliderVal3 = 0, SliderVal4 = 0, SliderVal5 = 0, SliderVal6 = 0, SliderVal7 = 0, SliderVal8 = 0, SliderVal9 = 0, SliderVal10 = 0, TokenVal = 100, name =
            'DApp')

app.run(host='0.0.0.0', port=5000)
