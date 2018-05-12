from flask import Flask, request, render_template
from flask_uwsgi_websocket import GeventWebSocket
from blockchain import *

# HTTP Interface Methods
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

@app.route('/mineBlock', methods = ['GET'])
def mineblock_get():
    return render_template('mine.html')

@app.route('/mineBlock', methods = ['POST'])
def mineblock_post():
    data = request.form['data']
    print(data)
    addBlock(generateNextBlock(data))
    return 'OK block added!'
    
@app.route('/clientMine', methods = ['POST'])
def clientMine_post():
    data = str(request.form['data']) + str(request.form['nonce'])
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
        if message is not None:
            for id in users:
                if id != wscon.id:
                    users[id].send(message)
        else:
            break
    del users[wscon.id]