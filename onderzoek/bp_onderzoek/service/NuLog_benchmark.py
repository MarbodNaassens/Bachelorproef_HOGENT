#!/usr/bin/env python

import sys

sys.path.append('../')
from parsers.NuLog import NuLogParser
from parsers.utils import evaluator

import os
import pandas as pd

input_dir = '../logs/'  # The input directory of log file
output_dir = './AttentionParserResult/'  # The output directory of parsing results

benchmark_settings = {
    'Orval': {
        'log_file': 'Orval/alert_ORVAL.log',
        'log_format': '<Date>T<Time> <Content>',
        'filters': '([ ])',
        'k': 15,
        'nr_epochs': 5,
        'num_samples': 0  
    },

    'WebLog': {
        'log_file': 'WebLog/weblog.txt',
        'log_format': '<IP>,\[<Date>:<Time>,<Content>,<Result>',
        'filters': '([ ])',
        'k': 15,
        'nr_epochs': 5,
        'num_samples': 0  
    },

    'Thunderbird': {
        'log_file': 'Thunderbird/Thunderbird_2k.log',
        'log_format': '<Label> <Timestamp> <Date> <User> <Month> <Day> <Time> <Location> <Component>(\[<PID>\])?: <Content>',
        'filters': '([\s(\d+\.){3}\d+])',
        'k': 15,
        'nr_epochs': 5,
        'num_samples': 0     
    },

    'Zookeeper': {
        'log_file': 'Zookeeper/Zookeeper_2k.log',
        'log_format': '<Date> <Time> - <Level>  \[<Node>:<Component>@<Id>\] - <Content>',
        'filters': '([\s(/|)(\d+\.){3,}\d+(:\d+)?])',
        'k': 50,
        'nr_epochs': 3,
        'num_samples': 0          
    },

    'Proxifier': {
        'log_file': 'Proxifier/Proxifier_2k.log',
        'log_format': '\[<Time>\] <Program> - <Content>',
        'filters': '([ ])',
        'k': 15,
        'nr_epochs': 5,
        'num_samples': 0 
    },

    'OpenSSH': {
        'log_file': 'OpenSSH/OpenSSH_2k.log',
        'log_format': '<Date> <Day> <Time> <Component> sshd\[<Pid>\]: <Content>',
        'filters': '([ ])',
        'k': 15,
        'nr_epochs': 5,
        'num_samples': 0  
    },

    'Linux': {
        'log_file': 'Linux/Linux_2k.log',
        'log_format': '<Month> <Date> <Time> <Level> <Component>(\[<PID>\])?: <Content>',
        'filters': '([\s(\d+\.){3}\d+, \s\d{2}:\d{2}:\d{2}])',
        'k': 50,
        'nr_epochs': 3,
        'num_samples': 0    
    },

    'Hadoop': {
        'log_file': 'Hadoop/Hadoop_2k.log',
        'log_format': '<Date> <Time> <Level> \[<Process>\] <Component>: <Content>', 
        'filters': '([\s(\d+\.){3}\d+])',
        'k': 50,
        'nr_epochs': 3,
        'num_samples': 0      
    },

    'BGL': {
        'log_file': 'BGL/BGL_2k.log',
        'log_format': '<Label> <Timestamp> <Date> <Node> <Time> <NodeRepeat> <Type> <Component> <Level> <Content>',
        'filters': '([ |:|\(|\)|=|,])|(core.)|(\.{2,})',
        'k': 50,
        'nr_epochs':3,
        'num_samples':0
    },

    'Andriod': {
        'log_file': 'Andriod/Andriod_2k.log',
        'log_format': '<Date> <Time>  <Pid>  <Tid> <Level> <Component>: <Content>',
        'filters': '([ |:|\(|\)|=|,|"|\{|\}|@|$|\[|\]|\||;])',
        'k': 25,
        'nr_epochs':5,
        'num_samples':5000
    },

    'OpenStack': {
        'log_file': 'OpenStack/OpenStack_2k.log',
        'log_format': '<Logrecord> <Date> <Time> <Pid> <Level> <Component> \[<ADDR>\] <Content>',
        'filters' : '([ |:|\(|\)|"|\{|\}|@|$|\[|\]|\||;])',
        'k':5,
        'nr_epochs':6,
        'num_samples':0
            
    },
    
    'HDFS': {
        'log_file': 'HDFS/HDFS_2k.log',
        'log_format': '<Date> <Time> <Pid> <Level> <Component>: <Content>',
        'filters': '(\s+blk_)|(:)|(\s)',
        'k':15,
        'nr_epochs':5,
        'num_samples':0
        },
    
    'Apache': {
        'log_file': 'Apache/Apache_2k.log',
        'log_format': '\[<Time>\] \[<Level>\] <Content>',
        'filters': '([ ])',
        'k':12,
        'nr_epochs':5,
        'num_samples':0
        },
    
    'HPC': {
        'log_file': 'HPC/HPC_2k.log',
        'log_format': '<LogId> <Node> <Component> <State> <Time> <Flag> <Content>',
        'filters': '([ |=])',
        'num_samples':0,
        'k':10,
        'nr_epochs':3
        },
    
    'Windows': {
        'log_file': 'Windows/Windows_2k.log',
        'log_format': '<Date> <Time>, <Level>                  <Component>    <Content>',
        'filters': '([ ])',
        'num_samples':0,
        'k':95,
        'nr_epochs':5   
        },
    
    'HealthApp': {
        'log_file': 'HealthApp/HealthApp_2k.log',
        'log_format': '<Time>\|<Component>\|<Pid>\|<Content>',
        'filters': '([ ])',
        'num_samples':0,
        'k':100,
        'nr_epochs':5 
        },
    
    'Mac': {
        'log_file': 'Mac/Mac_2k.log',
        'log_format': '<Month>  <Date> <Time> <User> <Component>\[<PID>\]( \(<Address>\))?: <Content>',
        'filters': '([ ])|([\w-]+\.){2,}[\w-]+',
        'num_samples':0,
        'k':300,
        'nr_epochs':10  
        },
    
    'Spark': {
        'log_file': 'Spark/Spark_2k.log',
        'log_format': '<Date> <Time> <Level> <Component>: <Content>', 
        'filters': '([ ])|(\d+\sB)|(\d+\sKB)|(\d+\.){3}\d+|\b[KGTM]?B\b|([\w-]+\.){2,}[\w-]+',
        'num_samples':0,
        'k':50,
        'nr_epochs':3
        },
}


for m in range(10):
    bechmark_result = []
    for dataset, setting in benchmark_settings.items():
        print('\n=== Evaluation on %s ===' % dataset)
        indir = os.path.join(input_dir, os.path.dirname(setting['log_file']))
        log_file = os.path.basename(setting['log_file'])

        parser = NuLogParser.LogParser(indir=indir, outdir=output_dir, filters=setting['filters'], k=setting['k'], log_format=setting['log_format'])
        parser.parse(log_file, nr_epochs=setting['nr_epochs'], num_samples=setting['num_samples'])

        f_measure, accuracy = evaluator.evaluate(
            groundtruth=os.path.join(indir, log_file + '_structured.csv'),
            parsedresult=os.path.join(output_dir, log_file + '_structured.csv')
        )
        bechmark_result.append([dataset, f_measure, accuracy])

    print('\n=== Overall evaluation results ===')
    df_result = pd.DataFrame(bechmark_result, columns=['Dataset', 'F_measure', 'Accuracy_ExactMatching'])
    df_result.set_index('Dataset', inplace=True)
    print(df_result)
    df_result.T.to_csv(output_dir+'NuLog_benchmark_result_run_'+str(m)+'.csv')
