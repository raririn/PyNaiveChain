from utils import calculateHash

class TxOut():
    def __init__(self, address, amount):
        self.address = address
        self.amount = amount

class TxIn():
    def __init__(self, TxOutID, TxOutIndex, signature):
        self.TxOutID = TxOutID
        self.TxOutIndex = TxOutIndex
        self.signature = signature

class Transaction():
    def __init__(self, TxIn, TxOut):
        self.ID = calculateHash(str(TxOut.address) + str(TxOut.amount) + str(TxIn.TxOutIndex) + str(TxIn.TxOutID) + str(TxIn.signature))
        self.TxIn = TxIn
        self.txOut = TxOut

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