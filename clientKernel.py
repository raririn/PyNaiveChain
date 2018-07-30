## Client side program.

#   In the beginning, as draft all functions the client
#   should have will be illustrated:
#   1. A HTTP-interface client, handling visualization.
#   2. Set up several websockets to handle P2P communication.

from utils import *
from blockchain import *
import requests
from websocket import create_connection
import asyncio
import websockets

class localClient:
    def __init__(self):
        self.txnPool = []

    @staticmethod
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


class HTTPClient:
    def __init__(self):
        pass

    @staticmethod
    def requestToMain(mainURL):
        ''' Send a request to central server and grab info. '''
        r = requests.get(mainURL + "/showChain")
        chainJSON = r.text
        print(chainJSON)
        chainINFO = json.loads(chainJSON)
        return chainINFO
    
    @staticmethod
    def getLocalIP(mainURL = HTTP_localhost):
        ''' Send a request querying local IP. '''
        r = requests.get(mainURL + "/getIP")
        localIP = r.text
        return localIP
    
    @staticmethod
    def broadcastTxn(mainURL):
        r = requests.post(mainURL + "/broadcastTxn", data = {'data1': 'Output', 'data2': 'Amount'})



class P2PClient:
    def __init__(self, port = P2P_recvport):
        self.port = port
    
    @staticmethod
    async def openConnect(targetAddress = P2P_localhost, queryOption = P2P_query_ALLBLOCK):
        ''' Open a connect, sending localhost info and get
            info of chain. '''
        async with websockets.connect(
                'ws://' + targetAddress) as websocket:
            #localIP = HTTPClient.getLocalIP()
            localIP = '1'
            localTarget =  str(localIP) + ':' + str(P2P_recvport)
            query = {'ClientInfo': localTarget, 'Query': queryOption}
            queryJSON = json.dumps(query)
            await websocket.send(queryJSON)
            backMsg = await websocket.recv()
            if query['Query'] == P2P_query_ALLBLOCK:
                chainObtained = buildChainFromJSON(backMsg)
                print(backMsg)
            else:
                pass

    
    @staticmethod
    def initConnect():
        asyncio.get_event_loop().run_until_complete(P2PClient.openConnect())
        #asyncio.get_event_loop().run_forever()

if __name__ == '__main__':
    P2PClient.initConnect()