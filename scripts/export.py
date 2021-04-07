#!/usr/bin/env python3

import argparse
import glob
import os
import json
import pandas as pd
from datetime import datetime


parser = argparse.ArgumentParser(description='"Export SalivApp data."')
parser.add_argument('data_dir', metavar='data_dir', type=str,
                    help='directory containing the participant-specific sub-directories with data.json')
parser.add_argument('-c', "--csv", dest="outcsv", action="store", default=None,
                    help='Output csv file name name. (default: None)')
parser.add_argument("-e", "--excel", dest="outexcel", action="store", default=None,
                    help='Output Excel speadsheet file name name. (default: None)')

args = parser.parse_args()

if __name__ == '__main__':

    # read all data
    jsons = glob.glob( os.path.join(args.data_dir,'*/data.json'))

    rows_list = []
    for js in jsons:
        with open(js, "r") as read_file:
            participant_id = js.split('/')[-2]
            try:
                data = json.load(read_file)
            except json.JSONDecodeError:
                rows_list.append([participant_id, "n/a", "n/a",
                                  "n/a", "n/a"])
            else:
                for d in data:
                    dt = datetime.fromtimestamp(d['timestamp'])
                    rows_list.append([participant_id, d['barcode'], d['timestamp'],
                                      dt.date(), dt.time()])

    df = pd.DataFrame(rows_list, columns=['participant_id', 'barcode_id', 'timestamp', 'date', 'time'])

    print(df)

    if args.outcsv:
        df.to_csv(args.outcsv)

    if args.outexcel:
        df.to_excel(args.outexcel)