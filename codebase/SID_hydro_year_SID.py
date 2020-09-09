#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 22 10:29:25 2019

@author: Jason Box, GEUS, jeb@geus.dk

Obtain annual min AAR (max ELA) hydrological year average solid ice discharge.

"""
import os
import numpy as np
# import matplotlib.pyplot as plt
import pandas as pd

ly='x'

fn='/Users/jason/Dropbox/1km_grid2/sector_info_v3.csv'
#count,name,region,type,id,lat,lon,area
os.system('ls -lF '+fn)
os.system('head '+fn) 
df = pd.read_csv(fn, delimiter=",")
sector = df["id"]
latmean = df["lat"]
lonmean = df["lon"]
area = df["area"]
g_type = df["sector_type"]
region = df["region"]
name = df["name"]
name2 = df["name"]

n=len(name)

fn='/Users/jason/Dropbox/SID/Mankoff_2019/sector_D.csv'
os.system('head -n10 '+fn) 
df_SID = pd.read_csv(fn, delimiter=",")
date=pd.to_datetime(df_SID["Date"],format='%Y-%m-%d')# %H:%M:%S')

n_SID=len(df_SID)
year=[None]*n_SID
month=[None]*n_SID
day=[None]*n_SID
doy=day
jt_SID=[0.]*n_SID

# ----------------------------------------- compute julian decimal year for SID
for k in range(0,n_SID-1):
#    print(j)
    date_string=(str(date[k]))
    year[k]=int(date_string[0:4])
    month[k]=int(date_string[5:7])
    day[k]=int(date_string[8:10])

    # julian date
    ts=pd.Timestamp(year[k], month[k], day[k])
    doy[k]=ts.dayofyear
    jt_SID[k]=year[k]+doy[k]/366.

versionx='20191127'
versionx='20200103'
versionx='20200320'

devname=["lo","mid","hi","const"]
devname2=["0.9","1.0","1.1","const"]
SID_dev=[0.9,1.0,1.1,1.0]

# for SID_dev_index in range(0,3):
for SID_dev_index in range(0,4):
# for SID_dev_index in range(1,2):
    for ALB_dev_index in range(0,3):
    # for ALB_dev_index in range(1,2):
        # ----------------------------------------- loop over sectors
        for k in range(0,n):
        # for k in range(0,1):
        
            # if name[k][0:3] == 'IKE':
            if g_type[k] == 'TW':
                print(k,devname[ALB_dev_index],g_type[k],name2[k],sector[k])
                nams=(name[k])
            #    type(name[k])
                mult=1.
                if name[k]=='IKERTIVAQ_M':mult=0.5# manual merging of problematic sector
                if name[k]=='IKERTIVAQ_S':
                    nams='IKERTIVAQ_M'
                    mult=0.5
                if name[k]=='IKERTIVAQ_NN':mult=0.5# manual merging of problematic sector
                if name[k]=='IKERTIVAQ_N':
                    nams='IKERTIVAQ_NN'
                    mult=0.5
                if name[k]=='NANSEN_GLETSCHER':mult=9# manual merging of problematic sector
                if name[k]=='NORDENSKIOLD_GLESCHER_NW':mult=0.5# manual merging of problematic sector
                if name[k]=='UKAASORSUAQ':mult=3# manual merging of problematic sector

                # nams="IKERTIVAQ_S"
                SID = df_SID[nams]*mult
                # print(name[k],"------------------------- before",SID[0])
                # if nams=='IKERTIVAQ_M':SID/=2.
                # if name[k]=='IKERTIVAQ_S':SID/=2.
                # if nams=='IKERTIVAQ_NN':SID/=2.        
                # print(name[k],"after",SID[0])
                # if name[k]=='IKERTIVAQ_N':SID/=2.
            #    SID=0.
                
        #        fn='/Users/jason/Dropbox/ELA/stats/ELA/regional/polygons/'+str('%03d'%sector[k])+'_ELA_stats_mean.csv'
        #    #    year,day of max snowline,max snowline,min AAR,mean albedo ablation area,mean albedo accumulation area,mean albedo all catchment,min albedo ablation area,min albedo all area,lat of snowline,lon of snowline
        #        os.system('ls -lF '+fn) 
        ##        os.system('wc -l '+fn)
        #        print(fn)
        #    #    os.system('head '+fn) 
        #        df_ELA = pd.read_csv(fn, delimiter=",")
        #        yearx = df_ELA["year"]
        #        doy1_ELA = df_ELA["day of max snowline"]
        
        #        fn='/Users/jason/Dropbox/ELA/stats/TSL/'+str('%03d'%sector[k])+'_ELA_v20191127.csv'
                
        # time interval defined by ELA data... ELA day of year
                fn='/Users/jason/Dropbox/ELA/stats/TSL/'+name[k]+'_ELA_v'+versionx+'_'+devname[ALB_dev_index]+'.csv'
        #        year,AAR,ELA,ELA_doy
                # os.system('ls -lF '+fn) 
                # os.system('cat '+fn) 
        
                df_ELA = pd.read_csv(fn, delimiter=",")
                yearx = df_ELA["year"]
                ELA = df_ELA["ELA"].values
                doy1_ELA = df_ELA["ELA_doy"].values#.tolist()
                doy1_ELA[doy1_ELA<0.1]=200
                # doy1_ELA = np.where(doy1_ELA < 0.1, np.nan, doy1_ELA)  # Set all data larger than 0.8 to NaN
        #        doy1_ELA = np.ma.array(doy1_ELA, mask=np.isnan(doy1_ELA)) # Use a mask to mark the NaNs
                
                # doy1_ELA = np.ma.array(doy1_ELA, mask=np.isnan(doy1_ELA)) # Use a mask to mark the NaNs
                # print('doy1_ELA',doy1_ELA,np.nanmean(doy1_ELA))
                
                jt0_ELA=1999+np.nanmean(doy1_ELA)/365.
                
                print('jt0_ELA',jt0_ELA)
                # out_fn2='/Users/jason/Dropbox/SID/Mankoff_2019/polygons/'+str('%03d'%sector[k])+'_SID_v'+versionx+'_'+devname[ALB_dev_index]+'.csv'
                out_fn='/Users/jason/Dropbox/SID/Mankoff_2019/polygons/'+\
                    name[k]+'_SID_ALB'+devname[ALB_dev_index]+'_SID'+devname2[SID_dev_index]+\
                        '_v'+versionx+'.csv'
                out_concept=open(out_fn,'w')
                out_concept.write('year,SID\n')
                
                # print('out fn',out_fn)
                # print(name[k])
                
                mean_SID=np.mean(SID) ; temp=mean_SID
                # averaging over 20 MODIS years
                for yy in range(0,20):           
                    if ELA[yy]>0.:
                        sumx=0.
                        countx=0.       
                        if yy>0:jt0_ELA=yearx[yy-1]+doy1_ELA[yy-1]/365.        
                        jt1_ELA=yearx[yy]+doy1_ELA[yy]/365.       
                        # if yy>0:print(yy,jt0_ELA,yearx[yy-1],doy1_ELA[yy-1],yearx[yy],doy1_ELA[yy],jt1_ELA)                       
                        for j in range(0,n_SID-1):
                            # print(j,df_SID.Date[j],SID[j])
                            # print(yy,jt_SID[j],jt0_ELA,jt1_ELA)
                            if ((jt_SID[j] >= jt0_ELA) & (jt_SID[j] <= jt1_ELA)):
                                # print(df_SID.Date[j],jt_SID[j],jt0_ELA,jt1_ELA,SID[j])
                                sumx+=SID[j]*SID_dev[SID_dev_index]
                                countx+=1.
                #                print(yy,jt0_ELA,jt_SID[k],jt1_ELA,sumx,countx)
        #                print(yy,sumx,countx,mean_SID)
                
                        if countx>0:mean_SID=sumx/countx
        #                print(yy,sumx,countx,mean_SID)
        
        #            print(yy,ELA[yy],mean_SID)
                    if SID_dev_index==3:mean_SID=temp
                    yx=yy+2000
                    out_concept.write(str('%04d'%yx)+','+str("%7.3f"%mean_SID)+' \n')
        
                # print('done')
                out_concept.close()
        
                print(out_fn)
                # os.system('/bin/rm '+out_fn2)