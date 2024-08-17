#test0817
import pandas as pd
import numpy as np
import copy
import argparse
from FSW_diff_alpha_function import FSW_diff_alpha_algorithm
from DJ_diff_alpha_function import DJ_diff_alpha_algorithm
from SemiOpt_diff_alpha_function import SemiOpt_diff_alpha_algorithm
import error_measure as em

def args():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('--datapath',
                        type=str,
                        default='new_data/A1_10',
                        help='Path to the dataset')          
    parser.add_argument('--id_data',
                        type=int,
                        default=0,
                        help='Dataset ID')        
    parser.add_argument('--eps',
                        type=float,
                        default=0.03,
                        help='The global error bound epsilon_0')    
    parser.add_argument('--alpha',
                        type=float,
                        default=0.2,
                        help='The scarling factor alpha in AEPLA')    
    parser.add_argument('--alg',
                        type=str,
                        default='o',
                        help='AEPLA or original PLA methods, `p` means AEPLA, `o` means original PLA methods')      
    parser.add_argument('--method',
                        type=str,
                        default='',
                        help='User-specified PLA methods, FSW for instance')         
    args = parser.parse_args()    
    return args

# read arguments

arguments = args()

# read data
dataset = pd.read_csv(arguments.datapath+'.csv')
print('***id_data={}***'.format(arguments.id_data))
data_source = dataset.loc[arguments.id_data,'datapoints'].split(',')
for j in range(0,len(data_source)):
    data_source[j] = float(data_source[j])   
data_source = np.array(data_source)    
timeseries_total = copy.deepcopy(data_source)          

# run AEPLA
if arguments.method == 'FSW':
    segment_total = FSW_diff_alpha_algorithm(arguments.eps, timeseries_total, arguments.alpha, arguments.alg)
    error_total = em.error_measure_function(segment_total,timeseries_total)
elif arguments.method == 'DJ':
    segment_total = DJ_diff_alpha_algorithm(arguments.eps, timeseries_total, arguments.alpha, arguments.alg)
    error_total = em.error_measure_function(segment_total,timeseries_total)
elif arguments.method == 'SemiOpt':
    segment_total = SemiOpt_diff_alpha_algorithm(arguments.eps, timeseries_total, arguments.alpha, arguments.alg)
    error_total = em.error_measure_function_SemiOpt(segment_total,timeseries_total)
else:
    print('Working on adding new methods...')
    
