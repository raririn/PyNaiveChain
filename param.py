from block import *

# Genesis block parameter
GENESIS_index = 0
GENESIS_previousHash = 0
GENESIS_timestamp = 1465154705
GENESIS_data = "The first block"
GENESIS_hash = calculateHash(str(0) + str(0) + str(GENESIS_timestamp) + GENESIS_data)

# Mining parameter
DEFAULT_difficulty = 2
MINING_url = 'http://127.0.0.1:5001/clientMine'
MINING_successMessage = 'OK.'

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