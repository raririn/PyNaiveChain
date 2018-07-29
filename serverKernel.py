from flask import Flask, request, render_template, jsonify
from flask_uwsgi_websocket import GeventWebSocket
from blockchain import *
from param import *

# As a trival center, the server should maintain the pear list as
# well as transaction pool for nodes.
peerList = []
txnPool = []

# HTTP Interface Methods
app = Flask(__name__)
ws = GeventWebSocket(app)

def initServer():
    app.run(host = HTTP_host, port = HTTP_port, debug = True)
    return

@app.route('/', methods = ['GET'])
def home():
    return render_template('home.html')

@app.route('/showChain', methods = ['GET'])
def showChain():
    global blockchain
    return blockchain.getJSON()

@app.route('/addPeer', methods = ['GET', 'POST'])
def addPeer():
    global peerList
    peerList.append(request.remote_addr)
    return '<br>'.join([str(x) for x in peerList])

@app.route('/broadcastTxn', methods = ['GET'])
def broadcastTxn_get():
    return render_template('mine.html')

@app.route('/broadcastTxn', methods = ['POST'])
def broadcastTxn_post():
    # TODO: The TXN here ought to be a object instead of str.
    data1 = request.form['data1']   # Output address
    data2 = request.form['data2']   # amount
    global blockchain, txnPool
    index = blockchain.getLength()
    ID = calculateHash(str(data1) + str(data2) + str(index))
    txn = "<br>{Transaction ID: " + str(ID) + "<br>IN: " + str(SENDDEFAULT_publickey) + "-><br>OUT: " + str(data1) + "<br>Amount: " + str(data2) + "Coins}"
    txnPool.append(txn)
    return 'OK message sent!'

@app.route('/showPool', methods = ['GET'])
def showPool():
    return ' '.join([i for i in txnPool])

@app.route('/getConnectAddress', methods = ['GET', 'POST'])
def getConnectAddress():
    return render_template('peerConnect.html')

@ws.route('/getConnect')
def getConnect_ws(wscon):
    count = 0
    users = {}
    users[wscon.id] = wscon
    while True:
        message = wscon.receive()
        if message is not None:
            for id in users:
                users[id].send(message, count)
                count += 1
        else:
            break
    del users[wscon.id]