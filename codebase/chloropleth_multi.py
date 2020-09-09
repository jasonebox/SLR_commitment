#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 14:10:15 2020

@author: Jason Box, GEUS, jeb@geus.dk

make chloropleth maps for a variety of parameters: "R","alpha_mean","alpha_2012","Mdot",'equivalent_ablation','ELA_trend','ELA_mean','ELA_mean_doy

"""

ly='x'
do_gif=0
plt_map=1
plt_hist=1
plt_map_sep=1
annotate_map=1

import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import geopandas as gpd
from matplotlib.patches import Rectangle

# plt.rcParams['font.sans-serif'] = ['Georgia']
plt.rcParams['axes.facecolor'] = 'white'
plt.rcParams['axes.edgecolor'] = 'black'
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 1
plt.rcParams['grid.linewidth'] = 1
plt.rcParams['grid.color'] = "grey"
fs=24
fs=18
plt.rcParams["font.size"] = fs
plt.rcParams["mathtext.default"]='regular'

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
    height *= rect[3]
    subax = fig.add_axes([x,y,width,height])
    x_labelsize = subax.get_xticklabels()[0].get_size()
    y_labelsize = subax.get_yticklabels()[0].get_size()
    x_labelsize *= rect[2]**0.5
    y_labelsize *= rect[3]**0.5
    subax.xaxis.set_tick_params(labelsize=x_labelsize)
    subax.yaxis.set_tick_params(labelsize=y_labelsize)
    return subax

# colormaps_filename = '/Users/jason/Dropbox/computer2/python/paraview_colormaps.pkl'
# with open(colormaps_filename, 'rb') as f:
#     pw_cmaps = pickle.load(f)

type_choice_name=['TW_only','LT_only','TW_and_LT']
SMB_or_TMB='TMB'
versionx='20200320'
# versionx='20200611'

alb_devname=["lo","mid","hi"]
SID_devname=["0.9","1.0","1.1"]

# ------------------------------------------------ loop over RCMs
RCM=['MAR','RACMO','ensemble']
# for mm in range(0,1):
# for mm in range(0,1):
for mm in range(2,3):
    # ------------------------------------------------ loop over albedo uncertainty
    # for dev_index in range(0,3):
    for alb_dev_index in range(1,2):
        # ------------------------------------------------ loop over glacier type combinations
        # for type_choice_index in range(0,3):
        for type_choice_index in range(0,1):
            cc=0
            fns=['']*36
            # ------------------------------------------------ loop over SID uncertainty
            # for SID_dev_index in range(0,3):
            for SID_dev_index in range(1,2):
                # ------------------------------------------------ loop over volume treatments
                volume_name=['unscaled','scaled']
                # for volume_index in range(0,2):
                # for volume_index in range(1,2):
                for volume_index in range(0,1):

                    # -----------------------------------------------------------------------------  
                    fn='/Users/jason/Dropbox/ELA/ancil/mouginot/output/ice_sheet_and_ice_cap_sectors.shp'
                    final_crs = {'init': 'epsg:3413'}
                    gdf= gpd.read_file(fn).to_crs(final_crs) 
                    
                    # read in statistics file for example
                    fn='/Users/jason/Dropbox/ELA/stats/imbalance/imbalance_'+\
                        SMB_or_TMB+'_ALB'+alb_devname[alb_dev_index]+'_'+RCM[mm]+'_'+\
                            volume_name[volume_index]+'_SID'+SID_devname[SID_dev_index]+\
                                '_v'+versionx+'.csv'
                    # fn='/Users/jason/Dropbox/ELA/stats/imbalance/_ensemble_imbalance_mean.csv'
                    # os.system('ls -lF '+fn)
                    df=pd.read_csv(fn, delimiter=",")
                    print(df.columns)
                    df["equivalent_ablation"]=df.SID/df.SMB
                    n=len(df.name)
                    
                    variables=["R","alpha_mean","alpha_2012","Mdot",'equivalent_ablation','ELA_trend','ELA_mean','ELA_mean_doy']
                    lo=[-1,0.8,0.,-500,-4,-200,0,180]
                    hi=[1,1.03,1.03,500,4,200,1800,230]
                    lo_hist=[-0.5,0.3,0.,-2600,-3.8,-300,0,180]
                    hi_hist=[1,1.2,1.2,1800,3.8,400,2200,250]
                    varname=['correlation','equilibrium departure','equilibrium departure 2012','specific mass balance','SID÷SMB', 'ELA change','ELA mean','ELA_mean_doy']
                    
                    # -------------------------------------------------------------------- loop over variables
                    for i,var in enumerate(variables):
                        print(var)
                        # if var=="alpha_mean":
                        # if var=="alpha_2012":
                        # if var=="R":
                        # if var=="Mdot":
                        if var=="ELA_trend":
                        # if var=="ELA_mean":
                        # if var=="ELA_mean_doy":
                        # if var=="equivalent_ablation":
                            gdf[var]=np.nan
                            gdf["SID"]=np.nan
                            gdf["lat"]=np.nan
                            gdf["lon"]=np.nan
                            gdf["ELA_corr_sig"]=np.nan
                            for k in range(0,n):
                                v=np.where(gdf.NAME==df.name[k])            
                                if len(v[0])==1:
                                    # if df.name[k][0:3]=='IC_':
                                    #     print(df.name[k])
                                    #     df[var][k]=np.nan
                                    # print(gdf[var].iloc[v[0][0]],df[var][k])
                                    gdf[var].iloc[v[0][0]]=df[var][k]
                                    gdf.lat.iloc[v[0][0]]=df.lat[k]
                                    gdf.lon.iloc[v[0][0]]=df.lon[k]
                                    gdf.SID.iloc[v[0][0]]=df.SID[k]
                                    gdf.ELA_corr_sig.iloc[v[0][0]]=df.ELA_corr_sig[k]

                                    # if df.lat[k]> 75 and df.lon[k]<-44 and df[var][k] > 0: 
                                    # if df.lon[k]>-44 and df[var][k] > 0: 
                                    # print(df.name[k][0:3])

                                    # if df.name[k]=='DIEBITSCH': 
                                    # if df.name[k]=='MORRIS_JESUP': 
                                    # if df.name[k]=='NORDENSKIOLD_GLESCHER_NW': 
                                    # if df.name[k]=='HUMBOLDT_GLETSCHER': 

                                        # if (df[var][k]) > 40 and df.lat[k]< 64 and df.lat[k]> 6 and df.lon[k]<-44 and df.area[k]>3000: 
                                        # print(df.region[k],"|",df.type[k],"|",df.name[k].replace("_", " ").title(),"| lat: ",df.lat[k],"| Mdot:",str("%8.0f"%df[var][k]).lstrip(),"kg/m2 | area:",f"{df.area[k]:,.0f}","km2| SID:",df.SID[k],'Gt/y','| '+RCM[mm]+' SMB:',df.SMB[k],'Gt/y')
                                    # if np.isnan(df[var][k]): 
                                    # if df[var][k] > 0: 
                                        # print("----------- ",df.region[k],df.name[k],'Mdot:',df[var][k],'area:',df.area[k],df.type[k],'SID:',df.SID[k])
                            # break
                            if plt_map:
                                # if var=="alpha_mean":
                                if var=="alpha_2012":
                                    y1=100
                                    v=np.where(gdf[var]>hi_hist[i]) ; gdf[var].iloc[v[0]]=np.nan
                                    v=np.where(gdf[var]<0) ; gdf[var].iloc[v[0]]=np.nan
                                    v=np.where(np.isfinite(gdf[var])) ; n_valid=float(len(v[0]))
                                    v=np.where(gdf[var]>1) ; n_pos=float(len(v[0]))
                                    print()
                                    print(RCM[mm])
                                    print("number of catchments in surplus ",len(v[0]),len(v[0])/n_valid)
                                    v=np.where(gdf[var]<0.5) ; n_pos=float(len(v[0]))
                                    print("number of catchments wiht alpha below 0.5 ",len(v[0]),len(v[0])/n_valid)
    
                                    cm=pw_cmaps['erdc_iceFire_L']
                                    cm='Reds_r'
                                    # v=np.where(gdf.lat>72) ; gdf[var].iloc[v[0]]=np.nan
                                    units=' unitless'; formatx="%.2f" ; formatx2=formatx
    
                                if var=="R": 
                                    y1=48
                                    cm='bwr'
                                    cm='seismic'
                                    cm='seismic'
                                    cm='RdBu_r'
                                    units=' between AAR\nand total mass balance' ; formatx="%.2f"
                                    units='' ; formatx="%.3f" ; formatx2="%.1f"
 
                                if var=="Mdot": 
                                    y1=65
                                    v=np.where(gdf[var]>2000) ; gdf[var].iloc[v[0]]=np.nan
                                    v=np.where(gdf[var]<-2500) ; gdf[var].iloc[v[0]]=np.nan
                                    cm='RdBu_r'
                                    units='kg $m^{-2}$ $y^{-1}$' ; formatx="%.0f" ; formatx2=formatx

                                if var=="equivalent_ablation":
                                    y1=20
                                    v=np.where(gdf[var]<lo[i]) ; gdf[var].iloc[v[0]]=lo[i]
                                    v=np.where(gdf[var]>hi[i]) ; gdf[var].iloc[v[0]]=hi[i]
                                    v=np.where(gdf.SID==0) ; gdf[var].iloc[v[0]]=np.nan

                                    cm='RdBu_r'
                                    units='unitless' ; formatx="%.2f" ; formatx2="%.0f"
 
                                if var=="ELA_trend": 
                                    y1=60
                                    # v=np.where(gdf["ELA_corr_sig"]<0.3) ; gdf[var].iloc[v[0]]=np.nan
                                    # v=np.where(gdf[var]<-2500) ; gdf[var].iloc[v[0]]=np.nan
                                    cm='RdBu_r'
                                    units='m $20y^{-1}$' ; formatx="%.0f" ; formatx2=formatx                                    
                               
                                if var=="ELA_mean": 
                                    y1=33
                                    v=np.where(gdf["ELA_mean"]<100) ; gdf[var].iloc[v[0]]=np.nan
                                    # v=np.where(gdf[var]<-2500) ; gdf[var].iloc[v[0]]=np.nan
                                    cm='viridis'; cm='jet'

                                    units='m a.s.l.' ; formatx="%.0f" ; formatx2=formatx                                    
                                
                                if var=="ELA_mean_doy": 
                                    y1=50
                                    v=np.where(gdf[var]<180) ; gdf[var].iloc[v[0]]=np.nan
                                    # v=np.where(gdf[var]<-2500) ; gdf[var].iloc[v[0]]=np.nan
                                    cm='viridis'; cm='jet'

                                    units='ELA date' ; formatx="%.0f" ; formatx2=formatx     
                                                              
                                print(np.nanmin(gdf[var]),np.nanmax(gdf[var]))
                            
                                plt.subplot(111)
                                ax = plt.subplot(111)
                                if plt_hist:
                                    # plt.figure()
                                    # ------------------------------------------ histogram
                                    plt.subplot(121)
                                    ax = plt.subplot(121)
                                    yj, xj, _ = plt.hist(gdf[var],bins=30)
                                    plt.xlabel(varname[i]+', '+units)
                                    plt.ylabel('count of ice catchments')
                                    plt.ylim(0,y1)
                                    plt.xlim(lo_hist[i],hi_hist[i])
                                   
                                    dx=xj[2]-xj[1]
                                    
                                    plt.axvline(xj[np.argmax(yj)]+dx/2, color='limegreen', linewidth=3)
                                    
                                    props = dict(boxstyle='round', facecolor='w',edgecolor='grey',alpha=0.8)
                                    
                                    # xmin, xmax, ymin, ymax = plt.axis()
        
                                    # yx = [0,ymax] ; xx = [1.0,1.0]
                                    # plt.plot(xx, yx, color='k',linewidth=2)
                                    
                                    # ------------------------------------------ mean
                                    meanx=np.nanmean(gdf[var])
                                    med=np.nanmedian(gdf[var])
                                    v=np.where(np.isfinite(gdf[var])) ; n_valid=len(v[0])
                                    plt.text(0.1, 0.85,'mode = '+str(formatx%xj[np.argmax(yj)]).lstrip()+' '+units+
                                            '\nmedian = '+str(formatx%med).lstrip()+' '+units+
                                            '\nmean = '+str(formatx%meanx).lstrip()+' '+units+
                                            '\nN ='+str(n_valid),
                                            transform=ax.transAxes,color='k',
                                            verticalalignment='top',
                                            bbox=props,fontsize = fs*0.8)
                                    
                                    # yx = [0,ymax] ; xx = [meanx,meanx]
                                    # plt.plot(xx, yx,'--', color='k',linewidth=1.5)
                                    # yx = [0,ymax] ; xx = [med,med]
                                    # plt.plot(xx, yx,':', color='k',linewidth=1.5)
                        
                                # ------------------------------------------ chloropleth map
                                if plt_map_sep:
                                    rect=[1.,0.01,1.2,1.04]
                                    
                                    ax2 = add_subplot_axes(ax,rect)

                                plt.set_cmap(cm)
                                current_cmap = plt.cm.get_cmap()                            
                                # gdf[var][np.isnan(gdf[var])]=lo[i]-1
                                current_cmap.set_under('lightgrey')
                                if var=="alpha_mean":
                                    gdf[var][gdf[var]>1]=hi[i]+10
                                    current_cmap.set_over('powderblue')
                                n=len(gdf[var])
                                if var=="Mdot":
                                    for k in range(0,n):
                                        if gdf[var][k]>=hi[i]:
                                            print('------------------- > high val',gdf.NAME[k],gdf[var][k])
                                            gdf[var][k]=hi[i]
                                        if gdf[var][k]<=lo[i]:
                                            print('------------------- < low val',gdf.NAME[k],gdf[var][k])
                                            gdf[var][k]=lo[i]
                                
                                if plt_map_sep:
                                    ax = gdf.plot(gdf[var],vmin=lo[i],vmax=hi[i],ax=ax2)
                                    leg = ax.get_legend()
                                if plt_map_sep==0:
                                    gdf.plot(gdf[var],vmin=lo[i],vmax=hi[i])

                                plt.axis('off')
    
    
                                # -------------------------------------------------- annotation
                                if annotate_map:
                                    xx0=0.58 ; yy0=0.07 ; dy=-0.05 ; cc=0
                            
                                    plt.text(xx0, yy0+cc*dy,SMB_or_TMB+'\nSMB from '+RCM[mm]+
                                             '\nSID x '+SID_devname[SID_dev_index],
                                     fontsize=fs*0.8,color=(0.,0.,0.),transform=ax.transAxes) ; cc+=1.
                                    
                                    xx0=0.05 ; yy0=0.96 ; dy=-0.05 ; cc=0
                            
                                    # plt.text(xx0, yy0+cc*dy, varname[i]+' between AAR\nand mass balance',
                                    #  fontsize=font_size,color=(0.,0.,0.),transform=ax.transAxes) ; cc+=1.
                                # ------------------------------------------ colorbar
                                fig = ax.get_figure()
                                xx0=0.51 ; dx=0.37 ; yy0=0.125 ; dy=0.04
                                cbax = fig.add_axes([xx0, yy0,dx, dy])          
                                sm = plt.cm.ScalarMappable(cmap=cm,norm=plt.Normalize(vmin=lo[i],
                                                                                      vmax=hi[i])) ; sm._A = []
                                # draw colorbar into 'cbax'
                                fig.colorbar(sm, cax=cbax, format=formatx2,label=varname[i]+', '+units, orientation='horizontal')
    
                                # ------------------------------------------ patch
                                if var=="alpha_mean":
                                    currentAxis = plt.gca()
                                    currentAxis.add_patch(Rectangle((0.836,-0.03)
                                                                ,2,2,fill=True,
                                                                color='powderblue',transform=ax.transAxes))
    
                                fig_path='/Users/jason/Dropbox/ELA/Figs/chloropleth/'+var+'/'
                                os.system('mkdir -p '+fig_path)
                                if ly=='p':
                                    figname=fig_path+'chlor_'+\
                                        variables[i]+'_'+\
                                            SMB_or_TMB+'_ALB'+alb_devname[alb_dev_index]+'_'+RCM[mm]+'_'+\
                                                volume_name[volume_index]+'_SID'+SID_devname[SID_dev_index]+'.png'
                                    plt.savefig(figname, bbox_inches='tight',dpi=250)
                                    # os.system('open '+figname)
                                if ly == 'x': plt.show()
                  
if do_gif == 1:
    print("making .gif")
    os.system('/usr/local/bin/convert -delay 100 -loop 0 '+fig_path+'*.png '+fig_path+'anim_'+var+'.gif')
