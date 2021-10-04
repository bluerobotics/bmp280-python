#!/usr/bin/python3

from bmp280 import BMP280
from llog import LLogWriter

device = "bmp280"
parser = LLogWriter.create_default_parser(__file__, device)
args = parser.parse_args()

with LLogWriter(args.meta, args.output, console=args.console) as log:
    bmp = BMP280()
    compensation = bmp.get_compensation()
    log.log_rom(' '.join(str(d) for d in compensation.data))
    log.log_config(f'{bmp.osrs_t} {bmp.osrs_p} {bmp.mode} {bmp.t_sb} {bmp.filter}')
    
    def data_getter():
        data = bmp.get_data()
        return f'{data.pressure} {data.temperature} {data.pressure_raw} {data.temperature_raw}'
    log.log_data_loop(data_getter, parser_args=args)
