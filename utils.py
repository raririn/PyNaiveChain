import hashlib
import json
import time

def calculateHash(content):
    ''' Return SHA-256 value in hex of given string. '''
    return hashlib.sha256(content.encode()).hexdigest()

def blockchain2txt(blockchain):
    ''' Return given blockchain(list) in readable HTML format. '''
    text = ''
    for block in blockchain:
        # (self, index, previousHash, timestamp, data, hash)
        text = text + ('Block No. %s <br> PreviousHash: %s <br> Timestamp: %s <br> Data: %s <br> Hash: %s <br><br>' % (str(block.index), block.previousHash, str(block.timestamp), str(block.data), block.hash))
    return text

def calculateTimestamp(currentTime):
    ''' Calculate a timestamp in %Y-%m-%d %H:%M:%S.
        Notice: the time should ba passed instead
        of calculating the time this function is called. '''
    now = int(currentTime)
    timeArray = time.localtime(now)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime

def localMethod(func):
    ''' A decorator doing nothing but implying the type of function.'''
    def wrapper(*args, **kw):
        #print('Calling %s():' % func.__name__)
        return func(*args, **kw)
    return wrapper

def HTTPMethod(func):
    return localMethod(func)

def SocketMethod(func):
    return localMethod(func)

def inplaceMethod(func):
    ''' The method is dangerous: It changes the value of object. '''
    return localMethod(func)