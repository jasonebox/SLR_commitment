#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 22 10:29:25 2019
@author: Jason Box, GEUS, jeb@geus.dk

compare AAR and MB, determine regional-scale imbalance for gamma = 1 and 1.25

input from: /Users/jason/Dropbox/ELA/prog/AAR_vs_MB_v_all_years_variable_gamma.py

output: ELA/Figs/AAR_vs/ and ELA/stats/

"""
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


ly='x'
batch=1
wo=1

open_plot=0
do_plot=1
plt_map=0
annotate_text=0
plt_title=1
prt=1


SID_index0=1 ; SID_index1=2
# SID_index0=0 ; SID_index1=4
ALB_index0=1 ; ALB_index1=2
volume_index0=0 ; volume_index1=1
RCM_index0=0 ; RCM_index1=1

th=1
# plt.rcParams['font.sans-serif'] = ['Georgia']
fs=24
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

n_sectors=473
# n_sectors=419

versionx='20200103'
versionx='20200320'
 
regions=['SW','CW','NW','NO','NE','CE','SE','all'] ; n_regions=len(regions)

#for if_icecaps in range(1,2):
for if_icecaps in range(0,1):
    if if_icecaps:
        if_icecaps_name='_icecaps_only'
    else:
        if_icecaps_name=''
#    print("if_icecaps_name:",if_icecaps_name)
#    x()
#    for by_area in range(0,1):
    by_area=1
    if by_area:
        by_area_name='_by_area'
    else:
        by_area_name='_by_volume'

    # for regionx in regions[7:8]:
    for regionx in regions[0:1]:
    # for regionx in regions[0:7]:
        fn='/Users/jason/Dropbox/1km_grid2/sector_info_v3.csv'
        #count,name,region,type,id,lat,lon,area
        #os.system('ls -lF '+fn)
        # os.system('head '+fn) 
        df = pd.read_csv(fn, delimiter=",")
        #print(df.columns)
        lat = df["lat"]
        lon = df["lon"]
        area = df["area"]
        volume = df["volume"]
        region = df["region"]
        name = df["name"]
        gl_type = df["gl_type"]
        
        v=region!=regionx
        df["sector_type"][v]='null'
        
        if if_icecaps:
            tot_vol=sum(volume[(region==regionx)&(gl_type==' ice_cap')])
            tot_area=sum(area[(region==regionx)&(gl_type==' ice_cap')])
        else:
            tot_vol=sum(volume[region==regionx])
            tot_area=sum(area[region==regionx])
        if regionx=='all':
            tot_vol=sum(volume)
            tot_area=sum(area)

        if batch:
            SID_index0=0 ; SID_index1=3
            ALB_index0=0 ; ALB_index1=3
            volume_index0=0 ; volume_index1=1
            RCM_index0=0 ; RCM_index1=2
        
        for sector_scenario in range(1,2):
        # for sector_scenario in range(0,4):
        # for sector_scenario in range(0,1):
            
            # ------------------------------------------------ loop over SID uncertainty
            devname=["lo","mid","hi","const"]
            
            SID_devname=["0.9","1.0","1.1","const"]
            
            for SID_dev_index in range(SID_index0,SID_index1):    
                # ------------------------------------------------ loop over volume treatments
                volume_name=['unscaled','scaled']
                for volume_index in range(volume_index0,volume_index1):
                    volume = df["volume"]
                    if volume_index:
                        v=np.where(area<89000)
                        volume[v[0]]=area[v[0]]*1.6233623010
                        
                    namex = df["name"]
                            
                    valid_flag=[0.]*n_sectors
                    # ------------------------------------------------ loop over RCMs
                    RCM=['MAR','RACMO']
                    for mm in range(RCM_index0,RCM_index1):
                    # ------------------------------------------------ loop over albedo uncertainty
                        for ALB_dev_index in range(ALB_index0,ALB_index1):
                            fn='/Users/jason/Dropbox/ELA/stats/TSL/'+\
                                        namex[0]+'_ELA_v'+versionx+'_'+devname[ALB_dev_index]+'.csv'
                            TMB_annual_tot = pd.read_csv(fn, delimiter=",")
            
                            TMB_annual_tot=TMB_annual_tot.drop(columns=TMB_annual_tot.columns[1:])
                            TMB_annual_tot["TMB"]=0.
                                         
                            sum_AAR=np.zeros(20)
                            sum_MB=np.zeros(20)
                            
                            for k in range(0,n_sectors):
                            # for k in range(0,2):
                                # if region[k]==regionx:
                                scenario_name='all_TMB'

#                                    if ((region[k]==regionx)&(gl_type[k]==' ice_cap')):
                                if ((region[k]!='null')):
#                                        print(regionx,gl_type[k],tot_vol)
                                # if gl_type[k]==' ice_sheet':
                                    # =================================== ELA
                                    fn='/Users/jason/Dropbox/ELA/stats/TSL/'+namex[k]+'_ELA_v'+versionx+'_'+devname[ALB_dev_index]+'.csv'
                                    df_ELA = pd.read_csv(fn)
                                    # print(fn)
                                    # x()
                                    # =================================== SMB
                                    fn='/Users/jason/Dropbox/RCM/stats/'+df.name[k]+'_v'+versionx+'_'+devname[ALB_dev_index]+'_'+RCM[mm]+'_SMB.csv'
                                    df_SMB = pd.read_csv(fn, delimiter=",")
                                    if df["sector_type"][k]=='TW':
                                        # =================================== SID
                                        fn='/Users/jason/Dropbox/SID/Mankoff_2019/polygons/'+\
                                        name[k]+'_SID_ALB'+devname[ALB_dev_index]+'_SID'+SID_devname[SID_dev_index]+\
                                            '_v'+versionx+'.csv'
                                        df_SID = pd.read_csv(fn)
                                                                    
                                    if by_area:
                                        integrator=df.area[k]/tot_area
                                        # print(k,by_area_name)
                                    else:
                                        integrator=df.volume[k]/tot_vol
                                    
                                    if sector_scenario==0:
                                        scenario_name='all_TMB'
                                        # if reif (df["sector_type"][k]=='TW')&(region==regionx)):
                                        if df["sector_type"][k]=='TW':
                                            sum_MB+=df_SMB.smb-df_SID.SID
                                            sum_AAR+=df_ELA.AAR*integrator
                                        if df["sector_type"][k]=='LT':
                                            sum_MB+=df_SMB.smb
                                            sum_AAR+=df_ELA.AAR*integrator
                
                                    if sector_scenario==1: #    scenario_name='TW_TMB'
                                        # v=np.where((df["sector_type"]=='TW')&(region==regionx))
                                        v=np.where(df["sector_type"]=='TW')
                                        tot_vol=sum(volume[v[0]])
                                        tot_area=sum(area[v[0]])
                                        integrator=df.area[k]/tot_area
                                        scenario_name='TW_TMB'
                                        if df["sector_type"][k]=='TW':
                                            sum_MB+=df_SMB.smb-df_SID.SID
                                            sum_AAR+=df_ELA.AAR*integrator
                
                                    if sector_scenario==2: #    scenario_name='LT_SMB'
                                        # v=np.where((df["sector_type"]=='LT')&(region==regionx))
                                        v=np.where(df["sector_type"]=='LT')
                                        tot_vol=sum(volume[v[0]])
                                        tot_area=sum(area[v[0]])
                                        integrator=df.area[k]/tot_area
                                        scenario_name='LT_SMB'
                                        if df["sector_type"][k]=='LT':
                                            sum_MB+=df_SMB.smb
                                            sum_AAR+=df_ELA.AAR*integrator
                
                                    if sector_scenario==3: #    scenario_name='TW_SMB'
                                        v=np.where((df["sector_type"]=='TW')&(region==regionx))
                                        # v=np.where(df["sector_type"]=='TW')
                                        tot_vol=sum(volume[v[0]])
                                        tot_area=sum(area[v[0]])
                                        integrator=df.area[k]/tot_area
                                        scenario_name='TW_SMB'
                                        if df["sector_type"][k]=='TW':
                                            sum_MB+=df_SMB.smb
                                            sum_AAR+=df_ELA.AAR*integrator
                                
                            if wo:
                                out_fn='/Users/jason/Dropbox/ELA/stats/AAR_vs_MB_all_sectors_together/'+\
                                    regionx+'_'+scenario_name+'_ALB'+devname[ALB_dev_index]+'_'+RCM[mm]+'_'+\
                                        volume_name[volume_index]+'_SID'+SID_devname[SID_dev_index]+\
                                            by_area_name+\
                                            if_icecaps_name+\
                                            '_v'+versionx+'.csv'

                                out_concept=open(out_fn,'w')
                                out_concept.write('year,mb,aar\n')
                                
                                for i in range(0,20):
                                    out_concept.write(str(i+2000)+','+\
                                    str(sum_MB[i])+','+\
                                    str(sum_AAR[i])+' \n')
            
                                out_concept.close()
                                print(out_fn)
                                # os.system('cat '+out_fn)
