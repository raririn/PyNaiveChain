from hashlib import sha256
from math import log

def entropy(wkList):
    wkSet   = set(wkList)
    rate    = {}
    lenList = len(wkList)
    for i in wkSet:
        rate[i] = float(wkList.count(i)) / lenList
    return sum([-p * log(p, 2) for p in rate.values()])

if __name__ == '__main__':
    wkDict = {} # key: index number; value: list of appeared chars
    for i in xrange(1000000):
        s = sha256(str(i)).hexdigest()
        for j in xrange(32):
            if not j in wkDict:
                wkDict[j] = [s[j]]
            else:
                wkDict[j].append(s[j])

    for j in xrange(32):
        print j, '\t', entropy(wkDict[j])