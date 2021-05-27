#!/usr/bin/python3

import argparse
from datetime import datetime
from fpdf import FPDF
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd

WIDTH = 210
HEIGHT = 297

file_path = './tmp/'
if not os.path.exists(file_path):
    os.makedirs(file_path)

# TODO Can I put this into a function?
parser = argparse.ArgumentParser(description='bmp280 test')
parser.add_argument('--input', action='store', type=str, required=True)
parser.add_argument('--output', action='store', type=str, required=True)
args = parser.parse_args()

data = pd.read_csv(args.input, header=None, sep=' ')
data.rename(columns={0: "Timestamp", 1: "Log_Type"}, inplace=True)
data['Timestamp'] = pd.to_datetime(data['Timestamp'], unit='s')
print(data.head())

measurements = pd.DataFrame(data=data.query('Log_Type == 1'))
measurements.rename(columns={2: "Pressure", 3: "Temperature", 4: "Pressure Raw", 5: "Temperature Raw"}, inplace=True)


configuration = pd.DataFrame(data=data.query('Log_Type == 2'))
configuration.rename(columns={2: 'CTRL Register Byte', 3: 'CFG Register Byte', 4: "Comp 1", 4: "Comp 2"}, inplace=True)

errors = pd.DataFrame(data=data.query('Log_Type == 0'))
errors.rename(columns={2: 'Error Message'}, inplace=True)


def generate_table():
    # Calib and errors
    ctrl_const = None
    ctrl = None
    cfg_const = None
    cfg = None
    error_list = None
    ts_list = None

    # TODO - make this simpler?
    if not configuration.empty:
        first_last_config = configuration.iloc[[0, -1]]
        if first_last_config['CTRL Register Byte'].iloc[0] == first_last_config['CTRL Register Byte'].iloc[1]:
            # gain settings unchanged during test
            ctrl_const = True
            ctrl = first_last_config['CTRL Register Byte'].iloc[0]
        if first_last_config['CFG Register Byte'].iloc[0] == first_last_config['CFG Register Byte'].iloc[1]:
            # odr settings unchanged during test
            cfg_const = True
            cfg = first_last_config['CFG Register Byte'].iloc[0]
        else:
            ctrl_const = False
            cfg_const = False

    if not errors.empty:
        error_list = errors['Error Message'].tolist()
        ts_list = errors['Timestamps'].to_list()

    # Measurement table
    mean_t = round(measurements['Temperature'].mean(), 3)
    mean_p = round(measurements['Pressure'].mean(), 3)

    min_t = round(measurements['Temperature'].min(), 3)
    min_p = round(measurements['Pressure'].min(), 3)

    max_t = round(measurements['Temperature'].max(), 3)
    max_p = round(measurements['Pressure'].max(), 3)

    std_t = round(measurements['Temperature'].std(), 3)
    std_p = round(measurements['Pressure'].std(), 3)

    return mean_t, mean_p, min_t, min_p, max_t, max_p, std_t, std_p, ctrl_const, ctrl, cfg_const, cfg, error_list, \
           ts_list


def generate_figures(filename=args.output):
    color1 = ["#FFA630", "#4DA1A9", "#611C35", "#2E5077"]
    color2 = ["#D7E8BA"]

    measurements.plot(kind='line', x='Timestamp', y='Temperature', color=color1)
    label_fig('Timestamp', 'Temperature', 'Temperature on BMP')
    plt.savefig(fname=file_path+'bmp_0.png')
    plt.close()

    measurements.plot(kind='line', x='Timestamp', y='Pressure', color=color1)
    label_fig('Timestamp', 'Pressure', 'Presure on BMP')
    plt.savefig(fname=file_path + 'bmp_1.png')
    plt.close()

    # Plot current vs voltage
    measurements.plot(kind='line', x='Timestamp', y='Temperature', color=color1)
    label_fig('Timestamp', 'Temperature', 'Pressure and Temperature')
    ax2 = plt.twinx()
    measurements.plot(kind='line', x='Timestamp', y='Pressure', color=color2, ax=ax2)
    ax2.legend(loc="upper left")
    ax2.set_ylabel('Pressure')

    plt.savefig(fname=file_path+'bmp_2.png')
    plt.close()


def label_fig(x, y, title):
    # TODO - create dict for columns to X and Y axis labels
    plt.title(f"{title}")
    plt.ylabel(f"{y}")
    plt.xlabel(f"{x}")


def table_helper(pdf, epw, th, table_data, col_num):
    for row in table_data:
        for datum in row:
            # Enter data in columns
            pdf.cell(epw/col_num, 2 * th, str(datum), border=1)
        pdf.ln(2 * th)


def init_report(filename=args.output):
    mean_t, mean_p, min_t, min_p, max_t, max_p, std_t, std_p, ctrl_const, ctrl, cfg_const, cfg, error_list, ts_list = \
        generate_table()

    config_data = [['', 'Ctrl Register Byte', 'Cfg Register Byte'], ['Value', ctrl, cfg], ['Constant Config',
                                                                                           ctrl_const, cfg_const]]
    error_data = [ts_list, error_list]

    table_data = [['Parameter', 'Mean', 'Min', 'Max', 'Std'], ['Temperature', mean_t, min_t, max_t, std_t],
                  ['Pressure', mean_p, min_p, max_p, std_p]]

    result_data = [[None]] # TODO add the required pass/fails for 9.6 in nav
    pdf = FPDF()
    epw = pdf.w - 2*pdf.l_margin
    pdf.add_page()

    pdf.set_font('Helvetica', '', 10.0)
    th = pdf.font_size

    if None not in result_data:
        pdf.set_font('Helvetica', '', 14.0)
        pdf.cell(WIDTH, 0.0, 'Summary of BMP Test', align='C')
        pdf.set_font('Helvetica', '', 10.0)
        pdf.ln(5)
        table_helper(pdf, epw, th, result_data, 3)
        pdf.ln(5)

    if None not in config_data:
        pdf.set_font('Helvetica', '', 12.0)
        pdf.cell(WIDTH, 0.0, 'Summary of BMP Test Configurations', align='C')
        pdf.set_font('Helvetica', '', 10.0)
        pdf.ln(5)
        table_helper(pdf, epw, th, config_data, 3)
        pdf.ln(5)

    if None not in error_data:
        pdf.set_font('Helvetica', '', 12.0)
        pdf.cell(WIDTH, 0.0, 'Summary of BMP Test Errors', align='C')
        pdf.set_font('Helvetica', '', 10.0)
        pdf.ln(5)
        table_helper(pdf, epw, th, error_data, len(error_list))
        pdf.ln(5)

    if None not in table_data:
        pdf.set_font('Helvetica', '', 12.0)
        pdf.cell(WIDTH, 0.0, 'Summary of BMP Test Measurements', align='C')
        pdf.set_font('Helvetica', '', 10.0)
        pdf.ln(5)
        table_helper(pdf, epw, th, table_data, 5)
        pdf.ln(5)

    # Add images
    pdf.image("./tmp/bmp_0.png", 5, 85, WIDTH/2-10)
    pdf.image("./tmp/bmp_1.png", WIDTH/2, 85, WIDTH/2-10)
    pdf.image("./tmp/bmp_2.png", 5, 150, WIDTH - 10)

    pdf.output(filename, 'F')


if __name__ == '__main__':
    print("Post-Processing Script")
    generate_table()
    generate_figures()
    init_report()
