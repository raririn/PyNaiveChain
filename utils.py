import hashlib

def calculateHash(content):
    ''' Return SHA-256 value in hex of given string '''
    return hashlib.sha256(content.encode()).hexdigest