import sys
sys.path.append('../')
from parsers import Drain, evaluator
import os
import pandas as pd


input_dir = '../logs/' # The input directory of log file
output_dir = 'Drain_stream_result/' # The output directory of parsing results

benchmark_settings = {
    'HDFS': {
        'log_file': 'HDFS/HDFS_2k.log',
        'log_format': '<Date> <Time> <Pid> <Level> <Component>: <Content>',
        'regex': [r'blk_-?\d+', r'(\d+\.){3}\d+(:\d+)?'],
        'st': 0.5,
        'depth': 4
    },
}

bechmark_result = []
for dataset, setting in benchmark_settings.items():
    print('\n=== Evaluation on %s ==='%dataset)
    indir = os.path.join(input_dir, os.path.dirname(setting['log_file']))
    log_file = os.path.basename(setting['log_file'])

    parser = Drain.LogParser(log_format=setting['log_format'], indir=indir, outdir=output_dir, rex=setting['regex'], depth=setting['depth'], st=setting['st'])
    with open('../logs/HDFS/HDFS_2k.log') as file:
        lines = file.readlines()

    for i in range(len(lines)):
        parser.parse(lines[i])
