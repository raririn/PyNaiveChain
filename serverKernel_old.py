from flask import Flask, request, render_template, jsonify
from flask_uwsgi_websocket import GeventWebSocket
from blockchain import *
from param import *
import asyncio
import websockets

# As a trival center, the server should maintain the pear list as
# well as transaction pool for nodes.
peerList = set()
txnPool = []

# HTTP Interface Methods
app = Flask(__name__)
ws = GeventWebSocket(app)

def initServer():
    ''' Start the HTTP server. The port can be set
        in other files. '''
    app.run(host = '0.0.0.0', port = HTTP_port, debug = True)
    return

@app.route('/', methods = ['GET'])
def home():
    return render_template('home.html')

@app.route('/showChain', methods = ['GET'])
def showChain():
    global blockchain
    return blockchain.getJSON()

@app.route('/getIP', methods = ['GET'])
def getIP():
    return request.remote_addr

@app.route('/addPeer', methods = ['GET', 'POST'])
def addPeer():
    global peerList
    peerList.add(request.remote_addr)
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

# P2P Interface Methods
def initListen():
    ''' Set up a websocket listener on local host and port. '''
    start_websocket = websockets.serve(setupConnect, '0.0.0.0', P2P_port)
    print('Start listening on 0.0.0.0:', P2P_port)
    asyncio.get_event_loop().run_until_complete(start_websocket)
    asyncio.get_event_loop().run_forever()

async def setupConnect(websocket, path):
    ''' Set up a ONE-TIME connect listener. Receive the Client info and
    return the blockchain info.'''
    global blockchain
    queryJSON = await websocket.recv()
    query = json.loads(queryJSON)
    print(query)
    clientInfo = query['ClientInfo']
    peerList.add(clientInfo)
    if query['Query'] == P2P_query_ALLBLOCK:
        blockInfo = blockchain.getJSON()
        await websocket.send(blockInfo)
    else:
        await websocket.send("Hi")

if __name__ == '__main__':
    #initServer()
    initListen()