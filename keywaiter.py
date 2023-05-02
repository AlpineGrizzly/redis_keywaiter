# MIT License
# 
# Copyright (c) 2023 Dalton Kinney
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys, argparse, redis, time

class RedisServer: 
    """ Class to represent information for Redis Server """
    def __init__(self, ip, port, udelay):
        self.ip = ip
        self.port = port
        self.udelay = udelay
    
def getargs(parser):
    """
    getargs Get arguments from the command line
    
    :parser: Parser object that holds arguments

    return: Returns parsed arguments
    """
    parser.add_argument('--help', '-h', action='help', help='Displays this information')
    parser.add_argument('redis_server', metavar="<serverip:port>", help="Ip address and port number of Redis server")
    parser.add_argument('keyname', metavar="<key>", help="Name of the key to query Redis of its existence")
    parser.add_argument('udelay', metavar="<udelay>", help="Microseconds to delay between each query")

    return parser.parse_args()

def redis_connect(ip, port):
    """
    redis_connect Connects to the redis server 
    
    :redis_server: Array containing redis server IP and port 

    return: Returns redis server object if successful, false otherwise
    """
    r = redis.Redis(
        host=ip,
        port=port,
        db=0)

    try: # to ping the Redis server to ensure we have a valid connection
        r.ping()
        return r
    except Exception as e:
        sys.stderr.write("Error: %s\n" % e) # Quite informative error message
        sys.exit(1)

def wait_for_key(redis, keyname, udelay):
    """ 
    wait_for_key Wait for a key to exist, return value of key when found 
    
    :redis: Pointer to instance of redis
    :keyname: Name of key we are waiting to exist in Redis datastore
    :udelay: Microseconds to wait between each check

    return: Returns value of key when found to exist
    """
    key_value = None

    while True:
        key_value = redis.get(keyname)# Query for key
        if(key_value != None):
            return key_value
        time.sleep(int(udelay) / 10**6) # Wait between each query
    
def main(): 
    parser = argparse.ArgumentParser(description="Wait for a key to appear in Redis", add_help=False)
    args = getargs(parser)

    # Get IP and port of Redis server
    redis_conn_info = args.redis_server.split(":") # IP:PORT -> [IP][PORT]
    if(len(redis_conn_info) != 2):
        parser.print_help()        
        sys.exit(0) # Server and IP incorrect format, exit
    
    rserver = RedisServer(redis_conn_info[0], redis_conn_info[1], args.udelay)
    redis_instance = redis_connect(rserver.ip, rserver.port)
    key_value = wait_for_key(redis_instance, args.keyname, rserver.udelay)

    print("%s: %s\n" % (args.keyname, key_value.decode("utf-8")))

if __name__ == "__main__":
    main()