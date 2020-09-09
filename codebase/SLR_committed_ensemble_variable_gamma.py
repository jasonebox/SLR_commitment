#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 14:10:13 2020

@author: Jason Box, GEUS, jeb@geus.dk

Make ensemble average, from the error propagation approach, of SLR summaries

preceded by /Users/jason/Dropbox/ELA/prog/SLR_committed.py
after: /Users/jason/Dropbox/ELA/prog/SLR_committed_ensemble_vs_ERA5.py
    
"""

import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import locale
locale.setlocale(locale.LC_ALL, '')  # Use '' for auto, or force e.g. to 'en_US.UTF-8'
from numpy.polynomial.polynomial import polyfit
from scipy import stats
import matplotlib.colors

def detrend_lin(x,y):
    b, m = polyfit(x, y, 1)
#    print(x)
#    print(y)
    y_detrended=y-(m*x+b)
    return y_detrended

fs=24 ; th=1
# plt.rcParams['font.sans-serif'] = ['Georgia']
plt.rcParams['axes.facecolor'] = 'white'
plt.rcParams['axes.edgecolor'] = 'black'
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 1
plt.rcParams['grid.color'] = "grey"
plt.rcParams["font.size"] = fs

type_choice_name=['TW_only','LT_only','TW_and_LT']
type_choice_name2=['bTW_only','aLT_only','cTW_and_LT']
SMB_or_TMB='TMB'
versionx='20200320'
versionx='20200611'
cc=0

for gamma_index in range(0,2):    
    gamma=1.
    gamma_name='_gamma1.0'
    
    if gamma_index:
        gamma=1.25
        gamma_name='_gamma1.25'
    # ------------------------------------------------ loop over glacier type combinations
    # for type_choice_index in range(0,3):
    for type_choice_index in range(2,3):
        cc=0
        fns=['']*36
        # ------------------------------------------------ loop over SID uncertainty
        SID_devname=["0.9","1.0","1.1","const"]
        
        for SID_dev_index in range(0,3):
        # for SID_dev_index in range(1,2):
        # for SID_dev_index in range(3,4):
            # ------------------------------------------------ loop over volume treatments
            volume_name=['unscaled','scaled']
            for volume_index in range(0,1):
            # for volume_index in range(1,2):
            
                # ------------------------------------------------ loop over RCMs
                RCM=['MAR','RACMO']
                for mm in range(0,2):
                # for mm in range(1,2):
                # for mm in range(1,2):
                    
                # ------------------------------------------------ loop over albedo uncertainty
                    devname=["lo","mid","hi"]
                    for alb_dev_index in range(0,3):
                    # for dev_index in range(1,2):
                        fn='/Users/jason/Dropbox/ELA/stats/imbalance/SLR_committed_'\
                            +type_choice_name[type_choice_index]+'_'+SMB_or_TMB+'_ALB'+devname[alb_dev_index]+'_'\
                                +RCM[mm]+'_'+volume_name[volume_index]+\
                                    '_SID'+SID_devname[SID_dev_index]+\
                                        '_v'+versionx+'.csv'
                        member = pd.read_csv(fn, delimiter=",")
                        # print(member.columns)
                        print(cc,fn)
                        # os.system('ls -lF '+fn)
                        fns[cc]=fn
                        cc+=1
    
        # print(cc)
        
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
    
    
        # ----------------------------------------- start graphic
        slc=np.zeros((20,18))
    
        slc[:,0]=df1.iloc[7,18:].values/-362.
        slc[:,1]=df2.iloc[7,18:].values/-362.
        slc[:,2]=df3.iloc[7,18:].values/-362.
        slc[:,3]=df4.iloc[7,18:].values/-362.
        slc[:,4]=df5.iloc[7,18:].values/-362.
        slc[:,5]=df6.iloc[7,18:].values/-362.
        slc[:,6]=df7.iloc[7,18:].values/-362.
        slc[:,7]=df8.iloc[7,18:].values/-362.
        slc[:,8]=df9.iloc[7,18:].values/-362.
        slc[:,9]=df10.iloc[7,18:].values/-362.
        slc[:,10]=df11.iloc[7,18:].values/-362.
        slc[:,11]=df12.iloc[7,18:].values/-362.
        slc[:,12]=df13.iloc[7,18:].values/-362.
        slc[:,13]=df14.iloc[7,18:].values/-362.
        slc[:,14]=df15.iloc[7,18:].values/-362.
        slc[:,15]=df16.iloc[7,18:].values/-362.
        slc[:,16]=df17.iloc[7,18:].values/-362.
        slc[:,17]=df18.iloc[7,18:].values/-362.
    
        # print(tots)
        
        fn='/Users/jason/Dropbox/ERA5/stats/ERA5_regional_Arctic_t2m_warm_season.csv'
        fn='/Users/jason/Dropbox/ERA5/stats/ERA5_regional_Arctic_t2m_JJA.csv'
        era=pd.read_csv(fn, delimiter=",")
        # print(era.columns)
        # print(era.year[21:])
        x=era.Greenland[21:].values
        
        fig = plt.gcf()
        ax = fig.add_subplot(111)
        plt.close()
    
        cmap = plt.cm.jet
        norm = matplotlib.colors.Normalize(vmin=0, vmax=17)
        
        for i in range(0,18):
            y=slc[:,i]
            plt.scatter(x,y,s=100,color=cmap(norm(i)),label=type_choice_name[type_choice_index])
            b, m = polyfit(x, y, 1)
            xx=np.linspace(np.min(x), np.max(x),2)
            yx=np.linspace(np.min(y), np.max(y),2)
    
            plt.plot(xx, yx, '--',color='grey',linewidth=th*2)
            coefs=stats.pearsonr(x,y)
            # print(type_choice_name[type_choice_index],i,coefs[0])
            if i==11:
            # if i!=101:
                # for yy in range(17,18):
                for yy in range(0,20):
                    # print(yy,x[yy],y[yy],'corr:',coefs[0])
                    plt.text(x[yy],y[yy], str(f"{yy:02d}"),horizontalalignment='center',verticalalignment='center',color='k',fontsize=fs*2)
    
        plt.xlabel('ERA5 Greenland NSAT JJAS, deg. C')
        plt.ylabel('eustatic sea level commitment, mm')
        # plt.legend()
        
        cc=0    ;   xx0=0.75    ;   yy0=0.07    ;   dy=0.06
        props = dict(boxstyle='round', facecolor='w',edgecolor='grey',alpha=1)
    
        plt.text(xx0, yy0+cc*dy,'2 digit year',color='r',
            transform=ax.transAxes,#, fontsize=9
            verticalalignment='top', bbox=props)   
        
        # ----------------------------------------- end graphic
        
        df_concat = pd.concat((df1,df2,df3,df4,df5,df6,\
                               df7,df8,df9,df10,df11,df12,\
                                df13,df14,df15,df16,df17,df18,\
                                # df19,df20,df21,df22,df23,df24,\
                                # df25,df26,df27,df28,df29,df30,\
                                # df31,df32,df33,df34,df35,df36,\
                                   ))
        by_row_index = df_concat.groupby(df_concat.index)
        df_ensemble_count = by_row_index.count()
        df_ensemble_count.to_csv('/Users/jason/Dropbox/ELA/stats/imbalance/_ensemble_count'+type_choice_name[type_choice_index]+'.csv', sep=',')
        
        df_ensemble_min = by_row_index.min()
        df_ensemble_min.to_csv('/Users/jason/Dropbox/ELA/stats/imbalance/_ensemble_min'+type_choice_name[type_choice_index]+'.csv', sep=',')
        df_ensemble_max = by_row_index.max()
        df_ensemble_max.to_csv('/Users/jason/Dropbox/ELA/stats/imbalance/_ensemble_max.csv'+type_choice_name[type_choice_index]+'.csv', sep=',')
        df_ensemble_std = by_row_index.std()
        df_ensemble_std.to_csv('/Users/jason/Dropbox/ELA/stats/imbalance/_ensemble_std.csv'+type_choice_name[type_choice_index]+'.csv', sep=',')
        df_ensemble_mean = by_row_index.mean()
        df_ensemble_mean.to_csv('/Users/jason/Dropbox/ELA/stats/imbalance/_ensemble_mean.csv'+type_choice_name[type_choice_index]+'.csv', sep=',')
        
        
        out_fn='/Users/jason/Dropbox/ELA/stats/imbalance/_ensemble_SLR_committed_'+type_choice_name2[type_choice_index]+'.csv'
        out_concept=open(out_fn,'w')
        cc+=1
        out_concept.write(type_choice_name[type_choice_index]+'\n')
    
        cols='region,n catchments,area sq km,area fraction,volume cubic km,volume fraction,disiquilibrium perpetual 2000-2019 mm SLE,disiquilibrium perpetual 2012 mm SLE,disiquilibrium perpetual 2018 mm SLE,disiquilibrium perpetual 2019 mm SLE,specific disequilibrium 2000-2019,specific disequilibrium 2012,specific disequilibrium 2018,specific disequilibrium 2019,Gt 2000-2019,Gt 2012,Gt 2018,Gt 2019\n'
        out_concept.write(cols)
        
        regions=['SW','CW','NW','NO','NE','CE','SE','All'] ; n_regions=len(regions)
        # print(df_ensemble_mean.columns)
    
        for k in range(0,8):
            out_concept.write(regions[k]+\
                            ','+str("%6.0f"%df_ensemble_mean.iloc[k,0]).lstrip()+\
                            ','+str("%6.0f"%df_ensemble_mean.iloc[k,1]).lstrip()+\
                            ','+str("%6.2f"%df_ensemble_mean.iloc[k,2]).lstrip()+\
                            ','+str("%6.0f"%df_ensemble_mean.iloc[k,3]).lstrip()+\
                            ','+str("%6.2f"%df_ensemble_mean.iloc[k,4]).lstrip()+\
                            ','+str("%8.0f"%df_ensemble_mean.iloc[k,5]).lstrip()+\
                            ','+str("%8.0f"%df_ensemble_mean.iloc[k,6]).lstrip()+\
                            ','+str("%8.0f"%df_ensemble_mean.iloc[k,7]).lstrip()+\
                            ','+str("%8.0f"%df_ensemble_mean.iloc[k,8]).lstrip()+\
                            ','+str("%8.0f"%df_ensemble_mean.iloc[k,9]).lstrip()+\
                            ','+str("%8.0f"%df_ensemble_mean.iloc[k,10]).lstrip()+\
                            ','+str("%8.0f"%df_ensemble_mean.iloc[k,11]).lstrip()+\
                            ','+str("%8.0f"%df_ensemble_mean.iloc[k,12]).lstrip()+\
                            ','+str("%8.0f"%df_ensemble_mean.iloc[k,13]).lstrip()+\
                            ','+str("%8.0f"%df_ensemble_mean.iloc[k,14]).lstrip()+\
                            ','+str("%8.0f"%df_ensemble_mean.iloc[k,15]).lstrip()+\
                            ','+str("%8.0f"%df_ensemble_mean.iloc[k,16]).lstrip()+\
                            ' \n')
        out_concept.write(' '+'\n')
        out_concept.write(' '+'\n')
        out_concept.write(' '+'\n')
        out_concept.write(' '+'\n')
        out_concept.write(' '+'\n')
        out_concept.write(' '+'\n')
        out_concept.write(' '+'\n')
        out_concept.write(' '+'\n')
        out_concept.write(' '+'\n')
    
        out_concept.close()
        # os.system('cat '+out_fn)
        
        out_fn='/Users/jason/Dropbox/ELA/stats/imbalance/_ensemble_SLR_committed_w_std'+type_choice_name2[type_choice_index]+'.csv'
        out_concept=open(out_fn,'w')
        out_concept.write(type_choice_name[type_choice_index]+'\n')
        out_concept.write(cols)
    
        # ,Gt 2000-2019,Gt 2012
        regions=['SW','CW','NW','NO','NE','CE','SE','All'] ; n_regions=len(regions)
        for k in range(0,8):
            # print(df_ensemble_mean.iloc[k,2])
            out_concept.write(regions[k]+\
                            ','+str("%6.0f"%df_ensemble_mean.iloc[k,0]).lstrip()+\
                                # '±'+str("%6.0f"%df_ensemble_std.iloc[k,0]).lstrip()+\
                            ','+str("%6.0f"%df_ensemble_mean.iloc[k,1]).lstrip()+\
                                # '±'+str("%6.0f"%df_ensemble_std.iloc[k,1]).lstrip()+\
                            ','+str("%6.2f"%df_ensemble_mean.iloc[k,2]).lstrip()+\
                                # '±'+str("%6.1f"%df_ensemble_std.iloc[k,2]).lstrip()+\
                            ','+str("%6.0f"%df_ensemble_mean.iloc[k,3]).lstrip()+\
                                # '±'+str("%6.0f"%df_ensemble_std.iloc[k,3]).lstrip()+\
                            ','+str("%6.2f"%df_ensemble_mean.iloc[k,4]).lstrip()+\
                                # '±'+str("%6.1f"%df_ensemble_std.iloc[k,4]).lstrip()+\
                            ','+str("%8.0f"%df_ensemble_mean.iloc[k,5]).lstrip()+\
                                '±'+str("%8.0f"%df_ensemble_std.iloc[k,5]).lstrip()+\
                            ','+str("%8.0f"%df_ensemble_mean.iloc[k,6]).lstrip()+\
                                '±'+str("%8.0f"%df_ensemble_std.iloc[k,6]).lstrip()+\
                            ','+str("%8.0f"%df_ensemble_mean.iloc[k,7]).lstrip()+\
                                '±'+str("%8.0f"%df_ensemble_std.iloc[k,7]).lstrip()+\
                            ','+str("%8.0f"%df_ensemble_mean.iloc[k,8]).lstrip()+\
                                '±'+str("%8.0f"%df_ensemble_std.iloc[k,8]).lstrip()+\
                            ','+str("%8.0f"%df_ensemble_mean.iloc[k,9]).lstrip()+\
                                '±'+str("%8.0f"%df_ensemble_std.iloc[k,9]).lstrip()+\
                            ','+str("%8.0f"%df_ensemble_mean.iloc[k,10]).lstrip()+\
                                '±'+str("%8.0f"%df_ensemble_std.iloc[k,10]).lstrip()+\
                            ','+str("%8.0f"%df_ensemble_mean.iloc[k,11]).lstrip()+\
                                '±'+str("%8.0f"%df_ensemble_std.iloc[k,11]).lstrip()+\
                            ','+str("%8.0f"%df_ensemble_mean.iloc[k,12]).lstrip()+\
                                '±'+str("%8.0f"%df_ensemble_std.iloc[k,12]).lstrip()+\
                            ','+str("%8.0f"%df_ensemble_mean.iloc[k,13]).lstrip()+\
                                '±'+str("%8.0f"%df_ensemble_std.iloc[k,13]).lstrip()+\
                            ','+str("%8.0f"%df_ensemble_mean.iloc[k,14]).lstrip()+\
                                '±'+str("%8.0f"%df_ensemble_std.iloc[k,14]).lstrip()+\
                            ','+str("%8.0f"%df_ensemble_mean.iloc[k,15]).lstrip()+\
                                '±'+str("%8.0f"%df_ensemble_std.iloc[k,15]).lstrip()+\
                            ','+str("%8.0f"%df_ensemble_mean.iloc[k,16]).lstrip()+\
                                '±'+str("%8.0f"%df_ensemble_std.iloc[k,16]).lstrip()+\
                            ' \n')
        out_concept.close()
    os.system('/bin/rm /Users/jason/Dropbox/ELA/stats/imbalance/_ensemble_SLR_committed_all.csv')
    # os.system('cat /Users/jason/Dropbox/ELA/stats/imbalance/_ensemble_SLR_committed_*.csv > /Users/jason/Dropbox/ELA/stats/imbalance/_ensemble_SLR_committed_all.csv')