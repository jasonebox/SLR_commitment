#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 14:10:13 2020

@author: Jason Box, GEUS, jeb@geus.dk

Obtain SLR commitment dependence on summer air temperature via linear regression of 2000-2019 values...for glacier type combinations, but ultimately featuring the combined tidewater and land terminating result

before: /Users/jason/Dropbox/ELA/prog/imbalance_old/SLR_committed_ensemble.py
after: /Users/jason/Dropbox/ELA/prog/SLR_committed_ensemble_vs_ERA5_*.py

"""

import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import locale
locale.setlocale(locale.LC_ALL, '')  # Use '' for auto, or force e.g. to 'en_US.UTF-8'
from numpy.polynomial.polynomial import polyfit
from scipy import stats

fs=36 # fontsize
th=1 # default line thickness
# plt.rcParams['font.sans-serif'] = ['Georgia']
plt.rcParams['axes.facecolor'] = 'white'
plt.rcParams['axes.edgecolor'] = 'black'
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 1
plt.rcParams['grid.linewidth'] = 0.5
plt.rcParams['grid.color'] = "grey"
plt.rcParams["font.size"] = fs
plt.rcParams['figure.figsize'] = 13, 15

type_choice_name=['TW_only','LT_only','TW_and_LT']
type_choice_name2=['bTW_only','aLT_only','cTW_and_LT']
SMB_or_TMB='TMB'
versionx='20200320'
versionx='20200611'
cc=0

# ------------------------------------------------ loop over glacier type combinations
for type_choice_index in range(2,3):
    cc=0
    fns=['']*36

    # xerr=df_ensemble_std.mb

    fn='/Users/jason/Dropbox/ELA/stats/imbalance/_ensemble_mean.csv'+type_choice_name[type_choice_index]+'.csv'
    # fn='/Users/jason/Dropbox/ELA/stats/imbalance/SLR_committed_TW_and_LT_TMB_ALBhi_RACMO_unscaled_SID1.0_v'+versionx+'.csv' # test case
    os.system('ls -lF '+fn)
    # os.system('cat '+fn)
    df=pd.read_csv(fn, delimiter=",")
    # print(df.columns)
    # y=df.iloc[7,18:].values/362.
    y=df.iloc[7,18:].values.astype(float)/-362. # convert from Gt mass balance to eustatic sea level
    # y=np.asarray(y)
    # print(tots)
    
    fn='/Users/jason/Dropbox/ERA5/stats/ERA5_regional_Arctic_t2m_JJA.csv'
    era=pd.read_csv(fn, delimiter=",")
    # print(era.columns)
    v=((era.year>=1981)&(era.year<=2010)) # make SLR commitment relative to the 1981 to 2010 climate normal, according to WMO standards
    temp=era.Greenland
    x=(era.Greenland[21:].values)-np.mean(temp[v])

    fig = plt.gcf()
    ax = fig.add_subplot(111)
    plt.close()

    plt.scatter(x,y,s=100,c='w',label='lab')
    b, m = polyfit(x, y, 1)
    xx=np.linspace(np.min(x), np.max(x),2)
    yx=np.linspace(np.min(y), np.max(y),2)

    z, cov = np.polyfit(x, y, 1, cov=True)
    errs=np.sqrt(np.diag(cov))
    print("err",errs)
    
    # model = sm.OLS(x,y)
    # results = model.fit()
    # print(results.summary())
    # print("standard error of fit",results.bse)

    plt.plot(xx, yx, '--',color='grey',linewidth=th*2)
    plt.xlabel('June through August\nGreenland air temperature anomaly\nvs 1981-2010, $^{o}$C (ERA5) ')
    plt.ylabel('mm eustatic sea level commitment')
    
    coefs=stats.pearsonr(x,y)
    print("gradient = ",m)
    print("intercept = ",b)
    # print(coefs[0],1-coefs[1])
    
    plt.scatter(x, y, s=1250, facecolors='k', edgecolors='w',linewidth=th)

    yos_text=2
    # for i in range(0,20):
    #     # print(y)
    #     plt.text(x[i],y[i], str(f"{i:02d}"),horizontalalignment='center',verticalalignment='center',color='r')
    for i in range(0,20):
        # print(x[i], y[i])
        plt.text(x[i], y[i]-yos_text, str(f"{i:02d}"), \
          horizontalalignment='center',verticalalignment='center', \
          color='w',zorder=20,fontsize=24)
    props = dict(boxstyle='round', facecolor='w',edgecolor='grey',alpha=0.8)

    propsk = dict(boxstyle='round', fc='k',facecolor='k',edgecolor='grey',alpha=1)

    cc=0    ;   xx0=0.09    ;   yy0=0.97    ;   dy=0.06
    plt.text(xx0, yy0+cc*dy,'2 digit year',color='w',
        transform=ax.transAxes,#, fontsize=9
        verticalalignment='top', bbox=propsk)   
    
    cc=0    ;   xx0=0.32    ;   yy0=0.26    ;   dy=0.06
    plt.text(xx0, yy0+cc*dy,'correlation = '+str("%.3f"%coefs[0])+\
             '\n1-p > 0.999'\
             '\nSLR$_{commit}$ = '+str("%.0f"%m)+'±'+str("%.0f"%(errs[0]*1.96))+' mm/$^{o}$C '+str("%.0f"%b)+' mm'\
             '\n2000-2019 baseline'\
                 ,color='k',
        transform=ax.transAxes, fontsize=fs*0.8,
        verticalalignment='top', bbox=props)   
