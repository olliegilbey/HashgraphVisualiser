from flask import Flask
app = Flask(__name__)


@app.route("/dapp")
def dapp():
	return render_template('dapp.html', TokenVal = 100, name ='Vote DApp')

@app.route('/')
def hello_world():
	return 'Hello, World!'

if __name__ == "__main__":
    app.run()
