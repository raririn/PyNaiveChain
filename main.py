from block import *

from flask import Flask, request, render_template
from flask_uwsgi_websocket import GeventWebSocket
import time

# Blockchain methods

def getGenesisBlock():
    ''' Return the hard-coded genesis block. '''
    return Block(GENESIS_index, GENESIS_previousHash, GENESIS_timestamp, GENESIS_data, GENESIS_hash)

def getLatestBlock():
    ''' Return the latest block. '''
    global blockchain
    current_length = len(blockchain)
    return blockchain[current_length - 1]

def generateNextBlock(data):
    ''' Generate a new block given data to store, and fetch the latest block as previous. '''
    previous_block = getLatestBlock()
    next_index = previous_block.index + 1
    next_timestamp = int(time.time())
    next_hash = calculateHash(str(next_index) + str(previous_block.hash) + str(next_timestamp) + str(data))
    return Block(next_index, previous_block.hash, next_timestamp, data, next_hash)

def isValidNewBlock(newBlock, previousBlock):
    ''' Check if all these attributes are correct:
        1. Index
        2. Previous Hash
        3. New Hash'''
    if previousBlock.index + 1 != newBlock.index:
        print("Warning: Index check failed.")
        return False
    elif previousBlock.hash != newBlock.previousHash:
        print("Warning: Previous hash check failed.")
        return False
    elif not (newBlock.selfHashCheck()):
        print("Warning: Self hash check failed.")
        return False
    return True

def addBlock(newBlock):
    ''' If a new block is valid, push it to the end of chain. '''
    # print("using addblock")
    if isValidNewBlock(newBlock, getLatestBlock()):
        global blockchain
        blockchain.append(newBlock)
    else:
        print("invalid block detected")
    return

def isValidNewBlockWithDiff(newBlock, previousBlock):
    if not isValidNewBlock(newBlock, previousBlock):
        return False
    elif not newBlock.hash[0] == '0':
        return False
    return True

def addBlockWithDiff(newBlock):
    if isValidNewBlockWithDiff(newBlock, getLatestBlock()):
        global blockchain
        blockchain.append(newBlock)
        return "Hash fits."
    else:
        return "The hash doesn't fit."

# HTTP Interface Methods
app = Flask(__name__)
ws = GeventWebSocket(app)
def initServer():
    app.run(host = HTTP_host, port = HTTP_port, debug = True)

@app.route('/', methods = ['GET', 'POST'])
def home():
    #return home_txt
    return render_template('home.html')

@app.route('/blocks', methods = ['GET'])
def blocks_get():
    global blockchain
    #print(blockchain)
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
    pass

@app.route('/addPeer', methods = ['POST'])
def addPeer_post():
    pass

blockchain = []
blockchain.append(getGenesisBlock())
if __name__ == '__main__':
    initServer()

    # Debugging
    # print(blockchain[0])
    # print(GENESIS_hash)
    # addBlock(generateNextBlock('data'))
    #print(blockchain2txt(BC.blockchain))