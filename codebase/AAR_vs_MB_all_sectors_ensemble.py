#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 14:10:13 2020

@author: jeb
"""

import matplotlib.pyplot as plt
# import numpy as np
import os
import pandas as pd
import locale
locale.setlocale(locale.LC_ALL, '')  # Use '' for auto, or force e.g. to 'en_US.UTF-8'
from matplotlib.ticker import StrMethodFormatter
import numpy as np
from scipy import stats

th=1 ; th=2
formatx='{x:,.3f}'; fs=24 ; fs=32
# plt.rcParams['font.sans-serif'] = ['Georgia']
plt.rcParams["font.size"] = fs
plt.rcParams['axes.facecolor'] = 'w'
plt.rcParams['axes.edgecolor'] = 'k'
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 1
plt.rcParams['grid.color'] = "#cccccc"
plt.rcParams["legend.facecolor"] ='w'
plt.rcParams["mathtext.default"]='regular'
plt.rcParams['grid.linewidth'] = th
plt.rcParams['axes.linewidth'] = th #set the value globally
plt.rcParams['figure.figsize'] = 12, 12.3

fn='/Users/jason/Dropbox/1km_grid2/sector_info_v3.csv'
#count,name,region,type,id,lat,lon,area
#os.system('ls -lF '+fn)
# os.system('head '+fn) 
df = pd.read_csv(fn, delimiter=",")
lat = df["lat"]
lon = df["lon"]
area = df["area"]
volume = df["volume"]
v=np.where(df.sector_type=='LTx')
df.sector_type[v[0]]='LT'

volfrac=np.zeros(4)
volfrac[0]=100.
v=np.where(df["sector_type"]=='TW')
volfrac[1]=sum(volume[v[0]])/sum(volume)*100
v=np.where(df["sector_type"]=='LT')
volfrac[2]=sum(volume[v[0]])/sum(volume)*100
volfrac[3]=volfrac[1]

sector_scenarios=['all_TMB','TW_TMB','LT_SMB','TW_SMB']
sector_scenario_names=['TMB, all sectors','TMB, tidewater sectors','SMB, land terminating sectors','SMB, tidewater sectors']
xtitle_names=['Total Mass Balance, all sectors','Surface Mass Balance, tidewater sectors','Total Mass Balance, land terminating sectors','Surface Mass Balance, tidewater sectors']
abcd=['a.) TMB vs AAR, all sectors','b.) TMB vs AAR, tidewater sectors','c.) TMB vs AAR, land terminating sectors','d.)  SMB vs AAR, tideawater sectors']
versionx='20200320'

fn='/Users/jason/Dropbox/1km_grid2/sector_info_v3.csv'
df = pd.read_csv(fn, delimiter=",")
tot_vol=sum(df.volume)

devname=["lo","mid","hi"]

for j,sector_scenario in enumerate(sector_scenarios[0:1]):
# for j,sector_scenario in enumerate(sector_scenarios):
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
                    for ALB_dev_index in range(0,3):
                    # for ALB_dev_index in range(1,2):
                        fn='/Users/jason/Dropbox/ELA/stats/AAR_vs_MB_all_sectors_together/'+\
                            sector_scenario+'_ALB'+devname[ALB_dev_index]+'_'+RCM[mm]+'_'+\
                                volume_name[volume_index]+'_SID'+SID_devname[SID_dev_index]+\
                                    '_v'+versionx+'.csv'
                        # os.system('ls -lF '+fn)
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
           
        df_concat = pd.concat((df1,df2,
                               df3,df4,df5,df6,\
                                df7,df8,df9,df10,df11,df12,\
                                 df13,df14,df15,df16,df17,df18,\
                                   ))
        
        by_row_index = df_concat.groupby(df_concat.index)
        
        df_ensemble_std = by_row_index.std()
        
        df_ensemble_mean = by_row_index.mean()
        
        
        x=df_ensemble_mean.mb
        xerr=df_ensemble_std.mb
    
        y=df_ensemble_mean.aar
        yerr=df_ensemble_std.aar
        
        year=df1.year
        
        plt.close()

        fancy=1
        
        if fancy:
            plt.errorbar(x, y, yerr=[yerr, 2*yerr], xerr=xerr,fmt='.',c='w', ecolor='purple', capthick=20,capsize=5, 
            elinewidth=th,
            markeredgewidth=th)

        # plt.scatter(x, y, s=650, facecolors='w', edgecolors='w',linewidth=th,zorder=9)
        plt.scatter(x, y, s=300, facecolors='k', edgecolors='k',linewidth=th,zorder=9)
        statsx=stats.pearsonr(x, y)
        R=statsx[0]
        oneminusp=1-statsx[1]
        oneminusp_string=' = '+str("%8.3f"%oneminusp).lstrip()
        if round(oneminusp, 3)==1.0:
            oneminusp_string='>0.999'
        print(round(oneminusp, 3))
        coef = np.polyfit(x,y,1)
        m,AAR0 = np.polyfit(x, y, 1)
        poly1d_fn = np.poly1d(coef) 
        
        xx = np.linspace(np.min(x), np.max(x),2)
        yx = m*xx+AAR0
        
        plt.plot(xx, yx, '--',color='grey',linewidth=th*2)
        
        AAR_mean=np.mean(y)
        alpha_mean=AAR0/AAR_mean
        
        imbalance_mean=(1-alpha_mean)*tot_vol
        mm_SLE_mean=-imbalance_mean/362.
        print('mean',mm_SLE_mean)

        for i in range(0,20):
            alpha_x=AAR0/y[i]
            imbalance_x=(1-alpha_x)*tot_vol
            mm_SLE_x=-imbalance_x/362.
            print("alpha_x",i+2000,y[i],"mm_SLE",mm_SLE_x)

        mean_y_err=np.mean(yerr)
        imbalance_mean0=(1-(alpha_mean-mean_y_err/2))*tot_vol
        mm_SLE_mean0=-imbalance_mean0/362.
        print(mm_SLE_mean0)

        imbalance_mean1=(1-(alpha_mean+mean_y_err/2))*tot_vol
        mm_SLE_mean1=-imbalance_mean1/362.
        
        print(mm_SLE_mean1)
        
        mm_err=mm_SLE_mean1-mm_SLE_mean0
        
        yos_text=0.004
        for i in range(0,20):
          plt.text(x[i], y[i]-yos_text/10, str(year[i])[2:4], \
              horizontalalignment='center',verticalalignment='center', \
              color='w',zorder=10,fontsize=14)
         
        plt.gca().yaxis.set_major_formatter(StrMethodFormatter(formatx))
        plt.xlabel(xtitle_names[j]+', Gt y$^{-1}$')
        # plt.title(sector_scenario_names[j])
        plt.ylabel('Accumulation Area Ratio (AAR)')
        plt.gca().spines['right'].set_color('none')
        plt.gca().spines['top'].set_color('none')
        xos=40
        if sector_scenario=='TW_SMB':xos=20
        if sector_scenario=='LT_SMB':xos=10
        plt.xlim(np.min(x)-xos*2,np.max(x)+xos*3)
        yos=0.02
        if sector_scenario=='LT_SMB':
            yos=0.03
        plt.ylim(np.min(y)-yos,np.max(y)+yos)
        osxx=0.002
        xos_text=4
        xx=np.linspace(np.min(x)-xos*2, 0+xos/2,2)
        xx=np.linspace(-10, 0+xos/2,2)
        if sector_scenario=='TW_SMB':
            xx = np.linspace(np.min(x)-xos, np.max(x)+xos/2,2)
        yx = [AAR0,AAR0]
        plt.plot(xx, yx, color='b',linewidth=th*2)
        plt.text(xx[1]+xos_text,AAR0-yos_text,'AAR$_0$\n'+str("%8.3f"%AAR0).lstrip(),color='b',zorder=12)
        
        yx = [AAR_mean,AAR_mean]
        plt.plot(xx, yx, color='r',linewidth=th*2)
        #                    plt.text(np.min(x)+xos,yx[0]+yx[0]*0.005,'AAR$_0$ = '+str("%8.3f"%AAR0).lstrip(),color='b')
        plt.text(xx[1]+xos_text,AAR_mean-yos_text,'AAR$_{2000-2019}$\n'+str("%8.3f"%AAR_mean).lstrip(),color='r')
        
        props = dict(boxstyle='round', facecolor='w',edgecolor='grey',alpha=1)
    
        fig = plt.gcf()
        ax = fig.add_subplot(111)
        cc=1    ;   xx0=0.4    ;   yy0=0.18    ;   dy=0.06
        # txt='ice volume = '+str("%8.1f"%volfrac[j]).lstrip()+'%'+\
        txt='alpha = '+str("%.3f"%alpha_mean)+'±'+str("%8.3f"%mean_y_err).lstrip()+\
            '\nSLE = '+str("%.0f"%mm_SLE_mean)+'±'+str("%8.0f"%mm_err).lstrip()+' mm'+\
            '\nR = '+str("%.3f"%R)+', 1-p '+oneminusp_string
        plt.text(xx0, yy0+cc*dy,txt,color='k',
            transform=ax.transAxes,#, fontsize=9
            verticalalignment='top', bbox=props)    ;   cc+=1
        ymin=0.5
        yos=0.002
        if np.min(y)-yos < ymin:ymin=0.
        
        xx = [0,0]
        #                yx = [np.min(y),AAR0]
        yx = [ymin,1.]
        plt.plot(xx, yx, '--', color='g',linewidth=th*2)
        
        # plt.show()
        
        fig_path='/Users/jason/Dropbox/ELA/Figs/AAR_vs_MB_all_sectors_together/'
        figname=fig_path+sector_scenario+'.png'
        plt.savefig(figname, bbox_inches='tight', dpi=250)
        # figname=fig_path+sector_scenario+'.eps'
        # plt.savefig(figname)
        
        # for i,regionx in enumerate(regions):
        wo=0
        if wo:
            out_concept.write('All'+\
                          ','+str("%8.2f"%sum_all_sector).lstrip()+\
                          ','+str("%8.2f"%sum_all_area).lstrip()+\
                          ','+str("%8.3f"%frac_area).lstrip()+\
                          ','+str("%8.3f"%sum_all_volume).lstrip()+\
                          ','+str("%8.3f"%frac_vol).lstrip()+\
                          ','+str("%8.5f"%(sum_all_mean/362.)).lstrip()+\
                          ','+str("%8.5f"%(sum_all_2012/362.)).lstrip()+\
                          ','+str("%8.5f"%(sum_all_2018/362.)).lstrip()+\
                          ','+str("%8.5f"%(sum_all_2019/362.)).lstrip()+\
                          ','+str("%8.5f"%spec_disequil_all_mean).lstrip()+\
                          ','+str("%8.5f"%spec_disequil_all_2012).lstrip()+\
                          ','+str("%8.5f"%spec_disequil_all_2018).lstrip()+\
                          ','+str("%8.5f"%spec_disequil_all_2019).lstrip()+\
                          ','+str("%.1f"%(sum_all_mean))+\
                          ','+str("%.1f"%(sum_all_2012))+\
                          ','+str("%.1f"%(sum_all_2018))+\
                          ','+str("%.1f"%(sum_all_2019))+\
                          ','+str("%.1f"%sum_by_year_all[0])+\
                          ','+str("%.1f"%sum_by_year_all[1])+\
                          ','+str("%.1f"%sum_by_year_all[2])+\
                          ','+str("%.1f"%sum_by_year_all[3])+\
                          ','+str("%.1f"%sum_by_year_all[4])+\
                          ','+str("%.1f"%sum_by_year_all[5])+\
                          ','+str("%.1f"%sum_by_year_all[6])+\
                          ','+str("%.1f"%sum_by_year_all[7])+\
                          ','+str("%.1f"%sum_by_year_all[8])+\
                          ','+str("%.1f"%sum_by_year_all[9])+\
                          ','+str("%.1f"%sum_by_year_all[10])+\
                          ','+str("%.1f"%sum_by_year_all[11])+\
                          ','+str("%.1f"%sum_by_year_all[12])+\
                          ','+str("%.1f"%sum_by_year_all[13])+\
                          ','+str("%.1f"%sum_by_year_all[14])+\
                          ','+str("%.1f"%sum_by_year_all[15])+\
                          ','+str("%.1f"%sum_by_year_all[16])+\
                          ','+str("%.1f"%sum_by_year_all[17])+\
                          ','+str("%.1f"%sum_by_year_all[18])+\
                          ','+str("%.1f"%sum_by_year_all[19])+\
                          ' \n')
            out_concept.close()