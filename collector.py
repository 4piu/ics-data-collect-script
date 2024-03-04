#!/usr/bin/env python3
# Run this on a standalone machine
import csv
import json
import os.path
import socket

from flatdict import FlatDict

LISTEN = ('0.0.0.0', 3001)


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(LISTEN)
    while True:
        data, addr = sock.recvfrom(512)  # buffer size is 512 bytes
        # print(f"recv {len(data)}B msg: {data}")
        sample = FlatDict(json.loads(data), delimiter='.')
        print(sample)
        if not os.path.exists(f"data/{sample['src']}.csv"):
            with open(f"data/{sample['src']}.csv", "a") as f:
                csv.writer(f).writerow(sample.keys())
        with open(f"data/{sample['src']}.csv", "a") as f:
            csv.writer(f).writerow(sample.values())

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("exit")
        pass
