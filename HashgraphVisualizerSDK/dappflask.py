import socket
from models import *
from flask import Flask, render_template, request, url_for, flash, redirect, session
from web3 import Web3

app = Flask(__name__)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
voterId = 0
studentNums = [20000000,
19768125,20143516,19923929,20129882,19236980,20460767,20000001,
19800045,20059884,19060815,20289472,19907281,16579089,20000002,
19894295,20415834,19976755,19960344,20424809,20058837,20000003,
18293468,18998178,20131836,19775520,18632807,19059019,20000004,
19165072,19930259,19478275,18187595,19400578,23053070,20000005,
17794633,19854382,18966330,18395376,20273401,19843151,20000006,
19768257,20165714,20194749,19007361,18439713,19990812,20000007,
20056354,20039867,20277970,19770251,19206674,20072015,20000008,
19896913,19770235,17839688,19066171,18395317,19790155,20000009,
19787065,18232973,20326033,19375816,19072708,18214304,20000010]

@app.route('/hello')
def hello_world():
	#return 'Hello, World!'
	return render_template('login.html', name="Login", GreatSuccess="")

@app.route('/', methods=['GET', 'POST'])
def login():
	global contract_instance
	global voterId
	if request.method == 'POST':
		try:
			voterId = studentNums.index(int(request.form['studnum']))
			#return render_template('dapp.html', TokenVal = contract_instance.getVotesRemaining(voterId), SliderVal1 = 0, SliderVal2 = 0,
			#SliderVal3 = 0, SliderVal4 = 0, SliderVal5 = 0, SliderVal6 = 0, SliderVal7 = 0,
			#SliderVal8 = 0, SliderVal9 = 0, SliderVal10 = 0, name = "DApp")
			return redirect(url_for('dapp',currVoterId=voterId))
		except ValueError as e:
			flash('Error, don\'t try your shit around here, your student number isn\'t valid')
			print("Invalid Student Number")

	return render_template('login.html', GreatSuccess = "Input Student Number", name = "Login")


@app.route('/dapp/<currVoterId>', methods=['GET', 'POST'])
def dapp(currVoterId):
	print("Dapp Function Entered")
	global contract_instance
	global voterId
	voterId = int(currVoterId)
	if request.method == 'POST':
		sumvotes = int(request.form['slider1']) + int(request.form['slider2']) + int(request.form['slider3']) + int(request.form['slider4']) + int(request.form['slider5']) + int(request.form['slider6']) + int(request.form['slider7']) + int(request.form['slider8']) + int(request.form['slider9']) + int(request.form['slider10'])

		if sumvotes <= contract_instance.getVotesRemaining(int(voterId)):
			contract_instance.vote( [int(request.form['slider1']), int(request.form['slider2']),
			int(request.form['slider3']), int(request.form['slider4']), int(request.form['slider5']),
			int(request.form['slider6']), int(request.form['slider7']), int(request.form['slider8']),
			int(request.form['slider9']), int(request.form['slider10'])], int(voterId) , transact={'from': w3.eth.accounts[int(voterId)]} )

			#contract_instance.vote( [0,1,2,3,4,5,6,7,8,9], 0 , transact={'from': w3.eth.accounts[7]} )
			print("balance ",w3.fromWei(w3.eth.getBalance(w3.eth.accounts[voterId]),'ether'))
			print("account ",w3.eth.accounts[voterId])
			remainingVotes = contract_instance.getVotesRemaining(voterId)
			print("votes remaining ", remainingVotes)

			print('Votes for Team  1 = {}'.format(contract_instance.totalVotesFor(b"Team 1")))
			print('Votes for Team  2 = {}'.format(contract_instance.totalVotesFor(b"Team 2")))
			print('Votes for Team  3 = {}'.format(contract_instance.totalVotesFor(b"Team 3")))
			print('Votes for Team  4 = {}'.format(contract_instance.totalVotesFor(b"Team 4")))
			print('Votes for Team  5 = {}'.format(contract_instance.totalVotesFor(b"Team 5")))
			print('Votes for Team  6 = {}'.format(contract_instance.totalVotesFor(b"Team 6")))
			print('Votes for Team  7 = {}'.format(contract_instance.totalVotesFor(b"Team 7")))
			print('Votes for Team  8 = {}'.format(contract_instance.totalVotesFor(b"Team 8")))
			print('Votes for Team  9 = {}'.format(contract_instance.totalVotesFor(b"Team 9")))
			print('Votes for Team 10 = {}'.format(contract_instance.totalVotesFor(b"Team 10")))
			if(remainingVotes > 0):
				print("STILL HAS VOTES REMAINING")
			else:
				#return redirect(url_for('/'))
				return render_template('login.html', name="Login", GreatSuccess="Successful Vote")
		else:
			flashstring = "You only have " + str(contract_instance.getVotesRemaining(int(voterId))) + " votes to use."
			flash(TokenVal)

	return render_template('dapp.html', TokenVal = contract_instance.getVotesRemaining(int(voterId)), SliderVal1 = 0, SliderVal2 = 0,
	SliderVal3 = 0, SliderVal4 = 0, SliderVal5 = 0, SliderVal6 = 0, SliderVal7 = 0,
	SliderVal8 = 0, SliderVal9 = 0, SliderVal10 = 0, name = "DApp")


w3 = Web3(HTTPProvider("http://127.0.0.1:8545"))
#w3 = Web3(HTTPProvider("http://172.19.0.2:6000"))
# deploy the Voting contract to ganache
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
contract_instance = deploy(71)
#app.run(debug=True)
app.run(host='0.0.0.0', port=5000)
