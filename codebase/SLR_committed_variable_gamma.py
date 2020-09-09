#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 18:34:01 2019

@author: Jason Box, GEUS, jeb@geus.dk

Summarise output and for N permutations depending on Error Propagation

before: /Users/jason/Dropbox/ELA/prog/imbalance_old/ensemble_imbalance.py
upstream of that is /Users/jason/Dropbox/ELA/prog/AAR_vs_MB_v_all_years.py
/Users/jason/Dropbox/ELA/prog/imbalance_old/AAR_vs_MB_w_map_v3.py

after: /Users/jason/Dropbox/ELA/prog/imbalance_old/SLR_committed_ensemble.py

"""

ly='x'

import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import locale
locale.setlocale(locale.LC_ALL, '')  # Use '' for auto, or force e.g. to 'en_US.UTF-8'

# plt.rcParams['font.sans-serif'] = ['Georgia']
plt.rcParams['axes.facecolor'] = 'white'
plt.rcParams['axes.edgecolor'] = 'black'
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 1
plt.rcParams['grid.color'] = "grey"
plt.rcParams["font.size"] = 14

plt=0
wo=1

versionx='20200320'
versionx='20200716'

SMB_or_TMB='TMB'
regions=['SW','CW','NW','NO','NE','CE','SE'] ; n_regions=len(regions)


for gamma_index in range(0,2):    
    gamma=1.
    gamma_name='_gamma1.0'
    
    if gamma_index:
        gamma=1.25
        gamma_name='_gamma1.25'
    # ------------------------------------------------ loop over SID uncertainty
    SID_devname=["0.9","1.0","1.1","const"]
    
    for SID_dev_index in range(0,3):
    # for SID_dev_index in range(1,2):
    # for SID_dev_index in range(3,4):
        
        # ------------------------------------------------ loop over volume treatments
        volume_name=['unscaled','scaled']
        for volume_index in range(0,1):
        # for volume_index in range(1,2):
        
            fn='/Users/jason/Dropbox/1km_grid2/sector_info_v3.csv'
            #count,name,region,type,id,lat,lon,area
            #os.system('ls -lF '+fn)
            #os.system('head '+fn) 
            df = pd.read_csv(fn, delimiter=",")
            latmean = df["lat"]
            lonmean = df["lon"]
            area_all = df["area"]
            #gl_type = df["type"]
            #region = df["region"]
            volume_all = df["volume"]
            if volume_index:
                v=np.where(area_all<89000)
                volume_all[v[0]]=area_all[v[0]]*1.6233623010
            name_all = df["name"]
            
            tot_vol_all=sum(volume_all)
            tot_area_all=sum(area_all)
            
            n_sectors_all=len(area_all)
            n_sectors_419=len(area_all)
        
            # ------------------------------------------------ loop over RCMs
            RCM=['MAR','RACMO']
            for mm in range(0,2):
            # for mm in range(1,2):
            # for mm in range(1,2):
                
            # ------------------------------------------------ loop over albedo uncertainty
                devname=["lo","mid","hi"]
                for alb_dev_index in range(0,3):
                # for alb_dev_index in range(1,2):
                    fn='/Users/jason/Dropbox/ELA/stats/imbalance/imbalance_'+\
                            SMB_or_TMB+'_ALB'+devname[alb_dev_index]+'_'+RCM[mm]+'_'+\
                                volume_name[volume_index]+'_SID'+SID_devname[SID_dev_index]+\
                                    gamma_name+\
                                    '_v'+versionx+'.csv'
                    os.system('ls -lF '+fn)
                    # stop
                    # os.system('head '+fn)
                    # os.system('wc -l '+fn)
                    df = pd.read_csv(fn, delimiter=",")
                    # print(df.columns)
                    # x()
                    #'name,region,volume,area,mean mass flux,AAR_mean,AAR0,alpha_mean,alpha_2012,R,N,imbalance_mean,mmSLE_mean,imbalance_mean,mmSLE_mean,id\n')
                    name = df["name"]
                    region = df["region"]
                    # R = df["R"]**2
                    volume = df["volume"]
                    area = df["area"]
                    gl_type = df["type"].values
                    alpha_mean = df["alpha_mean"]
                    alpha_2012 = df["alpha_2012"]
                    mmSLE_mean = df["mmSLE_mean"]
                    mmSLE_2012 = df["mmSLE_2012"]
                    alpha_2018 = df["alpha_2018"]
                    mmSLE_2018 = df["mmSLE_2018"]
                    alpha_2019 = df["alpha_2019"]
                    mmSLE_2019 = df["mmSLE_2019"]
                    AAR_mean = df["AAR_mean"]
                    AAR0 = df["AAR0"]
                    valid_flag = df["valid_flag"]
                    n=len(df.R)
    
                    # print(fn,np.nanmean(df.R))
                    du=1
                    if du:
                        n=len(AAR0)
                        
                        tot_volume=sum(volume)
                        
                        x=mmSLE_2012 ; varnam='mmSLE 2012' ; axisname='mm SLE 2012'
                        x=df.R ; varnam='R' ; axisname='correlation'
                        
                        # sum_mean_test=0.
                        # sum_2012_test=0.
                        
                        # ------------------------------------------------ loop over sectors
                        # for k in range(0,n):
                            # if np.isfinite(alpha_mean[k]):sum_mean_test+=(1-alpha_mean[k]*volume[k]
                            # if np.isfinite(alpha_2012[k]):sum_2012_test+=alpha_2012[k]*volume[k]
                        
                        # ------------------------------------------------ loop over treatments
                        for jj in range(0,3):
                            if jj==0:
                                typechoice='TW'
                                type_choice_name='TW_only'
                            if jj==1:
                                typechoice='LT'
                                type_choice_name='LT_only'
                                if typechoice=='LT':
                                    for k in range(0,n):
                                        if gl_type[k]=='ice_cap':
                                            print('ice cap is LT',name[k])
                                            gl_type[k]='LT'                
                            if jj==2:
                                typechoice='all'
                                type_choice_name='TW_and_LT'
                                if typechoice=='all':
                                    for k in range(0,n):
                                        gl_type[k]='all'
                                        
                            # if jj==3:
                            #     typechoice='ice_cap'
                            #     type_choice_name='ice_caps'
                            #     # if typechoice=='ice_cap':
                            #     #     for k in range(0,n):
                            #     #         gl_type[k]='ice_cap'
            
                            if plt:
                                plt.hist(df.R, bins=30)
                                plt.ylabel('frequency')
                                plt.xlabel(axisname)
                                           
                            if wo:
                                out_fn='/Users/jason/Dropbox/ELA/stats/imbalance/SLR_committed_'\
                                    +type_choice_name+'_'+SMB_or_TMB+'_ALB'+devname[alb_dev_index]+'_'\
                                        +RCM[mm]+'_'+volume_name[volume_index]+\
                                            '_SID'+SID_devname[SID_dev_index]+\
                                            gamma_name+\
                                                '_v'+versionx+'.csv'
                                                
                                out_concept=open(out_fn,'w')
                                # out_fn='/Users/jason/Dropbox/ELA/stats/imbalance/'+str("{:02d}".format(cc))+'SLR_committed_'\
    
                                out_concept.write('region,n catchments,area sq km,area fraction,volume cubic km,volume fraction,disiquilibrium perpetual 2000-2019 mm SLE,disiquilibrium perpetual 2012 mm SLE,disiquilibrium perpetual 2018 mm SLE,disiquilibrium perpetual 2019 mm SLE,specific disequilibrium 2000-2019,specific disequilibrium 2012,specific disequilibrium 2018,specific disequilibrium 2019,Gt 2000-2019,Gt 2012,Gt 2018,Gt 2019,Gt00,Gt01,Gt02,Gt03,Gt04,Gt05,Gt06,Gt07,Gt08,Gt09,Gt10,Gt11,Gt12,Gt13,Gt14,Gt15,Gt16,Gt17,Gt18,Gt19\n')
                            
                            sum_all_mean=0.
                            sum_all_2012=0.
                            sum_all_2018=0.
                            sum_all_2019=0.
                            sum_all_area=0.
                            sum_all_volume=0.
                            sum_all_sector=0.
                            sum_by_year_all=np.zeros(20)
                        
                            for region_index in range(0,n_regions):
                                # print(region[region_index])
                                sum_2012=0.
                                sum_2018=0.
                                sum_2019=0.
                                sum_mean=0.
                                sum_volume=0.
                                sum_area=0.
                                n_sectors=0.
                                sum_by_year=np.zeros(20)
                                
                                for k in range(0,n):
                            #        print(k,name[k],gl_type[k])
                            #        print(k,name[k],gl_type[k])
                                    # print(k,gl_type[k],typechoice,valid_flag[k])
                                    if ((gl_type[k]==typechoice)&(valid_flag[k]>0)):
                                    # if ((gl_type[k]==typechoice):
                        #            if ((gl_type[k]==typechoice)&(valid_flag[k]<10)):
                                        if region[k]==regions[region_index]:
                        #                    if abs(alpha_mean[k])<0.25:
                                            if ((np.isfinite(alpha_mean[k])) & (alpha_mean[k]>0)):
                                                sum_mean+=(alpha_mean[k]**gamma-1)*volume[k]
                                            if ((np.isfinite(alpha_2012[k])) & (alpha_2012[k]>0)):
                                                sum_2012+=(alpha_2012[k]**gamma-1)*volume[k]
                                            if ((np.isfinite(alpha_2018[k])) & (alpha_2018[k]>0)):
                                                sum_2018+=(alpha_2018[k]**gamma-1)*volume[k]
                                            if ((np.isfinite(alpha_2019[k])) & (alpha_2019[k]>0)):
                                                sum_2019+=(alpha_2019[k]**gamma-1)*volume[k]
                                            for i in range(0,20):
                                                if ( (np.isfinite(df["a"+str(f"{i:02d}")][k])) & (df["a"+str(f"{i:02d}")][k]>0) ):
                                                    # print(df.columns)
                                                    sum_by_year[i]+=(df["a"+str(f"{i:02d}")][k]**gamma-1)*volume[k]
                                                    if ~np.isfinite(sum_by_year[i]):x()
                                            sum_area+=area[k]
                                            sum_volume+=volume[k]
                                            n_sectors+=1
                                        # print(region[region_index],region_index)
                                    # volume_frac_2012=(sum_2012/tot_volume)*100
                                    # volume_frac_2018=(sum_2018/tot_volume)*100
    
                                    # volume_frac_2019=(sum_2019/tot_volume)*100
                                    # volume_frac_mean=(sum_mean/tot_volume)*100
                                    volume_frac=(sum_volume/sum(volume))*100
                                        
                                sum_all_mean+=sum_mean
                                sum_all_2012+=sum_2012
                                sum_all_2018+=sum_2018
                                sum_all_2019+=sum_2019
                                sum_by_year_all+=sum_by_year
                                sum_all_area+=sum_area
                                sum_all_volume+=sum_volume
                                sum_all_sector+=n_sectors
                                
                                frac_vol=sum_volume/sum(volume)*100.
                                frac_area=sum_area/sum(area)*100.
                            
                                spec_disequil_mean=sum_mean/sum_area*1e9/1e6
                                spec_disequil_2012=sum_2012/sum_area*1e9/1e6
                                spec_disequil_2018=sum_2018/sum_area*1e9/1e6
                                spec_disequil_2019=sum_2019/sum_area*1e9/1e6
                                
                                if wo:
                                    out_concept.write(regions[region_index]+\
                                                      ','+str("%8.0f"%n_sectors).lstrip()+\
                                                      ','+str("%8.3f"%sum_area).lstrip()+\
                                                      ','+str("%8.3f"%frac_area).lstrip()+\
                                                      ','+str("%8.3f"%sum_volume).lstrip()+\
                                                      ','+str("%8.3f"%frac_vol).lstrip()+\
                                                      ','+str("%8.5f"%(-sum_mean/362.)).lstrip()+\
                                                      ','+str("%8.5f"%(-sum_2012/362.)).lstrip()+\
                                                      ','+str("%8.5f"%(-sum_2018/362.)).lstrip()+\
                                                      ','+str("%8.5f"%(-sum_2019/362.)).lstrip()+\
                                                      ','+str("%8.5f"%spec_disequil_mean).lstrip()+\
                                                      ','+str("%8.5f"%spec_disequil_2012).lstrip()+\
                                                      ','+str("%8.5f"%spec_disequil_2018).lstrip()+\
                                                      ','+str("%8.5f"%spec_disequil_2019).lstrip()+\
                                                      ','+str("%.1f"%(sum_mean))+\
                                                      ','+str("%.1f"%(sum_2012))+\
                                                      ','+str("%.1f"%(sum_2018))+\
                                                      ','+str("%.1f"%(sum_2019))+\
                                                      ','+str("%.1f"%(sum_by_year[0]))+\
                                                      ','+str("%.1f"%(sum_by_year[1]))+\
                                                      ','+str("%.1f"%(sum_by_year[2]))+\
                                                      ','+str("%.1f"%(sum_by_year[3]))+\
                                                      ','+str("%.1f"%(sum_by_year[4]))+\
                                                      ','+str("%.1f"%(sum_by_year[5]))+\
                                                      ','+str("%.1f"%(sum_by_year[6]))+\
                                                      ','+str("%.1f"%(sum_by_year[7]))+\
                                                      ','+str("%.1f"%(sum_by_year[8]))+\
                                                      ','+str("%.1f"%(sum_by_year[9]))+\
                                                      ','+str("%.1f"%(sum_by_year[10]))+\
                                                      ','+str("%.1f"%(sum_by_year[11]))+\
                                                      ','+str("%.1f"%(sum_by_year[12]))+\
                                                      ','+str("%.1f"%(sum_by_year[13]))+\
                                                      ','+str("%.1f"%(sum_by_year[14]))+\
                                                      ','+str("%.1f"%(sum_by_year[15]))+\
                                                      ','+str("%.1f"%(sum_by_year[16]))+\
                                                      ','+str("%.1f"%(sum_by_year[17]))+\
                                                      ','+str("%.1f"%(sum_by_year[18]))+\
                                                      ','+str("%.1f"%(sum_by_year[19]))+\
                                                      ' \n')
    # all Greenland totals                            
                            frac_area=sum_all_area/sum(area)*100.
                            frac_vol=sum_all_volume/sum(volume)*100.
                            
                            spec_disequil_all_mean=sum_all_mean/sum_all_area*1e9/1e6
                            spec_disequil_all_2012=sum_all_2012/sum_all_area*1e9/1e6
                            spec_disequil_all_2018=sum_all_2018/sum_all_area*1e9/1e6
                            spec_disequil_all_2019=sum_all_2019/sum_all_area*1e9/1e6
                            
                            if wo:
                                out_concept.write('All'+\
                                                  ','+str("%8.2f"%sum_all_sector).lstrip()+\
                                                  ','+str("%8.2f"%sum_all_area).lstrip()+\
                                                  ','+str("%8.3f"%frac_area).lstrip()+\
                                                  ','+str("%8.3f"%sum_all_volume).lstrip()+\
                                                  ','+str("%8.3f"%frac_vol).lstrip()+\
                                                  ','+str("%8.5f"%(-sum_all_mean/362.)).lstrip()+\
                                                  ','+str("%8.5f"%(-sum_all_2012/362.)).lstrip()+\
                                                  ','+str("%8.5f"%(-sum_all_2018/362.)).lstrip()+\
                                                  ','+str("%8.5f"%(-sum_all_2019/362.)).lstrip()+\
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
                            
                                # os.system('cat '+out_fn)
                        
                        # v=np.where(np.isfinite(alpha_mean)&(area>0)&(area<900)&(alpha_mean>0)&(valid_flag>0))
                        # mean_alpha_0_600=np.nanmean(alpha_mean[v[0]])
                        # c=len(v[0])
                        # print("mean_alpha_0_600",mean_alpha_0_600,c)
                        # v=np.where(np.isfinite(alpha_mean)&(area>=900)&(area<=1400)&(alpha_mean>0)&(valid_flag>0))
                        # mean_alpha_900_1400=np.nanmean(alpha_mean[v[0]])
                        # c=len(v[0])
                        # print("mean_alpha_900_1400",mean_alpha_900_1400,c)
                        # v=np.where(np.isfinite(alpha_mean)&(area>1400)&(alpha_mean>0)&(valid_flag>0))
                        # mean_alpha_gt_1400=np.nanmean(alpha_mean[v[0]])
                        # c=len(v[0])
                        # print("mean_alpha_gt_1400",mean_alpha_gt_1400,c)
                        
                        #print("tot_area_all",tot_area_all)
                        #print("tot_vol_all",tot_vol_all)
                        #print("tot_vol_to shed mean",sum_all_mean/tot_vol_all*100)
                        #print("tot_vol_to shed 2012",sum_all_2012/tot_vol_all*100)
                        
                        #print("sum_mean_temp",sum_mean_test/362.)
                        #print("sum_2012_test",sum_2012_test/362.)