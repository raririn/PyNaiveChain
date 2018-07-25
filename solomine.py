import requests
import time
from param import *
from txn import *
from utils import calculateHash

nonce = 0
transactionPool = []
IN = ''
mine = True

r = requests.get('http://127.0.0.1:5001/getlen')
#print(r.text)
index = int(r.text)
coinbaseTxn = createCoinbaseTxn(DEFAULT_publickey, index)
transactionPool.append(coinbaseTxn)
#print(str(coinbaseTxn))

for txn in transactionPool:
    IN = IN + str(txn)
IN_backup = IN

while mine:
    r = requests.get('http://127.0.0.1:5001/getbuffer')
    if not r.text == '':
        IN = IN + r.text
    d = {'data':IN, 'nonce': nonce}
    r = requests.post(MINING_url, d)
    print(r.text + "Nonce: " + str(nonce))
    if r.text == MINING_successMessage:
        print("Mined successfully.")
        #break
        nonce = 0
        IN = IN_backup
        a = input("Continue? Y/n\n")
        if a == 'n':
            break
    nonce = nonce + 1
print("End.")