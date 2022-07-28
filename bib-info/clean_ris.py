import numpy as np
import pandas as pd
import tqdm
import re

## step 1: extract AU fields from ris

SN_list = []
INI_list = []

with open('Oxford_Thesis_biber.ris','r') as f:
    for line in f:
        if line[:2] == 'AU':
            
            items = line[6:].strip()
            items = items.split(',')
            sn = items[0].strip()
            
            if len(items)>1:
                ini = ','.join(items[1:]).strip()
                ini = ''.join([x.strip()[0] for x in re.split(' |. ',','.join(items[1:]).strip()) if x])
            else:
                ini = ''

            SN_list+=[sn]
            INI_list+=[ini]

## step 2: copy lists to dataframe

au_df = pd.DataFrame([INI_list,SN_list],index=['ini','sn']).T

## step 3: extract repeats & overwrite in dataframe

repeats = []

for row,s in tqdm.tqdm(au_df.iterrows()):
    
    if row in repeats:
        continue
    
    ini = s.loc['ini']
    sn = s.loc['sn']
    
    entries = au_df.loc[(au_df.sn==sn) & (au_df.ini.str[:len(ini)] == ini)]
    
    idx = entries.index.tolist()
    
    benchmark = entries.loc[entries.ini.str.len().idxmax()]
    
    au_df.loc[idx,'ini'] = benchmark.ini
    au_df.loc[idx,'sn'] = benchmark.sn
    
    repeats += idx

## step 4: re-write ris file

au_num = 0
with open('Oxford_Thesis_biber.ris','r') as f:
    
    f1 = open('Oxford_Thesis_biber_clean.ris','w')
    
    for line in f:
        if line[:2] != 'AU':
            f1.write(line)
            
        else:
            ini,sn = au_df.loc[au_num]
            f1.write('AU  - '+sn+', '+'. '.join(ini)+'.\n')
            au_num += 1
