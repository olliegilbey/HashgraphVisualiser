import socket
from models import *
from flask import Flask, render_template, request, url_for
from web3 import Web3

app = Flask(__name__)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

@app.route('/hello')
def hello_world():
	return 'Hello, World!'

@app.route('/', methods=['GET', 'POST'])
def dapp():
	global contract_instance
	if request.method == 'POST':
		contract_instance.vote( [int(request.form['slider1']), int(request.form['slider2']),
		int(request.form['slider3']), int(request.form['slider4']), int(request.form['slider5']),
		int(request.form['slider6']), int(request.form['slider7']), int(request.form['slider8']),
		int(request.form['slider9']), int(request.form['slider10'])] , transact={'from': w3.eth.accounts[0]} )

		print('Votes for Team 1 = {}'.format(contract_instance.totalVotesFor(b"Team 1")))
		print('Votes for Team 2 = {}'.format(contract_instance.totalVotesFor(b"Team 2")))
		print('Votes for Team 3 = {}'.format(contract_instance.totalVotesFor(b"Team 3")))
		print('Votes for Team 4 = {}'.format(contract_instance.totalVotesFor(b"Team 4")))
		print('Votes for Team 5 = {}'.format(contract_instance.totalVotesFor(b"Team 5")))
		print('Votes for Team 6 = {}'.format(contract_instance.totalVotesFor(b"Team 6")))
		print('Votes for Team 7 = {}'.format(contract_instance.totalVotesFor(b"Team 7")))
		print('Votes for Team 8 = {}'.format(contract_instance.totalVotesFor(b"Team 8")))
		print('Votes for Team 9 = {}'.format(contract_instance.totalVotesFor(b"Team 9")))
		print('Votes for Team 10 = {}'.format(contract_instance.totalVotesFor(b"Team 10")))

	return render_template('dapp.html', TokenVal = 100, SliderVal1 = 0, SliderVal2 = 0,
	SliderVal3 = 0, SliderVal4 = 0, SliderVal5 = 0, SliderVal6 = 0, SliderVal7 = 0,
	SliderVal8 = 0, SliderVal9 = 0, SliderVal10 = 0, name = "DApp")

w3 = Web3(HTTPProvider("http://127.0.0.1:8545"))
#w3 = Web3(HTTPProvider("http://172.19.0.2:6000"))
# deploy the Voting contract to ganache
contract_instance = deploy()

app.run(host='0.0.0.0', port=5000)
