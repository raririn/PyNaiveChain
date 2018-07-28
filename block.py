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

    @inplaceMethod
    def _addCoinBaseTxn(self, sign):
        pass

    @inplaceMethod
    def forceRecalculateHash(self):
        ''' This is the EXTERNAL method of force recalculating hash value of a block,
            for cases if the values inside are overriden and thus need a recal.
            Return True if the value is already correct, and False if not.'''
        if self._checkHash:
            return True
        else:
            self.hash = self._calculateHash()
            return False
    
    @inplaceMethod
    def _recalculateHash(self):
        self.hash = self._calculateHash()
    
    @inplaceMethod
    def overrideTimestamp(self, timestamp):
        ''' External method for overriding timestamp after initialization. '''
        self.timestamp = timestamp
        self._recalculateHash()
        return 0

    @inplaceMethod
    def incrementNonce(self):
        ''' Increment the nonce by 1.'''
        self.nonce = self.nonce + 1
        self._recalculateHash()
        return 0

    def getHash(self):
        ''' Return hash value of the block. '''
        return self.hash

    def _checkHash(self):
        return self.hash == self._calculateHash()

    def getDictForm(self):
        ''' Return dict format information of the block.'''
        blockDict = {'Index': self.index,
        'PreviousHash': self.previousHash,
        'TimeStamp': self.timestamp,
        'Data': self.data,
        'nonce': self.nonce}
        return blockDict