#!/usr/bin/python3

from bmp280 import BMP280
import argparse
import time

parser = argparse.ArgumentParser(description='bmp280 test')
parser.add_argument('--output', action='store', type=str, default=None)
parser.add_argument('--frequency', action='store', type=int, default=None)
args = parser.parse_args()

bmp = BMP280()

if args.output:
    outfile = open(args.output, "w")

while True:
    data = bmp.get_data()
    output = f"{time.time()} 1 {data.pressure} {data.temperature} {data.pressure_raw} {data.temperature_raw}"
    print(output)
    if args.output:
        outfile.write(output)
        outfile.write('\n')
    if args.frequency:
        time.sleep(1.0/args.frequency)

# this is never reached, but works anyway in practice
# todo handle KeyboardInterrupt for ctrl+c
if args.output:
    outfile.close()
