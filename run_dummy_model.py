#!/usr/bin/python3
import json
import sys
import argparse
from datetime import datetime

import warnings
warnings.simplefilter('ignore')

import pandas as pd
from tqdm import tqdm

from zcor_dummy.classifier import load_classifier_object
from zcor_dummy.utils import json_to_row

parser = argparse.ArgumentParser(description='Run ZCoR object.')

parser.add_argument('-p', '--predictor',
                    type=str, default=True, dest = "PREDICTOR_FILE",
                    help='Path to predictor object file.')
parser.add_argument('-i', '--input_data',
                    type=str, default=True, dest = "INPUT_DATA_FILE",
                    help='Path to input data folder. Must only contain the data files to be used for the run.')
parser.add_argument('-o', '--out_path',
                    type=str, default="", dest = "OUT_PATH",
                    help='Path to save predictions file to')
parser.add_argument('-v', '--verbose',
                    type=bool, default=False, dest = "VERBOSE",
                    help='Verbosity of the run')

if len(sys.argv[1:]) == 0:
    parser.print_help()
    parser.exit()
args = parser.parse_args()

RUN_NAME = datetime.now().strftime('%m-%d-%y-%H-%M')

PREDICTOR = load_classifier_object(args.PREDICTOR_FILE)

with open(args.INPUT_DATA_FILE, 'r') as json_file:
    raw_json_data = json.load(json_file)

converted_data = pd.DataFrame([json_to_row(i) for i in tqdm(raw_json_data,
                                                            "Convert to native format",
                                                            position = 0,
                                                            leave = True,
                                                            disable = not args.VERBOSE)])

json_predictions = PREDICTOR.deliver_predictions(converted_data, VERBOSE = args.VERBOSE)

if args.OUT_PATH:
    with open(args.OUT_PATH, 'w') as file:
        json.dump(json_predictions, file, indent = 4)
else:
    print(json_predictions)

