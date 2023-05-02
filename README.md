# redis_keywaiter
Waits for a key to exist in a target Redis database

## Usage
Connect to the Redis server on local host at port `6379` and query every `100` microseconds
for the existence of `thiskey`. Once the key exists, it will print the keyvalue out to stdout.
```
python3 keywaiter.py 127.0.0.1:6379 thiskey 100
```

