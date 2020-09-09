#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun '+RCM[mm]+' 22 02:11:24 2020

@author: jeb
"""
import os
import numpy as np
import pandas as pd
import calendar
import matplotlib.pyplot as plt
import time

wo=1
do_plt=0

RCM=['MAR','RACMO']

n_sectors=473
# n_sectors=419
versionx='20200103'
versionx='20200320'

for mm in range(0,2):
    devname=['lo','mid','hi']
    
    fn='/Users/jason/Dropbox/1km_grid2/sector_info_v3.csv'
    df = pd.read_csv(fn, delimiter=",")
        
    cc=0

    smb_annual=np.zeros((n_sectors,7670))
    # days=np.zeros(7670)
    # fn='/Users/jason/Dropbox/'+RCM[mm]+'/output/csv/all.txt'
    # smb_annual=np.loadtxt(fn, delimiter=',')

    for yy in range(1999,2020):
        # print(yy)
        n_days=365
        if calendar.isleap(yy):
            n_days=366
            # print(yy,'hi')
        cc+=n_days
        fn='/Users/jason/Dropbox/'+RCM[mm]+'/output/csv/'+str(yy)+'.csv'
        # os.system('ls -lF '+fn)
        x = np.loadtxt(fn, delimiter=',')
        # print(yy,cc-n_days,cc)
        # print(x[0:2,0:1])
        smb_annual[:,cc-n_days:cc]=x[0:n_sectors,0:n_days]
        # print(smb_annual[0,0:2])
        # time.sleep(5)
    
    # msg='/bin/cat /Users/jason/Dropbox/'+RCM[mm]+'/output/csv/*.csv > /Users/jason/Dropbox/'+RCM[mm]+'/output/csv/all.txt'
    # os.system(msg)
    # fn='/Users/jason/Dropbox/'+RCM[mm]+'/output/csv/all.txt'
    # os.system('head '+fnz)
    # smb_annual=np.loadtxt(fn, delimiter=',')
        
    # # print('n_days in all years',cc)
    
    ts=pd.Timestamp(1999,1,1)
    jd00=int(ts.to_julian_date()-0.5)
    print(jd00)
    
    # os.system('wc -l /tmp/all.csv')
    
    # smb_annual = pd.read_csv('/tmp/all.csv', delimiter=",")
    # print(smb_annual.iloc[:,0])
    
    # for dev_index in range(1,2):
    for dev_index in range(0,3):
    # for dev_index in range(2,3):
        # for k in range(0,n_sectors):
        for k in range(0,n_sectors):
        # for k in range(0,80):
        # for k in range(0,1):
            if df.name[k]!='x':
            # if df.name[k]=='NORDENSKIOLD_GLESCHER_NW':
                print(RCM[mm],k,devname[dev_index],df.name[k])
                ofile='/Users/jason/Dropbox/RCM/stats/'+df.name[k]+'_v'+versionx+'_'+devname[dev_index]+'_'+RCM[mm]+'_SMB.csv'
                if wo:
                    out=open(ofile,'w+')
                    out.write('year,smb,hydro_season_length\n')
            	
                fn='/Users/jason/Dropbox/ELA/stats/TSL/'+df.name[k]+'_ELA_v'+versionx+'_'+devname[dev_index]+'.csv'
                # os.system('cat '+fn)
                df_ELA = pd.read_csv(fn, delimiter=",")
                mean_doy=int(round(np.nanmean(df_ELA.ELA_doy)))
                
                # cum=np.zeros(7670)
                # temp=0. ; cc=0
                for yy in range(1999,2019):
                # for yy in range(2009,2013):
        
                    year0=df_ELA.year[yy-1999]-1
                    year1=df_ELA.year[yy-1999]
                    doy=df_ELA.ELA_doy[yy-1999]
                    
                    ts=pd.Timestamp(year0,1,1)
                    jd0=int(ts.to_julian_date()-0.5)
                    
                    ts=pd.Timestamp(year1,1,1)
                    jd1=int(ts.to_julian_date()-0.5)
                    
                    # -------------------- precise hydro year
                    if yy==1999:
                        x0=jd0+mean_doy-1-jd00
                        doy_choice=mean_doy
                    else:
                        x0=jd0+df_ELA.ELA_doy[yy-1999-1]-1-jd00
                        doy_choice=df_ELA.ELA_doy[yy-1999-1]
                    
                    x1=int(jd1+doy-jd00)
                    
                    # # -------------------- alternative simple hydro year    
                    # x0=jd0+mean_doy-1-jd00
                    # doy_choice=mean_doy         
                    # x1=x0+365
    
                    # # -------------------- calendar year    
                    # x0=jd0-jd00
                    # x1=x0+365
                    
                    h_season=x1-x0
                    if x1 >= 7670:x1=7669
                    smb_basin=np.sum(smb_annual[k,x0:x1])/1e6
                    # temp+=smb_basin
                    # cum[cc]=temp
                    if do_plt:
                        plt.plot(smb_annual[k,x0:x1]/1e6)
                        plt.title(df.name[k])
                    # print(year0,year1,doy_choice,doy,x0,x1,x1-x0,smb_basin)
                    # cc+=1
                    if wo:
                        out.write(str(yy+1)+\
                                  ', '+str("%12.4f"%smb_basin).lstrip()+\
                                  ', '+str("%8.0f"%h_season).lstrip()+\
                                  ' \n')
        
                if wo:out.close()
                # os.system('cat '+ofile)
                # os.system('cat '+ofile)