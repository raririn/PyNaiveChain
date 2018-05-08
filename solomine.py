import requests

url = 'http://127.0.0.1:5001/clientMine'
nonce = 0
IN = input("Input the data:")
while True:
    d = {'data':IN, 'nonce': nonce}
    r = requests.post(url, d)
    print(r.text)
    if r.text == "Hash fits.":
        break
    nonce = nonce + 1
print("Mined successfully.")