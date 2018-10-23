from flask import Flask, render_template, url_for
app = Flask(__name__)


@app.route("/")
def dapp():
        return render_template('dapp.html', TokenVal = 100, SliderVal1 = 0, SliderVal2 = 0, SliderVal3 = 0, SliderVal4 = 0, SliderVal5 = 0, SliderVal6 = 0, SliderVal7 = 0, SliderVal8 = 0, SliderVal9 = 0, SliderVal10 = 0, name = "DApp")

@app.route('/hello')
def hello_world():
	return 'Hello, World!'

if __name__ == "__main__":
    app.run(host='0.0.0.0')
