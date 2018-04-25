from * import utils
import time

GENESIS_index = 0
GENESIS_previousHash = 0
GENESIS_timestamp = 1465154705
GENESIS_data = "The first block"
GENESIS_hash = calculateHash(str(0) + str(0) + str(GENESIS_timestamp) + GENESIS_data)

class Block():
    def __init__(self, index, previousHash, timestamp, data, hash):
        self.index = index
        self.previousHash = str(previousHash)
        self.timestamp = timestamp
        self.data = data
        self.hash = str(hash)

    def __str__(self):
        return str(self.index) + self.previousHash + str(self.timestamp) + str(self.data) + self.hash

    def calculate_block_hash(self):
        return calculateHash(self.__str__())

    def selfHashCheck(self):
        return self.hash == str(self.calculate_block_hash())
    


def getGenesisBlock():
    ''' Return the hard-coded genesis block. '''
    return Block(GENESIS_index, GENESIS_previousHash, GENESIS_timestamp, GENESIS_data, GENESIS_hash)

def getLatestBlock():
    ''' Return the latest block. '''
    current_length = len(blockchain)
    return blockchain[current_length - 1]

def generateNextBlock(data):
    ''' Generate a new block given data to store, and fetch the latest block as previous. '''
    previous_block = getLatestBlock()
    next_index = previous_block.index + 1
    next_timestamp = int(time.time())
    next_hash = calculateHash(str(next_index + previous_block.hash + str(next_timestamp) + str(data))
    return Block(next_index, previous_block.hash, next_timestamp, data, next_hash)

def isValidNewBlock(newBlock, previousBlock):
    ''' Check if all these attributes are correct:
        1. Index
        2. Previous Hash
        3. New Hash'''
    if previousBlock.index + 1 != newBlock.index:
        return False
    elif previousBlock.hash != newBlock.previousHash:
        return False
    elif newBlock.selfHashCheck():
        return False
    return True

def addBlock(newBlock):
    ''' If a new block is valid, push it to the end of chain. '''
    if isValidNewBlock(newBlock, getLatestBlock()):
        global blockchain
        blockchain.append(newBlock)
    return

if __name__ == '__main__':
    blockchain = []     # Initialization as a list
    blockchain.append(getGenesisBlock)

    