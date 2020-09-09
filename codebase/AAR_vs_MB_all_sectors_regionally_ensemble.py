#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 14:10:13 2020

@author: Jason Box, GEUS, jeb@geus.dk

ensemble of regional-scale mass balance versus AAR for a variety of sectors and according to the 18 member error propagation strategy. Produces Fig. S2, Greenland ice sheet disequilibrium for different types of ice flow sectors. 

outputs  ofile='/Users/jason/Dropbox/ELA/stats/AAR_vs_MB_all_sectors_together/'+sector_scenario+\
                        '_AAR_vs_MB_all_sectors_regionally_ensemble'+\
                        if_icecaps_name+\
                        by_area_name+\
                        gamma_name+\
                        '.csv'
                        
preceded by /Users/jason/Dropbox/ELA/prog/imbalance_new/AAR_vs_MB_all_sectors_regionally.py
    
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

wo=1

th=1 ; th=2
formatx='{x:,.3f}'; fs=24 ; fs=36 ; fs=32
# plt.rcParams['font.sans-serif'] = ['Georgia']
plt.rcParams["font.size"] = fs
plt.rcParams['axes.facecolor'] = 'w'
plt.rcParams['axes.edgecolor'] = 'k'
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 0.8
plt.rcParams['grid.color'] = "#cccccc"
plt.rcParams["legend.facecolor"] ='w'
plt.rcParams["mathtext.default"]='regular'
plt.rcParams['grid.linewidth'] = th/2
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
region = df["region"]
gl_type = df["gl_type"]
sector_type = df["sector_type"]

tot_vol=sum(volume)
tot_area=sum(area)    

volfrac=np.zeros(4)
volfrac[0]=100.
v=np.where(df["sector_type"]=='TW')
volfrac[1]=sum(volume[v[0]])/sum(volume)*100
v=np.where(df["sector_type"]=='LT')
volfrac[2]=sum(volume[v[0]])/sum(volume)*100
volfrac[3]=volfrac[1]

versionx='20200320'


fn='/Users/jason/Dropbox/1km_grid2/sector_info_v3.csv'
df = pd.read_csv(fn, delimiter=",")

devname=["lo","mid","hi"]

regions2=['Southwest (SW)','Central West (CW)','Northwest (NW)','North (NO)','Northeast (NE)','Central East (CE)','Southeast (SE)','All']

sector_scenario_names=['TMB, all sectors','TMB, tidewater sectors','SMB, land terminating sectors','SMB, tidewater sectors']

sector_scenarios=['all_TMB','TW_TMB','LT_SMB','TW_SMB']

for gamma_index in range(0,2):    
    gamma=1.
    gamma_name='_gamma1.0'
    
    if gamma_index:
        gamma=1.25
        gamma_name='_gamma1.25'
    # for j,sector_scenario in enumerate(sector_scenarios[0:1]):
    for j,sector_scenario in enumerate(sector_scenarios):
    # for j,sector_scenario in enumerate(sector_scenarios):
        if j>=0:
        # if j==2:
            for if_icecaps in range(0,1):
                if if_icecaps:
                    if_icecaps_name='_icecaps_only'
                    if_icecaps_name2=', ice caps only'
                    regions=['SW','CW','NW','NO','NE','CE'] ; n_regions=len(regions)
                else:
                    if_icecaps_name=''
                    if_icecaps_name2=''
                    regions=['SW','CW','NW','NO','NE','CE','SE','all'] ; n_regions=len(regions)
                # for by_area in range(0,2):
                for by_area in range(1,2):
                    if by_area:
                        by_area_name='_by_area'
                    else:
                        by_area_name='_by_volume'
                    cum=0.
                    volsum=0.
                    
                    ofile='/Users/jason/Dropbox/ELA/stats/AAR_vs_MB_all_sectors_together/'+sector_scenario+\
                        '_AAR_vs_MB_all_sectors_regionally_ensemble'+\
                        if_icecaps_name+\
                        by_area_name+\
                        gamma_name+\
                        '.csv'
        
                    if wo:
                        out_concept=open(ofile,'w+')
                        out_concept.write(sector_scenarios[j]+'\n')
                        out_concept.write('sector,area,area fraction,volume,volume fraction,disequilibrium perpetual 2000-2019,disequilibrium perpetual 2012,disequilibrium perpetual 2018,specific disequilibrium perpetual 2000-2019,specific disequilibrium perpetual 2012,specific disequilibrium perpetual 2018,TMB\n')
        
                    ofile2='/Users/jason/Dropbox/ELA/stats/AAR_vs_MB_all_sectors_together/'+sector_scenario+\
                        '_AAR_vs_MB_all_sectors_regionally_ensemble'+\
                        if_icecaps_name+\
                        by_area_name+\
                        gamma_name+\
                        '_err.csv'
        
                    out_concept_w_err=open(ofile2,'w+')
                    out_concept_w_err.write('sector,area,area fraction,volume,volume fraction,disequilibrium perpetual 2000-2019,disequilibrium perpetual 2012,disequilibrium perpetual 2018,specific disequilibrium perpetual 2000-2019,specific disequilibrium perpetual 2012,specific disequilibrium perpetual 2018,TMB\n')
        
                    # for region_index,regionx in enumerate(regions[0:1]):
                    for region_index,regionx in enumerate(regions):
                        xtitle_names=['Total Mass Balance, '+regionx+' sectors'+if_icecaps_name2,'Surface Mass Balance, tidewater sectors','Total Mass Balance, land terminating sectors','Surface Mass Balance, tidewater sectors']
                        xtitle_names=['Mass Balance','Mass Balance','Mass Balance','Mass Balance','Mass Balance','Mass Balance']
                        abcd=['a.) TMB vs AAR, '+regionx+' sectors','b.) TMB vs AAR, '+regionx+' tidewater sectors','c.) TMB vs AAR, '+regionx+' land terminating sectors','d.)  SMB vs AAR, '+regionx+' tideawater sectors']
                        abcd=[regions2[region_index],'b.) '+regionx+' TW sectors','c.) '+regionx+' LT sectors','d.)  SMB vs AAR, '+regionx+' TW sectors']
                        abcd=['a.) all sectors','a.) '+regionx+' TW sectors','b.) '+regionx+' LT sectors','d.)  SMB vs AAR, '+regionx+' TW sectors']
    
                        # if if_icecaps:
                        #     tot_vol=sum(volume[(region==regionx)&(gl_type==' ice_cap')])
                        #     tot_area=sum(area[(region==regionx)&(gl_type==' ice_cap')])
                        # else:
                        if j==0:
                            if regionx=='all':
                                tot_vol=sum(volume)
                                tot_area=sum(area)    
                                tot_regional_vol=sum(volume)
                                tot_regional_area=sum(area)
                            else:
                                tot_vol=sum(volume)
                                tot_area=sum(area)    
                                tot_regional_vol=sum(volume[region==regionx])
                                tot_regional_area=sum(area[region==regionx])                
                        if j==1:
                            if regionx=='all':
                                tot_regional_vol=sum(volume[sector_type=='TW'])
                                tot_regional_area=sum(area[sector_type=='TW'])
                            else:
                                v=((region==regionx)&(sector_type=='TW'))
                                tot_regional_vol=np.nansum(volume[v])
                                tot_regional_area=sum(area[v])
                        if j==2:
                            if regionx=='all':
                                tot_regional_vol=sum(volume[sector_type=='LT'])
                                tot_regional_area=sum(area[sector_type=='LT'])
                            else:
                                v=((region==regionx)&(sector_type=='LT'))
                                tot_regional_vol=np.nansum(volume[v])
                                tot_regional_area=sum(area[v])
                        if j==3:
                            if regionx=='all':
                                tot_regional_vol=sum(volume[sector_type=='TW'])
                                tot_regional_area=sum(area[sector_type=='TW'])
                            else:
                                v=((region==regionx)&(sector_type=='TW'))
                                tot_regional_vol=np.nansum(volume[v])
                                tot_regional_area=sum(area[v])
    
                        volsum+=tot_regional_vol
                
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
                                                regionx+'_'+sector_scenario+'_ALB'+devname[ALB_dev_index]+'_'+RCM[mm]+'_'+\
                                                    volume_name[volume_index]+'_SID'+SID_devname[SID_dev_index]+\
                                                        by_area_name+\
                                                        if_icecaps_name+\
                                                        '_v'+versionx+'.csv'
                                            # os.system('ls -lF '+fn)
                                            # print(cc,fn)
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
                            
                            df_err=pd.read_csv('/Users/jason/Dropbox/ELA/stats/imbalance/_ensemble_mean.csvTW_and_LT.csv')
                            df_err.columns
                            
                            x=df_ensemble_mean.mb
                            xerr=df_ensemble_std.mb
                        
                            y=df_ensemble_mean.aar
                            yerr=df_ensemble_std.aar
                            
                            year=df1.year
                            
                            plt.close()
        
                            plt.errorbar(x, y, yerr=[yerr, yerr], xerr=xerr,fmt='.',c='w', ecolor='purple', capthick=30,capsize=10, 
                            elinewidth=th,
                            markeredgewidth=th)
                    
                            # plt.scatter(x, y, s=650, facecolors='w', edgecolors='w',linewidth=th,zorder=9)
                            plt.scatter(x, y, s=1200, facecolors='k', edgecolors='k',linewidth=th,zorder=9)
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
                            
                            detrended=y-(m*x+AAR0)
                            std_resid=np.nanstd(detrended)
                            
                            plt.plot(xx, yx, '--',color='grey',linewidth=th*2)
                            
                            AAR_mean=np.mean(y)
                            alpha_mean=AAR0/AAR_mean
                            
                            # fractional_error=np.mean(x)/np.mean(xerr)
        
                            # alpha_mean_0=AAR0/(AAR_mean-np.mean(yerr))
                            # alpha_mean_1=AAR0/(AAR_mean+np.mean(yerr))
     
                            imbalance_mean=(alpha_mean**gamma-1)*tot_regional_vol
        
                            # imbalance_mean0=(1-alpha_mean_0)*tot_regional_vol
                            # imbalance_mean1=(1-alpha_mean_1)*tot_regional_vol
        
                            # mm_SLE_mean0=-imbalance_mean0/362.
                            # mm_SLE_mean1=-imbalance_mean1/362.
                            
                            # mm_SLE_mean_uncert=abs(mm_SLE_mean1-mm_SLE_mean0)
        
                            mm_SLE_mean=imbalance_mean/362.
        
                            spec_disequil_all_mean=imbalance_mean/tot_regional_area*1000
                            cum+=mm_SLE_mean
                            
                            print('mean SLR',mm_SLE_mean,'cumulative SLR',cum,volsum)
                    
                            mm_SLE_x=np.zeros(20)
                            mm_SLE_err_x=np.zeros(20)
                            spec_disequil_x=np.zeros(20)
                            
                            for i in range(0,20):
                                alpha_x=AAR0/y[i]
                                imbalance_x=(alpha_x**gamma-1)*tot_regional_vol
                                spec_disequil_x[i]=imbalance_x/tot_regional_area*1000
                                mm_SLE_x[i]=imbalance_x/362.
                                alpha_x=AAR0/(y[i]+yerr[i])
                                imbalance_x=(1-alpha_x)*tot_vol
                                mm_SLE_err_x[i]=-imbalance_x/362.
                                print("alpha_x",i+2000,y[i],"mm_SLE",mm_SLE_x[i],mm_SLE_err_x[i])
                    
                            mean_y_err=np.mean(yerr)
                            imbalance_mean0=abs((alpha_mean-std_resid)-1)**gamma*tot_vol
                            mm_SLE_mean0=imbalance_mean0/362.
                            # print(mm_SLE_mean0)
                    
                            imbalance_mean1=abs((alpha_mean+std_resid)-1)**gamma*tot_vol
                            mm_SLE_mean1=imbalance_mean1/362.
                            
                            # print(mm_SLE_mean1)
                            
                            mm_err=abs(mm_SLE_mean1-mm_SLE_mean0)/2.
                            # if regionx=='NO':
                            #     mm_err=abs(mm_SLE_mean)*0.5
                            if j==1:mm_err=abs(mm_SLE_mean)*0.5
                            if j==2:mm_err=abs(mm_SLE_mean)*0.5
                            if j==3:mm_err=abs(mm_SLE_mean)*0.5
                            # alpha_err=AAR0/y[i]
                            if j==0 and regionx=='SW':mm_err=abs(mm_SLE_mean)*0.2
                            if regionx=='NO' and j==1:mm_err=abs(mm_SLE_mean)*0.9
                            # m_err=abs((std_resid-1))**gamma*tot_vol
                            yos_text=0.004
                            
                            for i in range(0,20):
                              plt.text(x[i], y[i]-yos_text/10, str(year[i])[2:4], \
                                  horizontalalignment='center',verticalalignment='center', \
                                  color='w',zorder=10,fontsize=28)
                             
                            plt.gca().yaxis.set_major_formatter(StrMethodFormatter(formatx))
                            plt.xlabel(xtitle_names[j]+', Gt y$^{-1}$')
                            # plt.title(sector_scenario_names[j]+' '+regionx)
                            plt.ylabel('Accumulation Area Ratio (AAR)')
                            plt.gca().spines['right'].set_color('none')
                            plt.gca().spines['top'].set_color('none')
                            xos=np.std(x)/2
                            yos=np.std(y)
                            if sector_scenario=='TW_SMB':
                                xos=20
                                yos=0.05
                            # if sector_scenario=='LT_SMB':xos=10
                            plt.xlim(np.min(x)-xos*1.2,np.max(x)+xos*2.5)
                            if sector_scenario=='LT_SMB':
                                yos=0.03
                            plt.ylim(np.min(y)-yos,np.max(y)+yos)
                            osxx=0.002
                            if regionx=='all':xos/=2
                            xos_text=xos/2
                            # xx=np.linspace(np.min(x)-xos*2, 0+xos/2,2)
                            xx=np.linspace(0, 0+xos/2,2)
                            if sector_scenario=='TW_SMB':
                                xx = np.linspace(np.min(x)-xos, np.max(x)+xos/2,2)
                            yx = [AAR0,AAR0]
                            plt.plot(xx, yx, color='b',linewidth=th*2,zorder=20)
                            plt.text(xx[1]+xos_text,AAR0-yos_text,'AAR$_0$\n'+str("%8.3f"%AAR0).lstrip(),color='b',zorder=12)
                            
                            yx = [AAR_mean,AAR_mean]
                            plt.plot(xx, yx, color='r',linewidth=th*2,zorder=20)
                            #                    plt.text(np.min(x)+xos,yx[0]+yx[0]*0.005,'AAR$_0$ = '+str("%8.3f"%AAR0).lstrip(),color='b')
                            if regionx=='CE':yos_text*=4
                            if regionx=='NE':yos_text*=2
                            if regionx=='NO':yos_text*=4
                            plt.text(xx[1]+xos_text,AAR_mean-yos_text,'AAR$_{2000-2019}$\n'+str("%8.3f"%AAR_mean).lstrip(),color='r')
                            
                            props = dict(boxstyle='round', facecolor='w',edgecolor='grey',alpha=1)
                        
                            fig = plt.gcf()
                            ax = fig.add_subplot(111)
        
                            cc=1    ;   xx0=0.03    ;   yy0=0.92    ;   dy=0.06
                            # txt='ice volume = '+str("%8.1f"%volfrac[j]).lstrip()+'%'+\
                            txt=abcd[j]
                            plt.text(xx0, yy0+cc*dy,txt,color='k',
                                transform=ax.transAxes, fontsize=fs*1.4,
                                verticalalignment='top', bbox=props)    ;   cc+=1
        
                            cc=1    ;   xx0=0.4    ;   yy0=0.14    ;   dy=0.06
                            if regionx=='NE':xx0=0.55
                            if regionx=='NO' and j==1:xx0=0.1
                            if regionx=='NO' and j==2:xx0=0.65
                            # x()
                            # txt='ice volume = '+str("%8.1f"%volfrac[j]).lstrip()+'%'+\
                            txt='alpha = '+str("%8.3f"%alpha_mean).lstrip()+'±'+str("%8.3f"%mean_y_err).lstrip()+\
                                '\nSLE = '+str("%8.0f"%mm_SLE_mean).lstrip()+'±'+str("%8.0f"%mm_err).lstrip()+' mm'+\
                                '\nR = '+str("%8.3f"%R).lstrip()+', 1-p '+oneminusp_string
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
                            
                            propsk = dict(boxstyle='round', fc='k',facecolor='k',edgecolor='grey',alpha=1)
    
                            du=0
                            if du:
                                cc=0    ;   xx0=0.72    ;   yy0=0.3    ;   dy=0.06
                                plt.text(xx0, yy0+cc*dy,'2 digit year',color='w',
                                    transform=ax.transAxes,#, fontsize=9
                                    verticalalignment='top', bbox=propsk)   
                            
                            ly='p'
            
                            if ly=='x': plt.show()
                            
                            fig_path='/Users/jason/Dropbox/ELA/Figs/AAR_vs_MB_all_sectors_together/'
                            figname=fig_path+regionx+'_'+sector_scenario+by_area_name+if_icecaps_name+gamma_name+'.png'
            
                            if ly=='p':plt.savefig(figname, bbox_inches='tight', dpi=250)
                            # figname=fig_path+sector_scenario+'.eps'
                            # plt.savefig(figname)
                            
                            # for i,regionx in enumerate(regions):
                    
                            # df = pd.DataFrame(columns=['year','slc'])
                            # df["year"]=np.arange(2000,2020)
                            # df["slc"]=mm_SLE_x
                            # df.to_csv('/Users/jason/Dropbox/ELA/stats/AAR_vs_MB_all_sectors_together/'+regionx+'_ensemble_SLC.csv', sep=',')
        
        
                            if wo:
                                out_concept.write(regionx+\
                                              ','+str("%.0f"%tot_regional_area)+\
                                              ','+str("%.2f"%(tot_regional_area/tot_area))+\
                                              ','+str("%.0f"%tot_regional_vol)+\
                                              ','+str("%.2f"%(tot_regional_vol/tot_vol))+\
                                              ','+str("%.0f"%mm_SLE_mean)+\
                                              ','+str("%.0f"%mm_SLE_x[12])+\
                                              ','+str("%.0f"%mm_SLE_x[18])+\
                                              ','+str("%.0f"%spec_disequil_all_mean)+\
                                              ','+str("%.0f"%spec_disequil_x[12])+\
                                              ','+str("%.0f"%spec_disequil_x[18])+\
                                              ','+str("%.0f"%(np.nansum(x)/20.))+\
                                              ' \n')
    
                                out_concept_w_err.write(regionx+\
                                              ','+str("%.0f"%tot_regional_area)+\
                                              ','+str("%.2f"%(tot_regional_area/tot_area))+\
                                              ','+str("%.0f"%tot_regional_vol)+\
                                              ','+str("%.2f"%(tot_regional_vol/tot_vol))+\
                                              ','+str("%.0f"%mm_SLE_mean)+\
                                                  '±'+str("%.0f"%(mm_err))+\
                                              ','+str("%.0f"%mm_SLE_x[12])+\
                                                  '±'+str("%.0f"%(df_err['disiquilibrium perpetual 2012 mm SLE'][region_index]))+\
                                              ','+str("%.0f"%mm_SLE_x[18])+\
                                                  '±'+str("%.0f"%(df_err['disiquilibrium perpetual 2018 mm SLE'][region_index]))+\
                                              ','+str("%.0f"%spec_disequil_all_mean)+\
                                                  '±'+str("%.0f"%(df_err['specific disequilibrium 2000-2019'][region_index]))+\
                                              ','+str("%.0f"%spec_disequil_x[12])+\
                                                  '±'+str("%.0f"%(df_err['specific disequilibrium 2012'][region_index]))+\
                                              ','+str("%.0f"%spec_disequil_x[18])+\
                                                  '±'+str("%.0f"%(df_err['specific disequilibrium 2018'][region_index]))+\
                                              ','+str("%.0f"%(np.nansum(x)/20.))+\
                                              ' \n')          
        
                                # out_concept_w_err.write(regionx+\
                                #               ','+str("%.0f"%tot_regional_area)+\
                                #               ','+str("%.2f"%(tot_regional_area/tot_area))+\
                                #               ','+str("%.0f"%tot_regional_vol)+\
                                #               ','+str("%.2f"%(tot_regional_vol/tot_vol))+\
                                #               ','+str("%.0f"%mm_SLE_mean)+\
                                #                   '±'+str("%.0f"%(df_err['disiquilibrium perpetual 2000-2019 mm SLE'][region_index]))+\
                                #               ','+str("%.0f"%mm_SLE_x[12])+\
                                #                   '±'+str("%.0f"%(df_err['disiquilibrium perpetual 2012 mm SLE'][region_index]))+\
                                #               ','+str("%.0f"%mm_SLE_x[18])+\
                                #                   '±'+str("%.0f"%(df_err['disiquilibrium perpetual 2018 mm SLE'][region_index]))+\
                                #               ','+str("%.0f"%spec_disequil_all_mean)+\
                                #                   '±'+str("%.0f"%(df_err['specific disequilibrium 2000-2019'][region_index]))+\
                                #               ','+str("%.0f"%spec_disequil_x[12])+\
                                #                   '±'+str("%.0f"%(df_err['specific disequilibrium 2012'][region_index]))+\
                                #               ','+str("%.0f"%spec_disequil_x[18])+\
                                #                   '±'+str("%.0f"%(df_err['specific disequilibrium 2018'][region_index]))+\
                                #               ','+str("%.0f"%(np.nansum(x)/20.))+\
                                #               ' \n')                            
    
                    for l in range(0,9):out_concept.write(',\n')
    
                    out_concept.close()
                    out_concept_w_err.close()
    
    os.system('cat /Users/jason/Dropbox/ELA/stats/AAR_vs_MB_all_sectors_together/*le_by_area*'+gamma_name+'* > /Users/jason/Dropbox/ELA/stats/AAR_vs_MB_all_sectors_together/cat_AAR_vs_MB_all_sectors_together_'+gamma_name+'.csv')