from utils import *
from param import *

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
        return calculateHash(str(self.index) + self.previousHash + str(self.timestamp) + str(self.data))

    def selfHashCheck(self):
        return self.hash == str(self.calculate_block_hash())