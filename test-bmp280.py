#!/usr/bin/python3

import argparse
from bmp280 import BMP280
import signal
import time

parser = argparse.ArgumentParser(description='bmp280 test')
parser.add_argument('--output', action='store', type=str, default=None)
parser.add_argument('--frequency', action='store', type=int, default=None)
args = parser.parse_args()

bmp = BMP280()

outfile = None

if args.output:
    outfile = open(args.output, "w")

def cleanup(_signo, _stack):
    if outfile:
        outfile.close()
    exit(0)


signal.signal(signal.SIGTERM, cleanup)
signal.signal(signal.SIGINT, cleanup)

while True:
    data = bmp.get_data()
    output = f"{time.time()} 1 {data.pressure} {data.temperature} {data.pressure_raw} {data.temperature_raw}"
    print(output)
    if outfile:
        outfile.write(output)
        outfile.write('\n')
    if args.frequency:
        time.sleep(1.0/args.frequency)
