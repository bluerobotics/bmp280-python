#!/usr/bin/python3

import matplotlib.pyplot as plt

def generate_figures(log):
    footer = 'bmp280 test report'

    f, spec = log.figure(height_ratios=[1,1], suptitle='bmp280 data', footer=footer)
    plt.subplot(spec[0,0])
    log.rom.T.ttable(rl=True)
    plt.subplot(spec[0,1])
    log.config.T.ttable(rl=True)

    plt.subplot(spec[1,:])
    log.data.pressure.pplot(log.data.temperature)

if __name__ == '__main__':
    import argparse
    from llog import LLogReader
    from matplotlib.backends.backend_pdf import PdfPages
    import os

    dir_path = os.path.dirname(os.path.realpath(__file__))

    defaultMeta = dir_path + '/bmp280.meta'
    parser = argparse.ArgumentParser(description='bmp280 test report')
    parser.add_argument('--input', action='store', type=str, required=True)
    parser.add_argument('--meta', action='store', type=str, default=defaultMeta)
    parser.add_argument('--output', action='store', type=str)
    parser.add_argument('--show', action='store_true')
    args = parser.parse_args()

    log = LLogReader(args.input, args.meta)

    generate_figures(log)

    if args.output:
        # todo check if it exists!
        with PdfPages(args.output) as pdf:
            [pdf.savefig(n) for n in plt.get_fignums()]

    if args.show:
        print('hello?')
        plt.show()
