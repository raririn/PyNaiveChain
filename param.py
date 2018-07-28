from block import *

# Genesis block parameter
GENESIS_index = 0
GENESIS_previousHash = 0
GENESIS_timestamp = 1465154705
GENESIS_data = "The first block"
GENESIS_hash = calculateHash(str(0) + str(0) + str(GENESIS_timestamp) + GENESIS_data)

# Mining parameter
DEFAULT_difficulty = 1
COINBASE_amount = 50
MINING_url = 'http://127.0.0.1:5001/clientMine'
MINING_successMessage = 'OK.'

# Solomine parameter
DEFAULT_publickey = '04bfcab8722991ae774db48f934ca79cfb7dd991229153b9f732ba5334aafcd8e7266e47076996b55a14bf9913ee3145ce0cfc1372ada8ada74bd287450313534a'
DEFAULT_privatekey = '19f128debc1b9122da0635954488b208b829879cf13b3d6cac5d1260c0fd967c'
SENDDEFAULT_publickey = '04b79a37f042c7827172b1616dbaa5ab5d27d73b1d4da18e2bb289dbf2c9b58ec1e181dab7f9d1f8b88e23c2edea5f956b9f42e45093047a7f356c055597bfefa6'
SENDDEFAULT_privatekey = 'db20d9dc29bfc78f72944f3fd778cf42cd6a360f82a7a4f18bbd27e361d1c8bb'

# HTTP server parameter
HTTP_port = 5001
HTTP_host = '127.0.0.1' # WARNING: the JS and HTML file doesn't include this.
home_txt = '''<html>
<body>
<p>Hello, world! </p>
</body>
</html>'''


# P2P server parameter
P2P_port = 6001
P2P_central_server = "http://bc-t.herokuapp.com/"