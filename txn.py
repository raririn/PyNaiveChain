from utils import calculateHash
from functools import reduce
import numpy as np

# The transaction class will likely to suffer from serious type-check
# problem, so every constructor is forced to apply a type check.

class TxOut():
    def __init__(self, address, amount):
        if not isinstance(address, str) or not isinstance(amount, np.float64):
            raise TypeError('Bad TxOut constructor parameter.')
        self.address = address          # str
        self.amount = amount            # np.float64

class TxIn():
    def __init__(self, TxOutID, TxOutIndex, signature):
        self.TxOutID = TxOutID          # str
        self.TxOutIndex = TxOutIndex    # int
        self.signature = signature      # str

class Transaction():
    def __init__(self):
        self.id = 0
        self.TxIns = []
        self.txOuts = []
    
    def getID(self):
        r = map(lambda x, y: (x + str(y)), self.TxIns)
        txInContent = reduce(lambda x, y: (x + y), r)
        r = map(lambda x, y: (x + str(y)), self.TxOuts)
        txOutContent = reduce(lambda x, y: (x + y), r)
        return calculateHash(txInContent + txOutContent)
    
    def signTxIn(self, txInIndex, privateKey, aUnspentTxOuts):
        TxIn = self.TxIns[txInIndex]
        dataToSign = self.id

class coinbaseTransaction():
    def __init__(self, TxOut, index):
        self.ID = calculateHash(str(TxOut.address) + str(TxOut.amount) + str(index))
        self.TxOut = TxOut
    
    def __str__(self):
        return "<br>{Transaction ID: " + str(self.ID) + "<br>IN: None -><br>OUT: " + str(self.TxOut.address) + "<br>Amount: " + str(self.TxOut.amount) + "Coins}"

def createCoinbaseTxn(address, index):
    txnout = TxOut(address, 50)
    txin = None
    txn = coinbaseTransaction(txnout, index)
    return txn