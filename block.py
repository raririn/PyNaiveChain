from utils import *
from param import *

##  Rework
##  Hash should not be passed into the block; but calculated inside instead.

class Block():
    def __init__(self, index, previousHash, timestamp, data):
        self.index = index
        self.previousHash = str(previousHash)
        self.timestamp = timestamp
        self.data = data
        self.nonce = 0
        self.hash = self._calculateHash()

    def __str__(self):
        ''' Override print method for Block.'''
        return str(self.index) + self.previousHash + str(self.timestamp) + str(self.data) + str(self.nonce) + self.hash

    def _getHashString(self):
        return str(self.index) + self.previousHash + str(self.timestamp) + str(self.data) + str(self.nonce)

    def _calculateHash(self):
        return hashlib.sha256(self._getHashString().encode()).hexdigest()

    def getHash(self):
        ''' Return hash value of the block. '''
        return self.hash

    def _checkHash(self):
        ''' Redundant function left; since the hash calculation has been changed. '''
        return self.hash == calculateHash(str(self.index) + self.previousHash + str(self.timestamp) + str(self.data))
    
    def getDictForm(self):
        ''' Return dict format information of the block.'''
        blockDict = {'Index': self.index,
        'PreviousHash': self.previousHash,
        'TimeStamp': self.timestamp,
        'Data': self.data,
        'nonce': self.nonce}
        return blockDict