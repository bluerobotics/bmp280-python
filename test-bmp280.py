#!/usr/bin/python3

import argparse
from bmp280 import BMP280
from llog import LLogWriter, LLOG_DATA
import signal
import time
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

defaultMeta = dir_path + '/bmp280.meta'

parser = argparse.ArgumentParser(description='bmp280 test')
parser.add_argument('--output', action='store', type=str, default=None)
parser.add_argument('--meta', action='store', type=str, default=defaultMeta)
parser.add_argument('--frequency', action='store', type=int, default=None)
args = parser.parse_args()

log = LLogWriter(args.meta, args.output)

def cleanup(_signo, _stack):
    log.close()
    exit(0)

signal.signal(signal.SIGTERM, cleanup)
signal.signal(signal.SIGINT, cleanup)

bmp = BMP280()

while True:
    data = bmp.get_data()
    output = f"{data.pressure} {data.temperature} {data.pressure_raw} {data.temperature_raw}"
    log.log(LLOG_DATA, output)
    if args.frequency:
        time.sleep(1.0/args.frequency)
