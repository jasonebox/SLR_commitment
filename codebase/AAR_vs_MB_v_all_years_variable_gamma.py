#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 22 10:29:25 2019

@author: Jason Box, GEUS, jeb@geus.dk

input is from
/Users/jason/Dropbox/ELA/prog/ELA_from_TSL_AAR_v3.py
/Users/jason/Dropbox/ELA/prog/SID_hydro_year_SID.py
/Users/jason/Dropbox/ELA/prog/SMB_from_TSL_dates.py

out to 
ELA/Figs/AAR_vs/
ELA/stats/

"""
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats
import geopandas as gpd
import locale
locale.setlocale(locale.LC_ALL, '')  # Use '' for auto, or force e.g. to 'en_US.UTF-8'
from matplotlib import colors
from matplotlib.ticker import StrMethodFormatter

ly='x'
wo=1
open_plot=0
thresh=9
do_plot=0
Rthresh=-1.
plt_map=0
annotate_text=0
formatx='{x:,.4f}' ; fs=12
plt_title=0
formatx='{x:,.3f}'; fs=46
plt_2_digit_y=0
plt_regional_renaming=0
prt=0

batch=1
SID_index0=1 ; SID_index1=2
# SID_index0=0 ; SID_index1=4
ALB_index0=1 ; ALB_index1=2
volume_index0=0 ; volume_index1=1
RCM_index0=0 ; RCM_index1=1

do_SMB=0
SMB_or_TMB='SMB'
SMB_or_TMB2='surface mass balance'

if do_SMB==0:
    SMB_or_TMB='TMB'
    SMB_or_TMB2='total mass balance'

def add_subplot_axes(ax,rect):
    fig = plt.gcf()
    box = ax.get_position()
    width = box.width
    height = box.height
    inax_position  = ax.transAxes.transform(rect[0:2])
    transFigure = fig.transFigure.inverted()
    infig_position = transFigure.transform(inax_position)    
    x = infig_position[0]
    y = infig_position[1]
    width *= rect[2]
    height *= rect[3]  # <= Typo was here
    subax = fig.add_axes([x,y,width,height])
    x_labelsize = subax.get_xticklabels()[0].get_size()
    y_labelsize = subax.get_yticklabels()[0].get_size()
    x_labelsize *= rect[2]**0.5
    y_labelsize *= rect[3]**0.5
    subax.xaxis.set_tick_params(labelsize=x_labelsize)
    subax.yaxis.set_tick_params(labelsize=y_labelsize)
    return subax

th=1

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

n_sectors=473
# n_sectors=419

versionx='20200103'
versionx='20200320'
versionx2='20200716'

fn='/Users/jason/Dropbox/1km_grid2/sector_info_v3.csv'
#count,name,region,type,id,lat,lon,area
#os.system('ls -lF '+fn)
# os.system('head '+fn) 
df = pd.read_csv(fn, delimiter=",")
lat = df["lat"]
lon = df["lon"]
area = df["area"]
# gl_type = df["sector_type"]
region = df["region"]
name = df["name"]
pd.set_option('mode.chained_assignment', None)

# print(df.columns)
# print(len(df.name))

# print(sum(df.volume))
# x()
# # v=np.where(df.area<89000)
# # df.volume[v[0]]=df.area[v[0]]*1.6233623010
# temp=0.
# for i in range(0,len(df.area)):
#     if df.area[i]>89000:
#         temp+=df.area[i]
#     if df.area[i]<89000:
#         temp+=df.area[i]*1.6233623010

# print(sum(df.volume),temp,temp/sum(df.volume))


if batch:
    SID_index0=0 ; SID_index1=3
    ALB_index0=0 ; ALB_index1=3
    volume_index0=0 ; volume_index1=1
    RCM_index0=0 ; RCM_index1=2

for gamma_index in range(0,2):    
    gamma=1.
    gamma_name='_gamma1.0'
    
    if gamma_index:
        gamma=1.25
        gamma_name='_gamma1.25'
        
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
                
            name2 = df["name"]
            
            tot_vol=sum(volume)
            tot_areal=sum(area)
            
            valid_flag=[0.]*n_sectors
            # ------------------------------------------------ loop over RCMs
            RCM=['MAR','RACMO']
            for mm in range(RCM_index0,RCM_index1):
            # ------------------------------------------------ loop over albedo uncertainty
                for ALB_dev_index in range(ALB_index0,ALB_index1):
                    fn='/Users/jason/Dropbox/ELA/stats/TSL/'+\
                                name2[0]+'_ELA_v'+versionx+'_'+devname[ALB_dev_index]+'.csv'
                    TMB_annual_tot = pd.read_csv(fn, delimiter=",")
    
                    TMB_annual_tot=TMB_annual_tot.drop(columns=TMB_annual_tot.columns[1:])
                    TMB_annual_tot["TMB"]=0.
    
                    if wo:
                        out_fn='/Users/jason/Dropbox/ELA/stats/imbalance/imbalance_'+\
                            SMB_or_TMB+'_ALB'+devname[ALB_dev_index]+'_'+RCM[mm]+'_'+\
                                volume_name[volume_index]+'_SID'+SID_devname[SID_dev_index]+\
                                    gamma_name+'_v'+versionx2+'.csv'
                        out_concept=open(out_fn,'w')
                        out_concept.write('name,region,type,lat,lon,volume,area,SMBdot,SIDdot,Mdot,ELA_min,ELA_mean,ELA_max,ELA_mean_doy,ELA_trend,ELA_corr,ELA_corr_sig,AAR_mean,AAR_change,AAR0,alpha_mean,alpha_2012,alpha_2018,alpha_2019,R,N,SMB,SMBstd,SID,SIDstd,TMB,imbalance_mean,mmSLE_mean,imbalance_2012,mmSLE_2012,imbalance_2018,mmSLE_2018,imbalance_2019,mmSLE_2019,valid_flag,a00,a01,a02,a03,a04,a05,a06,a07,a08,a09,a10,a11,a12,a13,a14,a15,a16,a17,a18,a19,i00,i01,i02,i03,i04,i05,i06,i07,i08,i09,i10,i11,i12,i13,i14,i15,i16,i17,i18,i19\n')
                    
                    lost_count=0
                    valid_vol_sum=0.
                    valid_area_sum=0.
                    
                    for k in range(0,n_sectors):
                    # for k in range(1,2):
                    # for k in range(0,100): # 
                    # for k in range(200,300): # 
                    # for k in range(4,5): # Russel
                    # for k in range(300,n_sectors):
                    #for k in range(74,75):
                    # for k in range(0,10):
                    #for k in range(101,136):
                        # print(SID_dev_index,k,RCM[mm],volume_name[volume_index],name[k])
                    
                        if do_plot==1:
                            plt.close()
                            # fig = plt.figure(figsize=(12,8))
                        # if df.name[k][0:3]=='IC_':
    
                    #    if name[k]=='OSTENFELD_GLETSCHER':
                        # if name[k][0:3]=='IKE':
                        # if name[k][0:5]=='NANSE':
                        # if name[k]=='NORDENSKIOLD_GLESCHER_NW':
                        # if name[k]=='SERMILIK':
                        # if df.name[k]=='HUMBOLDT_GLETSCHER':
                        # if df.name[k]=='PETERMANN_GLETSCHER':
                        # if df.name[k]=='NANSEN_GLETSCHER':
                        # if df.name[k]=='NIOGHALVFJERDSFJORDEN': 
                        # if df.name[k]=='HELHEIMGLETSCHER': 
                        # if df.name[k]=='IC_1659': #KR ice arm
                        # if df.name[k]=='IC_1110': # Renland ice cap
                        # if df.name[k]=='IC_1203': # CE ice cap
                        # if df.name[k]=='IC_684': # North ice cap
                        # if df.name[k]=='JAKOBSHAVN_ISBRAE':
                        # if df.name[k]=='KOGE_BUGT_C': 
                        # if df.name[k]=='UKAASORSUAQ':
                        # if df.name[k]=='SAQQAP-MAJORQAQ-SOUTHTERRUSSEL_SOUTHQUARUSSEL': 
                        # if df.name[k]=='EIELSON_HARE_FJORD-ROLIGE': 
                        # if df.name[k]=='HELHEIMGLETSCHER': 
    
                        # if name[k]=='QALERALLIT_SERMIAT':
                        # if name[k]=='IC_1715':
                        if region[k]!='SWx':            
                            fn='/Users/jason/Dropbox/ELA/stats/TSL/'+\
                                name2[k]+'_ELA_v'+versionx+'_'+devname[ALB_dev_index]+'.csv'
                            # os.system('ls -lF '+fn) 
                    #        os.system('cat '+fn) 
                    #        year,AAR,ELA,ELA_doy
                            df_ELA = pd.read_csv(fn, delimiter=",")
                            year = df_ELA["year"]
                            AAR = df_ELA["AAR"]     
                            ELA = df_ELA["ELA"]
                            n_years=len(year)
                            
                            fn='/Users/jason/Dropbox/RCM/stats/'+\
                                df.name[k]+'_v'+versionx+'_'+devname[ALB_dev_index]+'_'+RCM[mm]+'_SMB.csv'
                    #        os.system('ls -lF '+fn) 
                    #        os.system('cat '+fn) 
                    #        os.system('open '+fn) 
                            smb = pd.read_csv(fn, delimiter=",")
                            year = smb["year"].astype(int)
                            SMB = smb["smb"]
                            SMB_mean=np.mean(SMB)
                            SMB_std=np.std(SMB)
                            SID_mean=0.
                            spec_SID=0.
    
                            ELA_min=np.nanmin(df_ELA["ELA"])
                            ELA_mean=np.nanmean(df_ELA["ELA"])
                            ELA_max=np.nanmax(df_ELA["ELA"])
                            ELA_mean_doy=np.nanmean(df_ELA["ELA_doy"])
                            m,b= np.polyfit(smb["year"], df_ELA["ELA"], 1)
                            ELA_trend=m*20.
                            ELA_corr_stats=stats.pearsonr(smb["year"], df_ELA["ELA"])
                            ELA_corr=ELA_corr_stats[0]
                            ELA_corr_sig=1-ELA_corr_stats[1]
    
    
                            if ((df["sector_type"][k]=='TW') & (do_SMB==0)):
                                SMB_or_TMB='TMB'
                    #            print(k,name[k],df["sector_type"][k])
                                fn='/Users/jason/Dropbox/SID/Mankoff_2019/polygons/'+\
                                    name[k]+'_SID_ALB'+devname[ALB_dev_index]+'_SID'+SID_devname[SID_dev_index]+\
                                        '_v'+versionx+'.csv'
                                # os.system('ls -lF '+fn) 
                                df_SID = pd.read_csv(fn, delimiter=",")
                                year = df_SID["year"]
                                SID = df_SID["SID"]
                                SID_mean=np.mean(SID)
                                SID_std=np.std(SID)
                                spec_SID=SID_mean/area[k]*1e9/1e6*1000.
    
    
                                SMB-=SID
                                
                            iyear=2000
                            fyear=2019
                                    
                            th=1
                            
                    #        print(AAR)
                            v=np.where( (AAR > 0.) & (AAR < 1.) ) ; y=AAR[v[0]] ; x=SMB[v[0]]
                            TMB_annual_tot["TMB"][v[0]]+=SMB[v[0]]
                            
                            c=len(v[0])
                            if c<thresh:
                                lost_count+=1
                    #            do_plot=1
                    
                    #        if c<thresh:
                    #            print(k,c,name[k],region[k],df["sector_type"][k],'area',area[k])
                            
                            alpha_mean=0.
                            AAR_2012=0. ; AAR_2018=0. ; AAR_2019=0.
                            mean_mass_flux=0.
                            AAR_mean=0. ; AAR_change=0.
                            spec_TMB=np.nan
                            spec_SMB=np.nan
                            
                            imbalance_mean=0. ; mm_SLE_mean=0.
                            imbalance_2012=0. ; mm_SLE_2012=0. ; imbalance_2018=0. ; mm_SLE_2018=0. ; imbalance_2019=0. ; mm_SLE_2019=0.
    
                            
                            if c>=thresh:
                                statsx=stats.pearsonr(x, y)
                                R=statsx[0]
                                if R<Rthresh:
                                    lost_count+=1
                                    # print("corr_bel_zero",name[k],region[k],area[k])
                                if R>Rthresh:
                    #                print(k,c,name[k],region[k],df["sector_type"][k],'R',R)
                                    valid_flag[k]=1
                                    valid_vol_sum+=volume[k]
                                    valid_area_sum+=area[k]
                                    
                                    s=np.argsort(y)
                                    # print('AAR sorted',df_ELA.year[s])
                                    s=np.argsort(x)
                                    # print('MB sorted',df_ELA.year[s])
                                    
                                    if do_plot==1:
                                        # plt.scatter(x,y,color='k',s=1)#,size=1)
                                        plt.scatter(x, y, s=400, facecolors='gray', edgecolors='k',linewidth=th,zorder=9)
    
                                        v2012=np.where(year==2012)
                                        plt.scatter(x[v2012[0]], y[v2012[0]],
                                                    s=400, facecolors='orange', edgecolors='k',linewidth=th,zorder=10)
                                        plt.text(x[v2012[0]]+0.2, y[v2012[0]], '2012',c='orange',zorder=10)
    
                                        # v2012=np.where(year==2015)
                                        # plt.scatter(x[v2012[0]], y[v2012[0]],
                                        #             s=400, facecolors='k', edgecolors='k',linewidth=th,zorder=10)
                                        # plt.text(x[v2012[0]]+0.2, y[v2012[0]], '2015',c='k',zorder=10)
    
                                        # v2012=np.where(year==2010)
                                        # plt.scatter(x[v2012[0]], y[v2012[0]],
                                        #             s=400, facecolors='m', edgecolors='k',linewidth=th,zorder=10)
                                        # plt.text(x[v2012[0]]+0.2, y[v2012[0]], '2010',c='m',zorder=10) 
    
                                        # v2012=np.where(year==2018)
                                        # plt.scatter(x[v2012[0]], y[v2012[0]],
                                        #             s=400, facecolors='c', edgecolors='k',linewidth=th,zorder=10)
                                        # plt.text(x[v2012[0]]+0.2, y[v2012[0]], '2018',c='c',zorder=10)
    
                                        # v2012=np.where(year==2008)
                                        # plt.scatter(x[v2012[0]], y[v2012[0]],
                                        #             s=400, facecolors='brown', edgecolors='k',linewidth=th,zorder=10)
                                        # plt.text(x[v2012[0]]+0.2, y[v2012[0]], '2008',c='brown',zorder=10)
    
                                        # v2012=np.where(year==2013)
                                        # plt.scatter(x[v2012[0]], y[v2012[0]],
                                        #             s=400, facecolors='c', edgecolors='k',linewidth=th,zorder=10)
                                        # plt.text(x[v2012[0]]+0.2, y[v2012[0]], '2013',c='c',zorder=10)  
                                        
                                        plt.gca().yaxis.set_major_formatter(StrMethodFormatter(formatx))
                                        plt.xlabel(SMB_or_TMB2+', Gt/y')
                                        plt.ylabel('AAR')
                                        plt.gca().spines['right'].set_color('none')
                                        plt.gca().spines['top'].set_color('none')
    
                                        # fig, axx = plt.subplots()
                                        # y1, y2 = axx.get_ylim()
                                        # print("--------------------------- ",y1,y2)
    
    # 
    #                                     axes.get_ylim()
                                    
                                    coef = np.polyfit(x,y,1)
                                    m,AAR0 = np.polyfit(x, y, 1)
                                    poly1d_fn = np.poly1d(coef) 
                            
                                    xx = np.linspace(np.min(x), np.max(x),2)
                                    yx = m*xx+AAR0
                                    
                                    if do_plot==1:
                                        plt.plot(xx, yx, '--',color='grey',linewidth=th*2)
                                    
                                    AAR_mean=np.mean(y)
                                    coef_AAR_v_time = np.polyfit(df_ELA["year"][v[0]],df_ELA["AAR"][v[0]],1)
                                    AAR_change=coef_AAR_v_time[0]*20.
                                    mean_mass_flux=np.mean(x)
                                    spec_SMB=SMB_mean/area[k]*1e9/1e6*1000.
                                    spec_TMB=mean_mass_flux/area[k]*1e9/1e6*1000.
                                    alpha_mean=AAR_mean/AAR0
    
                    #                if alpha_mean<0.5:
                    ##                    print('warning',name2[k],str("%9.5f"%AAR_mean).lstrip(),str("%9.5f"%AAR0).lstrip(),str("%9.5f"%alpha_mean).lstrip())
                    #                    print('warning',name2[k],str("%9.5f"%alpha_mean).lstrip())
                                    
                                    # if area[k]<900:alpha_mean=0.8
                                    imbalance_mean=(alpha_mean**gamma-1)*volume[k]
                                    mm_SLE_mean=-imbalance_mean/362.
                                    if prt:print(df.name[k],'R',statsx[0],'alpha',alpha_mean,'mm SLE',mm_SLE_mean)
                                    
                                    AAR_2012=0. ; AAR_2018=0. ; AAR_2019=0.
                                    alpha_by_year=np.zeros(20) ; alpha_by_year[:]=np.nan
                                    imbalance_by_year=np.zeros(20) ; imbalance_by_year[:]=np.nan
                                    
                                    for kk in range(0,c):
                                        if year[kk]==2012:AAR_2012=AAR[kk]
                                        if year[kk]==2018:AAR_2018=AAR[kk]
                                        if year[kk]==2019:AAR_2019=AAR[kk]
                                        alpha_by_year[year[kk]-2000]=AAR[kk]/AAR0
                                        imbalance_by_year[year[kk]-2000]=(alpha_by_year[year[kk]-2000]**gamma-1)*volume[k]
    
                                    alpha_2012=AAR_2012/AAR0
                                    alpha_2018=AAR_2018/AAR0
                                    alpha_2019=AAR_2019/AAR0
                    #                if alpha_2012<0.:
                    #                    print(name2[k],AAR_2012,AAR0)
                    #                if alpha_2012<0.5:
                    #                    print('warning',name2[k],str("%9.5f"%AAR_mean).lstrip(),str("%9.5f"%AAR0).lstrip(),str("%9.5f"%alpha_mean).lstrip())
                    #                    print('alpha_2012<0.5',name2[k],str("%9.5f"%alpha_2012).lstrip(),area[k])
                                    imbalance_2012=(alpha_2012**gamma-1)*volume[k]
                                    mm_SLE_2012=-imbalance_2012/362.
                                    imbalance_2018=(alpha_2018**gamma-1)*volume[k]
                                    mm_SLE_2018=-imbalance_2018/362.
                                    imbalance_2019=(alpha_2019**gamma-1)*volume[k]
                                    mm_SLE_2019=-imbalance_2019/362.
                                                
                                    if do_plot==1:
                                        osxx=0.008 # JAK
                                        # osxx=0.08 #Thule
                                        osxx=0.001 # NIO
                                        osxx=0.002
                                        xos=abs(np.nanmean(x))*1
                                        xx = np.linspace(np.min(x)-xos, 0+xos/2,2)
                                        yx = [AAR0,AAR0]
                                        plt.plot(xx, yx, '--', color='b',linewidth=th*2)
                    #                    plt.text(np.min(x)+xos,yx[0]+yx[0]*0.005,'AAR$_0$ = '+str("%8.3f"%AAR0).lstrip(),color='b')
                                        plt.text(xx[1]+xos,AAR0+osxx,'AAR$_0$\n='+str("%8.3f"%AAR0).lstrip(),color='b',zorder=12)
    
                                        yx = [AAR_mean,AAR_mean]
                                        plt.plot(xx, yx, '--', color='r',linewidth=th*2)
                    #                    plt.text(np.min(x)+xos,yx[0]+yx[0]*0.005,'AAR$_0$ = '+str("%8.3f"%AAR0).lstrip(),color='b')
                                        plt.text(xx[1]+xos,AAR_mean-osxx*3,'AAR$_{2000-2019}$\n='+str("%8.3f"%AAR_mean).lstrip(),color='r')
                                        
                                        ymin=0.5
                                        yos=0.002
                                        if np.min(y)-yos < ymin:ymin=0.
                        
                                        xx = [0,0]
                        #                yx = [np.min(y),AAR0]
                                        yx = [ymin,1.]
                                        plt.plot(xx, yx, '--', color='g',linewidth=th*2)
                                    
                                        # plt.xlim(np.min(x)-xos, np.max(x)+xos)
                                        # plt.xlim(np.min(x)-xos, 0+xos)
                                        # plt.ylim(np.min(y)-yos, np.max(y)+yos)
                                        if df.name[k]=='UKAASORSUAQ':
                                            plt.ylim(np.min(y)-yos*4, 1.01)
                                            plt.xlim(np.min(x)-xos, 1.0)
                                        if df.name[k]=='HUMBOLDT_GLETSCHER':
                                            plt.xlim(np.min(x)-xos, 0+xos)
                                            plt.ylim(np.min(y)-yos, np.max(y)+yos)
                                        if df.name[k]=='IC_684': # CE ice cap
                                            # plt.xlim(np.min(x)-xos, 0+xos)
                                            plt.ylim(0.1, 1.01)
                                        if df.name[k]=='NANSEN_GLETSCHER':
                                            # plt.xlim(np.min(x)-xos, 0+xos)
                                            plt.ylim(0.961, 0.98)
                                        if df.name[k]=='JAKOBSHAVN_ISBRAE':
                                            # plt.xlim(np.min(x)-xos, 0+xos)
                                            plt.ylim(0.91, 0.98)
                                        if df.name[k]=='NIOGHALVFJERDSFJORDEN': 
                                            # plt.xlim(np.min(x)-xos, 0+xos)
                                            plt.ylim(0.967, 0.981)
                                            # if df.name[k]=='HELHEIMGLETSCHER': 
                        # if df.name[k]=='IC_1659': #KR ice arm
                                        if df.name[k]=='IC_1203':
                                            plt.ylim(0.3, 0.9)
                                            # plt.xlim(-0., 0+xos)
                                        if df.name[k]=='IC_1110':
                                            plt.ylim(0.32, 0.86)
                                            # plt.xlim(-0., 0+xos)
                                        if df.name[k]=='KOGE_BUGT_C': 
                                            plt.ylim(0.975, 1.0)
                                            # plt.xlim(-0., 0+xos)
                                        if df.name[k]=='SAQQAP-MAJORQAQ-SOUTHTERRUSSEL_SOUTHQUARUSSEL': 
                                            plt.ylim(0.65, 0.9)
                                        if df.name[k]=='EIELSON_HARE_FJORD-ROLIGE': 
                                            plt.ylim(0.8, 0.925)
                                        if df.name[k]=='HELHEIMGLETSCHER': 
                                            plt.ylim(0.97, 0.995)
    
                                        fancy_title=df.name[k].replace("_", " ").title()
                                        fancy_title=fancy_title.replace("strom","strøm")
                                        fancy_title=fancy_title.replace("ae","æ")
                                        if df.name[k]=='IC_684':fancy_title="North Ice Cap"
                                        if df.name[k]=='IC_1110':fancy_title="Renland Ice Cap"
                                        fancy_area=f"{area[k]:,.0f}"
                                        if plt_title:plt.title(fancy_title+'\n'+df["sector_type"][k]+' sector, '+"%4.1f"%lat[k]+' N, '+str("%5.1f"%abs(lon[k]))+' W, '+fancy_area+' $km^2$')
                                        
                        #                plt.legend(loc='lower left')
                                        if plt_2_digit_y:
                                            for i in range(0,20):
                            #                    print(i,SMB[i], AAR[i])
                                                if ( (AAR[i] > 0.0) & (AAR[i] < 1) ):
                                                    plt.text(SMB[i], AAR[i], str(year[i])[2:4], \
                                                         horizontalalignment='center',verticalalignment='center', \
                                                         color='r')
                                        if annotate_text:
                                            #-----------------------------------------------------------------
                                            cc=0. ; dy=33 ; xx0=1440 ; yy0=450 ; fs=8. # yy0 is from bottom
                                            #-----------------------------------------------------------------
                                            #-----------------------------------------------------------------
                                            plt.text(xx0, yy0-cc*dy, 'R = '+str("%6.3f"%R),
                                                ha='left', va='top',
                                                transform=None,color='g', fontsize=fs)
                                            cc+=1.
                                            #-----------------------------------------------------------------
                                            aa=r'$\alpha$'
                                            plt.text(xx0, yy0-cc*dy, aa+' = '+str("%8.4f"%(alpha_mean)),
                                                ha='left', va='top',
                                                transform=None,color='g', fontsize=fs)
                                            cc+=1.
                                            #-----------------------------------------------------------------
                                            plt.text(xx0, yy0-cc*dy, 'SMB:'+str("%7.2f"%(SMB_mean)+' Gt/y, '+RCM[mm]),
                                                ha='left', va='top',
                                                transform=None,color='g', fontsize=fs)
                                            cc+=1.
                                            #-----------------------------------------------------------------
                                            plt.text(xx0, yy0-cc*dy, 'SID:'+str("%7.2f"%(SID_mean)+' Gt/y'),
                                                ha='left', va='top',
                                                transform=None,color='g', fontsize=fs)
                                            cc+=1.
                                            #-----------------------------------------------------------------
                                            plt.text(xx0, yy0-cc*dy, 'TMB:'+str("%7.2f"%(SMB_mean-SID_mean)+' Gt/y'),
                                                ha='left', va='top',
                                                transform=None,color='g', fontsize=fs)
                                            cc+=1.
                                            #-----------------------------------------------------------------
                                            plt.text(xx0, yy0-cc*dy, 'total volume:'+str("%7.2f"%(100*volume[k]/tot_vol)+' %'),
                                                ha='left', va='top',
                                                transform=None,color='g', fontsize=fs)
                                            cc+=1.
                                            #-----------------------------------------------------------------
                                            plt.text(xx0, yy0-cc*dy, 'N = '+str(c)+' years',
                                                ha='left', va='top',
                                                transform=None,color='g', fontsize=fs)
                                            cc+=1.
                                            #-----------------------------------------------------------------
                                            plt.text(xx0, yy0-cc*dy, 'imbalance 2000-2019:\n'+str("%8.3f"%mm_SLE_mean).lstrip()+' mm SLE',
                                                ha='left', va='top',
                                                transform=None,color='g', fontsize=fs)
                                            cc+=1.                
                                            cc+=1.                
                                            #-----------------------------------------------------------------
                                            plt.text(xx0, yy0-cc*dy, 'imbalance 2012:\n'+str("%8.3f"%mm_SLE_2012).lstrip()+' mm SLE',
                                                ha='left', va='top',
                                                transform=None,color='g', fontsize=fs)
                                            cc+=1.                
                                            cc+=1.
                                            #-----------------------------------------------------------------
                                            plt.text(xx0, yy0-cc*dy, 'alb selection:'+devname[ALB_dev_index],
                                                ha='left', va='top',
                                                transform=None,color='g', fontsize=fs)
                                            cc+=1.
                                            #-----------------------------------------------------------------
                                            plt.text(xx0, yy0-cc*dy, 'volume:'+volume_name[volume_index],
                                                ha='left', va='top',
                                                transform=None,color='g', fontsize=fs)        
                                        if plt_map:
                                            ax = fig.add_subplot(111)
                                            rect=[0.8,0.36,0.75,0.81]
                                            
                                            ax1 = add_subplot_axes(ax,rect)
                            #                final_crs = {'init': 'epsg:3413'}
                                            # -----------------------------------------------------------------------------  
                                            fn='/Users/jason/Dropbox/ELA/ancil/mouginot/output/ice_sheet_and_ice_cap_sectors.shp'
                                            final_crs = {'init': 'epsg:3413'}
                                            gdf= gpd.read_file(fn).to_crs(final_crs)
                                            gdf["temp"]=0.
                                            
                                            for l in range(0,len(gdf.NAME)):
                                                if gdf.NAME[l]==df.name[k]:
                                                    gdf.temp[l]=1
                                            cm='Blues' #; plt.set_cmap(cm)
                                            # current_cmap=plt.set_cmap(cm)
                                            cm=colors.ListedColormap(['C0', 'orangered'])
                                            # plt.set_cmap(cm)
                                            gdf.plot(gdf.temp,vmin=0.,vmax=1,ax=ax1,cmap=cm)
                                            # current_cmap = plt.cm.get_cmap()                        
                                            # current_cmap.set_over('red')
                                            # current_cmap.set_under('')
        
                                            
                        #                    ax = plt.subplot(111)
                                            props = dict(boxstyle='round', facecolor='w',edgecolor='grey',alpha=0.6)
                        #                    plt.text(0.8, 0.15, 'J.Box, GEUS', transform=ax.transAxes, fontsize=9,
                        #                            verticalalignment='top', bbox=props)
                        #                    plt.text(0.7, 0.17,'AAR$_0$ = '+str("%8.4f"%AAR0).lstrip(),color='b',
                        #                            transform=ax.transAxes,#, fontsize=9
                        #                            verticalalignment='top', bbox=props)
                                            plt.text(0.80, 0.09,'2 digit year',color='r',
                                                    transform=ax.transAxes,#, fontsize=9
                                                    verticalalignment='top', bbox=props)
                                            ax1.axis('off')
                        
                        #    out_concept.write('name,region,volume,area,mean mass flux,AAR_mean,AAR0,alpha_mean,
                        #alpha_2012,R,N,imbalance_mean,mmSLE_mean,imbalance_mean,mmSLE_mean,id\n')
                        
                            
                                    if do_plot==1:
                                        if ly == 'x':
                                            plt.show()
                                        
                                        if ly == 'p':
                                            figpath='/Users/jason/Dropbox/ELA/Figs/AAR_vs_'+SMB_or_TMB+'/'
                                            os.system('mkdir -p '+figpath)
                                            figpath_regional='/Users/jason/Dropbox/ELA/Figs/AAR_vs_'+SMB_or_TMB+'/_by_region/'+region[k]+'/'
                                            os.system('mkdir -p '+figpath_regional)
    
                                            figname=figpath+name[k]+'_'+region[k]+'_AAR_vs_'+SMB_or_TMB+'_'+versionx2+'_'+devname[ALB_dev_index]+'_'+RCM[mm]+'_'+volume_name[volume_index]+'.png'
                                            figname_eps=figpath+name[k]+'_'+region[k]+'_AAR_vs_'+SMB_or_TMB+'_'+version2x+'_'+devname[ALB_dev_index]+'_'+RCM[mm]+'_'+volume_name[volume_index]+'.eps'
    
                                            plt.savefig(figname, bbox_inches='tight', dpi=250)
                                            plt.savefig(figname_eps,bbox_inches='tight')                    
                                            if plt_regional_renaming:
                            #----------------------------------------------- by name
                                                
                                                figname=figpath_regional+str("%6.2f"%lat[k]).lstrip()+'_'+region[k]+'_'+name[k]+'_AAR_vs_'+SMB_or_TMB+'_'+versionx+'_'+devname[ALB_dev_index]+'_'+RCM[mm]+'_'+volume_name[volume_index]+'.png'
                                                plt.savefig(figname, bbox_inches='tight', dpi=250)
                                                figpathx=figpath+'_by_latitude/' ; os.system('mkdir -p '+figpathx)
                                                os.system('/bin/cp '+figname+' '+figpathx)
                        
                                                figname=figpath_regional+str("%8.3f"%R).lstrip()+'_'+region[k]+'_'+name[k]+'_AAR_vs_'+SMB_or_TMB+'_'+versionx+'_'+devname[ALB_dev_index]+'_'+RCM[mm]+'_'+volume_name[volume_index]+'.png'
                                                plt.savefig(figname, bbox_inches='tight', dpi=250)
                                                figpathx=figpath+'_by_correlation/' ; os.system('mkdir -p '+figpathx)
                                                os.system('/bin/cp '+figname+' '+figpathx)
                                                
                                                figname=figpath_regional+str("%02d"%c).lstrip()+'_'+region[k]+'_'+name[k]+'_AAR_vs_'+SMB_or_TMB+'_'+versionx+'_'+devname[ALB_dev_index]+'_'+RCM[mm]+'_'+volume_name[volume_index]+'.png'
                                                plt.savefig(figname, bbox_inches='tight', dpi=250)
                                                figpathx=figpath+'_by_N/' ; os.system('mkdir -p '+figpathx)
                                                os.system('/bin/cp '+figname+' '+figpathx)
                        
                                                figname=figpath_regional+str("%8.5f"%(alpha_mean)).lstrip()+'_'+region[k]+'_'+name[k]+'_AAR_vs_'+SMB_or_TMB+'_'+versionx+'_'+devname[ALB_dev_index]+'_'+RCM[mm]+'_'+volume_name[volume_index]+'.png'
                                                plt.savefig(figname, bbox_inches='tight', dpi=250)
                                                figpathx=figpath+'_by_alpha/' ; os.system('mkdir -p '+figpathx)
                                                os.system('/bin/cp '+figname+' '+figpathx)
                            
                                                figname=figpath_regional+df["sector_type"][k]+'_'+str("%8.3f"%R).lstrip()+'_'+region[k]+'_'+name[k]+'_AAR_vs_'+SMB_or_TMB+'_'+versionx+'_'+devname[ALB_dev_index]+'_'+RCM[mm]+'_'+volume_name[volume_index]+'.png'
                                                plt.savefig(figname, bbox_inches='tight', dpi=250)
                                                figpathx=figpath+'_by_type/' ; os.system('mkdir -p '+figpathx)
                                                os.system('/bin/cp '+figname+' '+figpathx)
                                            
                                            if open_plot:
                                                os.system('open '+figname)
                            #                os.system('ls -lF '+figname)
                            
                            if wo:
                                if alpha_mean==0.:alpha_mean=np.nan
                                
                                out_concept.write(name[k]+','+\
                                              region[k]+','+\
                                              df["sector_type"][k]+','+\
                                              str("%.2f"%lat[k])+','+\
                                              str("%.2f"%lon[k])+','+\
                                              str("%.1f"%volume[k])+','+\
                                              str("%.1f"%area[k])+','+\
                                              str("%.3f"%spec_SMB)+','+\
                                              str("%.3f"%spec_SID)+','+\
                                              str("%.3f"%spec_TMB)+','+\
                                              str("%.0f"%ELA_min)+','+\
                                              str("%.0f"%ELA_mean)+','+\
                                              str("%.0f"%ELA_max)+','+\
                                              str("%.0f"%ELA_mean_doy)+','+\
                                              str("%.1f"%ELA_trend)+','+\
                                              str("%.3f"%ELA_corr)+','+\
                                              str("%.3f"%ELA_corr_sig)+','+\
                                              str("%.5f"%AAR_mean)+','+\
                                              str("%.5f"%AAR_change)+','+\
                                              str("%.5f"%AAR0)+','+\
                                              str("%.5f"%alpha_mean)+','+\
                                              str("%.5f"%alpha_2012)+','+\
                                              str("%.5f"%alpha_2018)+','+\
                                              str("%.5f"%alpha_2019)+','+\
                                              str("%.3f"%R)+','+\
                                              str(c)+','+\
                                              str("%.2f"%SMB_mean)+','+\
                                              str("%.2f"%SMB_std)+','+\
                                              str("%.2f"%SID_mean)+','+\
                                              str("%.2f"%SID_std)+','+\
                                              str("%.3f"%mean_mass_flux)+','+\
                                              str("%.3f"%imbalance_mean)+','+\
                                              str("%.3f"%mm_SLE_mean)+','+\
                                              str("%.3f"%imbalance_2012)+','+\
                                              str("%.3f"%mm_SLE_2012)+','+\
                                              str("%.3f"%imbalance_2018)+','+\
                                              str("%.3f"%mm_SLE_2018)+','+\
                                              str("%.3f"%imbalance_2019)+','+\
                                              str("%.3f"%mm_SLE_2019)+','+\
                                              str("%6.0f"%valid_flag[k])+','+\
                                              str("%.5f"%alpha_by_year[0])+','+\
                                              str("%.5f"%alpha_by_year[1])+','+\
                                              str("%.5f"%alpha_by_year[2])+','+\
                                              str("%.5f"%alpha_by_year[3])+','+\
                                              str("%.5f"%alpha_by_year[4])+','+\
                                              str("%.5f"%alpha_by_year[5])+','+\
                                              str("%.5f"%alpha_by_year[6])+','+\
                                              str("%.5f"%alpha_by_year[7])+','+\
                                              str("%.5f"%alpha_by_year[8])+','+\
                                              str("%.5f"%alpha_by_year[9])+','+\
                                              str("%.5f"%alpha_by_year[10])+','+\
                                              str("%.5f"%alpha_by_year[11])+','+\
                                              str("%.5f"%alpha_by_year[12])+','+\
                                              str("%.5f"%alpha_by_year[13])+','+\
                                              str("%.5f"%alpha_by_year[14])+','+\
                                              str("%.5f"%alpha_by_year[15])+','+\
                                              str("%.5f"%alpha_by_year[16])+','+\
                                              str("%.5f"%alpha_by_year[17])+','+\
                                              str("%.5f"%alpha_by_year[18])+','+\
                                              str("%.5f"%alpha_by_year[19])+','+\
                                              str("%.5f"%imbalance_by_year[0])+','+\
                                              str("%.5f"%imbalance_by_year[1])+','+\
                                              str("%.5f"%imbalance_by_year[2])+','+\
                                              str("%.5f"%imbalance_by_year[3])+','+\
                                              str("%.5f"%imbalance_by_year[4])+','+\
                                              str("%.5f"%imbalance_by_year[5])+','+\
                                              str("%.5f"%imbalance_by_year[6])+','+\
                                              str("%.5f"%imbalance_by_year[7])+','+\
                                              str("%.5f"%imbalance_by_year[8])+','+\
                                              str("%.5f"%imbalance_by_year[9])+','+\
                                              str("%.5f"%imbalance_by_year[10])+','+\
                                              str("%.5f"%imbalance_by_year[11])+','+\
                                              str("%.5f"%imbalance_by_year[12])+','+\
                                              str("%.5f"%imbalance_by_year[13])+','+\
                                              str("%.5f"%imbalance_by_year[14])+','+\
                                              str("%.5f"%imbalance_by_year[15])+','+\
                                              str("%.5f"%imbalance_by_year[16])+','+\
                                              str("%.5f"%imbalance_by_year[17])+','+\
                                              str("%.5f"%imbalance_by_year[18])+','+\
                                              str("%.5f"%imbalance_by_year[19])+\
                                                  ' \n')
                    
                    if wo:
                        out_concept.close()
                    #    os.system('cat '+out_fn)
                        os.system('wc -l '+out_fn)
                        
                        # print("N with insufficient sample",lost_count)
                        # print("N with sufficient sample",n_sectors-lost_count)
                        print("valid volume",valid_vol_sum)
                        print("valid volume frac",valid_vol_sum/tot_vol)
                        print("valid_area frac",valid_area_sum/tot_areal)
                        
                        valid_flag=np.asarray(valid_flag)
                        
                        v=np.where(valid_flag<1)
                        # print("area corr_bel_zero",sum(area[v[0]]))
                        # print("mean area corr_bel_zero",np.mean(area[v[0]]))
                        
                        fn='/Users/jason/Dropbox/ELA/stats/imbalance/TMB_annual_ALB'+devname[ALB_dev_index]+'_'+RCM[mm]+'_'+\
                                volume_name[volume_index]+'_SID'+SID_devname[SID_dev_index]+\
                                    '_v'+versionx+'.csv'
                        for i in range(0,20):
                            TMB_annual_tot["year"][i]=i+2000
    
                        TMB_annual_tot.to_csv(fn, sep=',')
