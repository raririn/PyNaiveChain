from utils import *
from param import *
from txn import *

##  Rework
##  Hash should not be passed into the block; but calculated inside instead.

class Data():
    def __init__(self):
        pass

class Block():
    def __init__(self, index, previousHash, timestamp, data = '', nonce = 0):
        self.index = int(index)
        self.previousHash = str(previousHash)
        self.timestamp = timestamp
        self.data = data
        self.nonce = nonce
        self.hash = self._calculateHash()

    def __str__(self):
        ''' Override print method for Block.'''
        return str(self.index) + self.previousHash + str(self.timestamp) + str(self.data) + str(self.nonce) + self.hash

    def _getHashString(self):
        return str(self.index) + self.previousHash + str(self.timestamp) + str(self.data) + str(self.nonce)

    def _calculateHash(self):
        return calculateHash(self._getHashString())

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
        'Nonce': self.nonce}
        return blockDict

if __name__ == '__main__':
    a = Block(1, 0, 0, '123')
    print(a.getDictForm())