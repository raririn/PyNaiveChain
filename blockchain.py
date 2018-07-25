from block import *
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
    for i in range(DEFAULT_difficulty):
        if not newBlock.hash[i] == '0':
            return False
    print("reach end")
    return True

def addBlockWithDiff(newBlock):
    if isValidNewBlockWithDiff(newBlock, getLatestBlock()):
        global blockchain
        blockchain.append(newBlock)
        return MINING_successMessage
    else:
        return "The hash doesn't fit."

# Global operations on initializing.
blockchain = []
blockchain.append(getGenesisBlock())