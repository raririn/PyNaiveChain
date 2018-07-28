## Client side program.

#   In the beginning, as draft all functions the client
#   should have will be illustrated:
#   1. A HTTP-interface client, handling visualization.
#   2. Set up several websockets to handle P2P communication.

from utils import *
from blockchain import *
import requests

@localMethod
def localMine(data):
    global blockchain
    diff = blockchain.difficulty
    prevBlock = blockchain.getLatestBlock()
    start_time = time.time()
    timestamp = calculateTimestamp(int(start_time))
    targetBlock = Block(prevBlock.index + 1, prevBlock.hash, timestamp, data)
    while str(targetBlock.hash)[0:diff] != ''.join(['0'] * diff):
        targetBlock.incrementNonce()
    print("Block mined. Nonce = " +  str(targetBlock.nonce) + ".")

def requestToMain(mainURL):
    ''' Send a request to central server and grab info. '''
    r = requests.get(mainURL)
    return r.text

class HTTPClient:
    def __init__(self):
        pass

    @staticmethod
    def requestToMain(mainURL):
        ''' Send a request to central server and grab info. '''
        r = requests.get(mainURL + "/showChain")
        chainJSON = r.text
        chainINFO = json.loads(chainJSON)
        return chainINFO
    
    @staticmethod
    def broadcastTxn(mainURL):
        r = requests.post(mainURL + "/broadcastTxn", data = {'data1': 'Output', 'data2': 'Amount'})



if __name__ == '__main__':
    print(HTTPClient.requestToMain())