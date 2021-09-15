#!/usr/bin/python3

import argparse
from bmp280 import BMP280
from llog import LLogWriter, LLOG_DATA, LLOG_CONFIG, LLOG_ROM
import time
from pathlib import Path

device = "bmp280"
defaultMeta = Path(__file__).resolve().parent / f"{device}.meta"

parser = argparse.ArgumentParser(description=f'{device} test')
parser.add_argument('--output', action='store', type=str, default=None)
parser.add_argument('--meta', action='store', type=str, default=defaultMeta)
parser.add_argument('--frequency', action='store', type=int, default=None)
args = parser.parse_args()

with LLogWriter(args.meta, args.output) as log:
    bmp = BMP280()
    compensation = bmp.get_compensation()
    log.log(LLOG_ROM, ' '.join(str(d) for d in compensation.data))
    log.log(LLOG_CONFIG, f'{bmp.osrs_t} {bmp.osrs_p} {bmp.mode} {bmp.t_sb} {bmp.filter}')
    while True:
        data = bmp.get_data()
        output = f'{data.pressure} {data.temperature} {data.pressure_raw} {data.temperature_raw}'
        log.log(LLOG_DATA, output)
        if args.frequency:
            time.sleep(1.0/args.frequency)