import socket
from models import *
from flask import Flask, render_template, request
from web3 import Web3

app = Flask(__name__)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

@app.route('/', methods=['GET', 'POST'], SliderVal1 = 0, SliderVal2 = 0, SliderVal3 = 0, SliderVal4 = 0, SliderVal5 = 0, SliderVal6 = 0, SliderVal7 = 0, SliderVal8 = 0, SliderVal9 = 0, SliderVal10 = 0, name = "DApp")
def dapp():

	if request.method == 'POST':
		contract_instance.vote([request.form['slider1'], request.form['slider2'], request.form['slider3']], transact={'from': w3.eth.accounts[0]})

	return render_template('dapp.html', TokenVal = 100, name ='Vote DApp')

w3 = Web3(HTTPProvider("http://127.0.0.1:8545"))
# deploy the Voting contract to ganache
contract_instance = deploy()

#print('Votes for Team 1 = {}'.format(contract_instance.totalVotesFor(b"Team 1")))

#contract_instance.vote([3, 1, 2], transact={'from': w3.eth.accounts[0]})

app.run(host='0.0.0.0', port=5001)
