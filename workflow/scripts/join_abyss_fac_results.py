import numpy as np
import pandas as pd
import argparse

parser = argparse.ArgumentParser("")
parser.add_argument('--master', type=str) 
parser.add_argument('--abyss_out', type=str) 
parser.add_argument('--result',  type=str) 
args = parser.parse_args()

#big table
joined = pd.read_csv(args.master ,dtype='unicode')
#abyss-fac table
abyss = pd.read_table(args.abyss_out)
abyss['name_cut'] = abyss['name'].str.slice(2, 17)
abyss = abyss[~abyss['name'].str.contains('name')]
abyss_join = pd.merge(joined, abyss, left_on = 'genbank_assembly_accession', right_on='name_cut', how = 'outer')
abyss_join.drop(columns=['name_cut'],inplace=True)
abyss_join.to_csv(args.result)

    
#python3 {script} --master {input.master} --abyss_out {input.abyss_out} --result {output.master_abyss}