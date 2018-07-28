from block import *

##  Rework
##  It is annoying to use global methods, so a new class is defined.

class Blockchain:
    def __init__(self):
        self.chain = [self._getGenesisBlock()]
        self.difficulty = 2
    
    def _getGenesisBlock(self):
        ''' Return the hard-coded genesis block. '''
        return Block(GENESIS_index, GENESIS_previousHash, GENESIS_timestamp, GENESIS_data)

    def getLength(self):
        ''' Return the current length. '''
        return len(self.chain)
    
    def getLatestBlock(self):
        return self.chain[-1]
    
    def getLatestHash(self):
        return self.chain[-1].hash
    
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

    def _adjustDifficulty(self):
        return False

if __name__ == '__main__':
    blockchain = Blockchain()
    print(blockchain.chain[0])

# Global operations on initializing.
else:
    blockchain = Blockchain()