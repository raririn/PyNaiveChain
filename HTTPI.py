from flask import Flask, request, render_template
from flask_uwsgi_websocket import GeventWebSocket
from blockchain import *

# HTTP Interface Methods
txnbuffer = []
app = Flask(__name__)
ws = GeventWebSocket(app)
def initServer():
    app.run(host = HTTP_host, port = HTTP_port, debug = True)

@app.route('/', methods = ['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/blocks', methods = ['GET'])
def blocks_get():
    global blockchain
    return blockchain2txt(blockchain)

@app.route('/getbuffer', methods = ['GET'])
def getbuffer():
    global txnbuffer
    buffertext = ''
    for i in txnbuffer:
        buffertext = buffertext + str(i)
    txnbuffer = []  # reset
    return buffertext

@app.route('/getlen', methods = ['GET'])
def getlen():
    global blockchain
    return str(len(blockchain))

@app.route('/broadcastTxn', methods = ['GET'])
def broadcastTxn_get():
    return render_template('mine.html')

@app.route('/broadcastTxn', methods = ['POST'])
def broadcastTxn_post():
    data1 = request.form['data1']   # Output address
    data2 = request.form['data2']   # amount
    global blockchain
    index = len(blockchain)
    ID = calculateHash(str(data1) + str(data2) + str(index))
    txn = "<br>{Transaction ID: " + str(ID) + "<br>IN: " + str(SENDDEFAULT_publickey) + "-><br>OUT: " + str(data1) + "<br>Amount: " + str(data2) + "Coins}"
    txnbuffer.append(txn)
    return 'OK message sent!'
    
@app.route('/clientMine', methods = ['POST'])
def clientMine_post():
    data = str(request.form['data']) + '<br> Nonce:' + str(request.form['nonce'])
    return addBlockWithDiff(generateNextBlock(data))

@app.route('/peers', methods = ['GET'])
def peers_get():
    return render_template('peerConnect.html')

@ws.route('/addPeer')
def addPeer_ws(wscon):
    users = {}
    users[wscon.id] = wscon
    while True:
        message = wscon.receive()
        print("message:", message)
        if message is not None:
            for id in users:
                if id != wscon.id:
                    users[id].send(message)
        else:
            break
    del users[wscon.id]