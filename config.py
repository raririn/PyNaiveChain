import os
from param import *

''' Environment config file. Find port and peers in os environment,
    give default value if not found. '''

try:
    port = int(os.environ['PORT'])
except Exception:
    port = HTTP_port
    print('No port found in environment.')

try:
    initialPeers = os.environ['PEERS'].split(",")
except Exception:
    initialPeers = []
    print('No initial peers found in environment.')