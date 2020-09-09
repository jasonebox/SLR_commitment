#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 14:10:13 2020

@author: Jason Box, GEUS, jeb@geus.dk

per sector ensemble average, from the error propagation approach, of SLR summaries

before: /Users/jason/Dropbox/ELA/prog/AAR_vs_MB_*.py
after /Users/jason/Dropbox/ELA/prog/SLR_committed.py
    /Users/jason/Dropbox/ELA/prog/SLR_committed_ensemble.py

"""

import matplotlib.pyplot as plt
# import numpy as np
import os
import pandas as pd
import locale
locale.setlocale(locale.LC_ALL, '')  # Use '' for auto, or force e.g. to 'en_US.UTF-8'

def reorder_jeb(df,names):
    df["name"]=names
    cols = df.columns.tolist() # get a list of columns
    cols.insert(0, cols.pop(cols.index('name')))   # move the column to head of list using index, pop and insert
    df = df.reindex(columns= cols)
    return df

# plt.rcParams['font.sans-serif'] = ['Georgia']
plt.rcParams['axes.facecolor'] = 'white'
plt.rcParams['axes.edgecolor'] = 'black'
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 1
plt.rcParams['grid.color'] = "grey"
plt.rcParams["font.size"] = 10

type_choice_name=['TW_only','LT_only','TW_and_LT']
SMB_or_TMB='TMB'
versionx='20200320'
versionx='20200716'
# versionx='20200611'

n_members='_6_members'
n_members='_2_members'
n_members='_18_members'
# # ------------------------------------------------ loop over treatments
# for jj in range(0,3):
#     if jj==0:
#         typechoice='TW'
#         type_choice_name='TW_only'
#     if jj==1:
#         typechoice='LT'
#         type_choice_name='LT_only'
#         if typechoice=='LT':
#             for k in range(0,n):
#                 if gl_type[k]=='ice_cap':
#                     print('ice cap is LT',name[k])
#                     gl_type[k]='LT'                
#     if jj==2:
#         typechoice='all'
#         type_choice_name='TW_and_LT'
#         if typechoice=='all':
#             for k in range(0,n):
#                 gl_type[k]='all'

for gamma_index in range(0,2):    
    gamma=1.
    gamma_name='_gamma1.0'
    
    if gamma_index:
        gamma=1.25
        gamma_name='_gamma1.25'

    # ------------------------------------------------ loop over glacier type combinations
    for type_choice_index in range(2,3):
        cc=0
        fns=['']*18
        # ------------------------------------------------ loop over SID uncertainty
        SID_devname=["0.9","1.0","1.1","const"]
        
        for SID_dev_index in range(0,3):
        # for SID_dev_index in range(1,2):
        # for SID_dev_index in range(3,4):
            # ------------------------------------------------ loop over volume treatments
            volume_name=['unscaled','scaled']
            # for volume_index in range(0,2):
            for volume_index in range(0,1):
            
                # ------------------------------------------------ loop over RCMs
                RCM=['MAR','RACMO']
                for mm in range(0,2):
                # for mm in range(1,2):
                # for mm in range(1,2):
                    
                # ------------------------------------------------ loop over albedo uncertainty
                    alb_devname=["lo","mid","hi"]
                    for alb_dev_index in range(0,3):
                    # for alb_dev_index in range(1,2):
                        fn='/Users/jason/Dropbox/ELA/stats/imbalance/imbalance_'+\
                            SMB_or_TMB+'_ALB'+alb_devname[alb_dev_index]+'_'+RCM[mm]+'_'+\
                                volume_name[volume_index]+'_SID'+SID_devname[SID_dev_index]+\
                                    gamma_name+\
                                    '_v'+versionx+'.csv'
                        os.system('ls -lF '+fn)
                        print(cc,fn)
                        member = pd.read_csv(fn, delimiter=",")
                        fns[cc]=fn
                        cc+=1
    
        cols=member.columns
        # print(cc)
        # break
        cc=0
        # os.system('ls -lF '+fns[0])
        df1 = pd.read_csv(fns[cc], delimiter=",") ; cc+=1
        df2 = pd.read_csv(fns[cc], delimiter=",") ; cc+=1
        df3 = pd.read_csv(fns[cc], delimiter=",") ; cc+=1
        df4 = pd.read_csv(fns[cc], delimiter=",") ; cc+=1
        df5 = pd.read_csv(fns[cc], delimiter=",") ; cc+=1
        df6 = pd.read_csv(fns[cc], delimiter=",") ; cc+=1
        
        df7 = pd.read_csv(fns[cc], delimiter=",") ; cc+=1
        df8 = pd.read_csv(fns[cc], delimiter=",") ; cc+=1
        df9 = pd.read_csv(fns[cc], delimiter=",") ; cc+=1
        df10 = pd.read_csv(fns[cc], delimiter=",") ; cc+=1
        df11 = pd.read_csv(fns[cc], delimiter=",") ; cc+=1
        df12 = pd.read_csv(fns[cc], delimiter=",") ; cc+=1
        
        df13 = pd.read_csv(fns[cc], delimiter=",") ; cc+=1
        df14 = pd.read_csv(fns[cc], delimiter=",") ; cc+=1
        df15 = pd.read_csv(fns[cc], delimiter=",") ; cc+=1
        df16 = pd.read_csv(fns[cc], delimiter=",") ; cc+=1
        df17 = pd.read_csv(fns[cc], delimiter=",") ; cc+=1
        df18 = pd.read_csv(fns[cc], delimiter=",") ; cc+=1
        
        # df19 = pd.read_csv(fns[cc], delimiter=",") ; cc+=1
        # df20 = pd.read_csv(fns[cc], delimiter=",") ; cc+=1
        # df21 = pd.read_csv(fns[cc], delimiter=",") ; cc+=1
        # df22 = pd.read_csv(fns[cc], delimiter=",") ; cc+=1
        # df23 = pd.read_csv(fns[cc], delimiter=",") ; cc+=1
        # df24 = pd.read_csv(fns[cc], delimiter=",") ; cc+=1
        
        # df25 = pd.read_csv(fns[cc], delimiter=",") ; cc+=1
        # df26 = pd.read_csv(fns[cc], delimiter=",") ; cc+=1
        # df27 = pd.read_csv(fns[cc], delimiter=",") ; cc+=1
        # df28 = pd.read_csv(fns[cc], delimiter=",") ; cc+=1
        # df29 = pd.read_csv(fns[cc], delimiter=",") ; cc+=1
        # df30 = pd.read_csv(fns[cc], delimiter=",") ; cc+=1
        
        # df31 = pd.read_csv(fns[cc], delimiter=",") ; cc+=1
        # df32 = pd.read_csv(fns[cc], delimiter=",") ; cc+=1
        # df33 = pd.read_csv(fns[cc], delimiter=",") ; cc+=1
        # df34 = pd.read_csv(fns[cc], delimiter=",") ; cc+=1
        # df35 = pd.read_csv(fns[cc], delimiter=",") ; cc+=1
        # df36 = pd.read_csv(fns[cc], delimiter=",") ; cc+=1
        
        df_concat = pd.concat((df1,df2,
                               df3,df4,df5,df6,\
                                df7,df8,df9,df10,df11,df12,\
                                 df13,df14,df15,df16,df17,df18,\
                                # df19,df20,df21,df22,df23,df24,\
                                # df25,df26,df27,df28,df29,df30,\
                                # df31,df32,df33,df34,df35,df36,\
                                   ))
        
        by_row_index = df_concat.groupby(df_concat.index)
        # df_ensemble_count = by_row_index.count()
        # df_ensemble_count.to_csv('/Users/jason/Dropbox/ELA/stats/imbalance/_ensemble_imbalance_count'+type_choice_name[type_choice_index]+'.csv', sep=',')
        
        # df_ensemble_min = by_row_index.min()
        # df_ensemble_min.to_csv('/Users/jason/Dropbox/ELA/stats/imbalance/_ensemble_imbalance_min.csv', sep=',')
        
        # df_ensemble_max = by_row_index.max()
        # df_ensemble_max.to_csv('/Users/jason/Dropbox/ELA/stats/imbalance/_ensemble_imbalance_max'.csv', sep=',')
        
        df_ensemble_std = by_row_index.std()
        df_ensemble_std=reorder_jeb(df_ensemble_std,member.name)
        df_ensemble_std["type"]=member.type
        df_ensemble_std["region"]=member.region
        df_ensemble_std.to_csv('/Users/jason/Dropbox/ELA/stats/imbalance/_ensemble_imbalance_std'+n_members+gamma_name+'.csv', sep=',')
        print(df_ensemble_std.columns)
        print(len(df_ensemble_std.columns))
        
        df_ensemble_mean = by_row_index.mean()
        df_ensemble_mean=reorder_jeb(df_ensemble_mean,member.name)
        df_ensemble_mean["type"]=member.type
        df_ensemble_mean["region"]=member.region
        df_ensemble_mean.to_csv('/Users/jason/Dropbox/ELA/stats/imbalance/_ensemble_imbalance_mean'+n_members+gamma_name+'.csv', sep=',')
        print(df_ensemble_mean.columns)
        print(len(df_ensemble_mean.columns))    
    
   