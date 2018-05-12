import requests
from param import *

nonce = 0
IN = input("Input the data:")
while True:
    d = {'data':IN, 'nonce': nonce}
    r = requests.post(MINING_url, d)
    print(r.text)
    if r.text == MINING_successMessage:
        break
    nonce = nonce + 1
print("Mined successfully.")