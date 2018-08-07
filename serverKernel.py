import json
import os
import asyncio

from sanic import Sanic, response
import websockets
from websockets.exceptions import ConnectionClosed

from blockchain import Blockchain
from block import Block
from param import *
from utils import *
from txn import *
from config import *
from sanicTools import render_template

class Server():
    def __init__(self):
        self.app = Sanic(__name__)
        self.blockchain = Blockchain()
        self.sockets = []
        self.txnPool = []
        self.app.add_route(self.showChain, '/showChain', methods = ['GET'])
        self.app.add_route(self.mineBlockPage, '/mineBlock', methods = ['GET'])
        self.app.add_route(self.mineBlock, '/mineBlock', methods = ['POST'])
        self.app.add_route(self.peers, '/peers', methods = ['GET'])
        self.app.add_route(self.addPeer, '/addPeer', methods = ['POST'])
        self.app.add_websocket_route(self.P2PHandler, '/')

    async def showChain(self, request):
        return response.text(self.blockchain.getJSON())
    
    async def mineBlockPage(self, request):
        return render_template('mineBlock.html')

    async def mineBlock(self, request):
        data = request.form['data'][0]  # IDK but data turns out to be a list instead of str
        currentBlock = self.blockchain.getLatestBlock()
        diff = self.blockchain.difficulty
        start_time = time.time()
        timestamp = calculateTimestamp(int(start_time))
        targetBlock = Block(currentBlock.index + 1, currentBlock.hash, timestamp, data)
        while str(targetBlock.hash)[0:diff] != ''.join(['0'] * diff):
            targetBlock.incrementNonce()
        self.blockchain.addNewBlock(targetBlock)
        await self._broadcast(self.blockchain.getJSON(), P2P_broadcast_CHAIN)
        return response.text(str(targetBlock.nonce))

    async def peers(self, request):
        peers = map(lambda x:"{}:{}".format(x.remote_address[0], x.remote_address[1]), self.sockets)
        return response.json(peers)
    
    async def addPeer(self, request):
        asyncio.ensure_future(self.connect_to_peers([request.json['peer']]), loop = asynico.get_event_loop())
        res = {"Status": True}
        return response.json(res)
    
    async def connect2Peers(self, newPeers):
        for peer in newPeers:
            try:
                ws = await websockets.connect(peer)
                await self.initConnection(ws)
            except Exception as e:
                print(str(e))

    async def P2PHandler(self, request, ws):
        try:
            await self.initConnection(ws)
        except ConnectionClosed:
            await self.connectionClosed(ws)
    
    async def initConnection(self, ws):
        self.sockets.append(ws)
        query = json.dumps({'type': P2P_query_ALLBLOCK})
        await ws.send(query)
        while True:
            await self.initMsgHandler(ws)

    async def connectionClosed(self, ws):
        self.sockets.remove(ws)
        print('Connection closed.')
        return
    
    async def initMsgHandler(self, ws):
        data = await ws.recv()
        message = json.loads(data)
        print(message)
        if message['type'] == P2P_query_LATESTBLOCK:
            await self.send_latest(ws, message)
        elif message['type'] == P2P_query_ALLBLOCK:
            await self.send_chain(ws, message)
        elif message['type'] == P2P_query_PEERLIST:
            await self.send_peerlist(ws, message)
        elif message['type'] == P2P_res_CHAIN:
            await self.process_res(ws, message)
        else:
            print('Bad query type.')
    
    async def send_latest(self, ws, *args):
        blockInfo = self.blockchain.getLatestBlock.getDictForm()
        res = json.dumps({'type': P2P_res_CHAIN, 'data': blockInfo})
        await ws.send(res)

    async def send_chain(self, ws, *args):
        chainInfo = self.blockchain.getJSON()
        res = json.dumps({'type': P2P_res_CHAIN, 'data': chainInfo})
        await ws.send(res)

    async def send_peerlist(self, ws, *args):
        pass

    async def process_res(self, ws, message):
        blockRecv = Blockchain.buildChainFromJSON(message['data'])
        print(message['data'])
        choose = Blockchain.chooseChain(self.blockchain, blockRecv)
        if isinstance(choose, int):
            print("Error: invalid chain. Code = ", choose)
        else:
            print("Chain replaced.")
            self.blockchain = choose

    async def _broadcast(self, message, option = P2P_broadcast_CHAIN):
        ''' General broadcast method, either works for txn and block.'''
        for socket in self.sockets:
            await socket.send(json.dumps({'type': option, 'data':message}))
    
if __name__ == '__main__':
    server = Server()
    server.app.add_task(server.connect2Peers(initialPeers))
    server.app.run(host = 'localhost', port = port, debug = False)
    