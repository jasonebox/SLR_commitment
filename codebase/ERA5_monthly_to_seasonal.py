#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 15 05:59:26 2020

@author: Jason Box, GEUS, jeb@geus.dk

Compute seasonal averages for regional polygons

"""
import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

varnam_index=2
varname=['mtpr','msr','t2m']

wo=1

regions=['Greenland','Alaska','Canada','Scandinavia','Svalbard','Iceland','Russian Arctic','Arctic Land','North America','Eurasia','Northern Hemisphere','Arctic Ocean','Arctic','Finland','Global']


fn='/Users/jason/Dropbox/ERA5/stats/ERA5_'+varname[varnam_index]+'_monthly.csv'
os.system('ls -lF '+fn)
df=pd.read_csv(fn, delimiter=",")
print(df.columns)

iyear=1979 ; fyear=2019
# iyear=1996 ; fyear=1997
n_years=fyear-iyear+1


season_name=['annual','cold_season','warm_season','JJA','MJJAS','July','JA']
imonth=[1,10,6,6,5,7,7]
fmonth=[12,5,9,8,9,7,8]

for j,season_nam in enumerate(season_name):

    ofile='/Users/jason/Dropbox/ERA5/stats/ERA5_regional_Arctic_'+varname[varnam_index]+'_'+season_name[j]+'.csv'
    out_concept=open(ofile,'w+')
    header='year,Greenland,Alaska,Canada,Scandinavia,Svalbard,Iceland,Russian Arctic,Arctic Land,North America,Eurasia,Northern Hemisphere,Arctic Ocean,Arctic,Finland,Global\n'
    out_concept.write(header)
    
    for yy in range(0,n_years):
        
        results=np.zeros(len(regions))
        
        if season_name[j]=='cold_season':
            v=np.where((df.year==yy+iyear-1)&(df.month>=imonth[j])&(df.month<=12))
            v2=np.where((df.year==yy+iyear)&(df.month>=1)&(df.month<=fmonth[j]))
            v=np.concatenate([v[0],v2[0]])
            # print(v)
        if season_name[j]!='cold_season':
            v=np.where((df.year==yy+iyear)&(df.month>=imonth[j])&(df.month<=fmonth[j]))
            v=v[0]
        # print(season_nam,yy+1979,v)
        for i,region in enumerate(regions):
            # if season_name[j]!='cold_season':
            # if varnam_index==0:results[i]=np.nansum(df.iloc[v,i+2])
            if varnam_index==2:
                results[i]=np.nanmean(df.iloc[v,i+2])
            if varnam_index!=2:
                results[i]=np.nansum(df.iloc[v,i+2])
            # if season_name[j]=='cold_season':results[i]=np.nanmean(df.iloc[v[0]:v2[0],i+2])
        # if region=='Greenland':print(region,yy+iyear,results[i])
    
        if ((season_name[j]=='cold_season') and (yy==0)):results[:]=np.nan
        print(season_nam,yy,results)
        out_concept.write(\
              str(yy+1979)+\
              ','+str("%8.2f"%(results[0])).lstrip()+\
              ','+str("%8.2f"%(results[1])).lstrip()+\
              ','+str("%8.2f"%(results[2])).lstrip()+\
              ','+str("%8.2f"%(results[3])).lstrip()+\
              ','+str("%8.2f"%(results[4])).lstrip()+\
              ','+str("%8.2f"%(results[5])).lstrip()+\
              ','+str("%8.2f"%(results[6])).lstrip()+\
              ','+str("%8.2f"%(results[7])).lstrip()+\
              ','+str("%8.2f"%(results[8])).lstrip()+\
               ','+str("%8.2f"%(results[9])).lstrip()+\
               ','+str("%8.2f"%(results[10])).lstrip()+\
               ','+str("%8.2f"%(results[11])).lstrip()+\
               ','+str("%8.2f"%(results[12])).lstrip()+\
               ','+str("%8.2f"%(results[13])).lstrip()+\
                ','+str("%.3f"%(results[14]))+\
                    '\n')
    
    if wo:out_concept.close()
