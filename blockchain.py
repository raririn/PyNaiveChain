from block import Block
from utils import *
from param import *
##  Rework
##  It is annoying to use global methods, so a new class is defined.

class Blockchain:
    def __init__(self, chain = [], difficulty = 2):
        if chain == []:
            self.chain = [self._getGenesisBlock()]
        else:
            self.chain = chain
        self.difficulty = difficulty
    
    def _getGenesisBlock(self):
        ''' Return the hard-coded genesis block. '''
        return Block(GENESIS_index, GENESIS_previousHash, GENESIS_timestamp, GENESIS_data)

    def getLength(self):
        ''' Return the current length. Note the length equals to index of the NEXT block.'''
        return len(self.chain)
    
    def getLatestBlock(self):
        return self.chain[-1]
    
    def getLatestHash(self):
        return self.chain[-1].hash
    
    @inplaceMethod
    def _generateNextBlock(self, data):
        ''' Generate a new block given data to store, and fetch the latest block as previous. '''
        previous_block = self.getLatestBlock()
        previous_hash = previous_block.getHash()
        next_index = previous_block.inedx + 1
        next_timestamp = calculateTimestamp(time.time())
        next_block = Block(next_index, previous_hash, next_timestamp, data)
        self.chain.append(next_block)
        return True
    
    def getJSON(self):
        ''' Return JSON format info for web processing.'''
        dList = [i.getDictForm() for i in self.chain]
        return json.dumps(dList)

    @inplaceMethod
    def _adjustDifficulty(self):
        return False
    
    def isValid(self):
        ''' Validate the blockchain.
            Note: The method is expensive as it iterates over the full block list.
        '''
        for i in range(self.chain.getLength()):
            block = self.chain[i]
            if not (isinstance(block.index, int) and isinstance(block.hash, str) and \
            isinstance(block.previousHash, str) and isinstance(block.timestamp, str) \
            and isinstance(block.nonce, int)):
                return False
            if self.chain[i+1].previousHash != self.chain[i].hash:
                return False
            if self.chain[i+1].index != (self.chain[i].index + 1):
                return False
            if not block._checkHash():
                return False
        return True
            
        
    @staticmethod
    def buildChainFromJSON(chainJSON):
        chainList = json.loads(chainJSON)
        blockList = []
        for i in chainList:
            a_block = Block(i['Index'], i['PreviousHash'], i['TimeStamp'], i['Data'], i['Nonce'])
            blockList.append(a_block)
        return Blockchain(blockList)

    @staticmethod
    def chooseChain(chain1, chain2):
        ''' Choose the longer chain. Return 0 if both chains are valid and have equal length,
            and -1 if both are not valid (not expected since at least one of them should 
            be originally verified).'''
        if chain1.isValid() and chain2.isValid():
            if chain1.getLength() > chain2.getLength():
                return chain1
            elif chain2.getLength() > chain1.getLength():
                return chain2
            else:
                return 0
        elif chain1.isValid() and (not chain2.isValid()):
            return chain1
        elif (not chain1.isValid()) and chain2.isValid():
            return chain2
        else:
            return -1

if __name__ == '__main__':
    blockchain = Blockchain()
    bJ = blockchain.getJSON()
    print(buildChainFromJSON(bJ).getJSON())

# Global operations on initializing.
else:
    blockchain = Blockchain()