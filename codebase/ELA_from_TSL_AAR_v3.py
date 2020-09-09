#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Jason Box, GEUS, jeb@geus.dk

from daily transient snowline data, retrieve per sector annual minimum AAR, and their days of year also for use in SMB and SID data selection

"""
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
import locale
locale.setlocale(locale.LC_ALL, '')  # Use '' for auto, or force e.g. to 'en_US.UTF-8'
from matplotlib import colors

ly='p'
do_plot=0
open_plot=0
annotatex=0
do_annotation=1
plt_map=0
plt_title=0
th=0.5
fs=50
plt_legend=0

batch=1
ALB_index0=1 ; ALB_index1=2

if batch:
    ALB_index0=0 ; ALB_index1=3

wo=0
wo_all_catchments_table=0
thresh=10
do_break=0

versionx='20200121'
versionx='20200320'
# versionx='20200611'

TSL_or_AAR='TSL'
#TSL_or_AAR='AAR'

region_type='polygons'
region_type='PROMICE'

#plt.rcParams["font.family"] = "sans-serif"
#plt.rcParams['font.sans-serif'] = ['DIN Alternate']
#plt.rcParams['font.sans-serif'] = ['Tahoma']
# plt.rcParams['font.sans-serif'] = ['Georgia']
#http://jonathansoma.com/lede/data-studio/matplotlib/list-all-fonts-available-in-matplotlib-plus-samples/
plt.rcParams["font.size"] = fs
plt.rcParams['axes.facecolor'] = 'w'
plt.rcParams['axes.edgecolor'] = 'k'
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 1
plt.rcParams['grid.linewidth'] = th/2.
plt.rcParams['grid.color'] = "#cccccc"
plt.rcParams["legend.facecolor"] ='w'
plt.rcParams['axes.linewidth'] = th/2. #set the value globally


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

if region_type=='PROMICE':
    sectorx=['QAS','NUK','KAN','UPE','THU','KPC','SCO','TAS']
    name2=sectorx
    n_sectors=len(region_type)

if region_type=='polygons':
    fn='/Users/jason/Dropbox/1km_grid2/sector_info_v3.csv'
    os.system('ls -lF '+fn)
    os.system('head '+fn) 
    df = pd.read_csv(fn)
    
    n_sectors=len(df.name)

i=0

#https://matplotlib.org/3.1.0/gallery/color/named_colors.html
co=['b','c','b','m','c','c','tab:orange','limegreen','blueviolet','purple',
    'k','pink','r','m','c','g','tab:orange','limegreen','blueviolet','purple','m']
syms=['+','+','+','+','+','+','+','+','+','+',
      '*','+','.','+','+','+','2','1','4','3']

syms=['.','.','.','.','.','.','.','.','.','.',
      '.','.','.','.','.','.','.','.','.','.']

iyear=2000
fyear=2019

#v=np.where(name=="UPERNAVIK_ISSTROM_SS")
#print("v",v)

devname=["lo","mid","hi"]

# ------------------------------------------------------------- loop over albedo ranges
for ALB_dev_index in range(ALB_index0,ALB_index1):


    if wo_all_catchments_table:
                ofile_all='/Users/jason/Dropbox/ELA/stats/ELA/ELA_average_all_catchments_v'+versionx+'_'+devname[ALB_dev_index]+'.csv'
                out_concept_all=open(ofile_all,'w+')
                out_concept_all.write('catchment name,sector id,gl_type,region,mean ELA meters,stdev ELA meters,mean day of year,stdev day of year,mean lat,mean lon,std lat,std lon\n')

# ------------------------------------------------------------- loop over sectors
    # for k in range(0,n_sectors):
    for k in range(0,1):
    #for k in range(n_sectors-1,n_sectors):
    # for k in range(54,55):
    # for k in range(400,n_sectors):
    # for k in range(0,31):
    # for k in range(101,131):
#    for k in range(201,221):
    
        # print(k,devname[ALB_dev_index],df.name[k])
        

        # if df.region[k]!='SWx':
        if sectorx[k]!='SWx':
            counts=[0.]*366
            sums=[0.]*366
            means=np.zeros(366) ; means[:]=np.nan
            doys=np.zeros(366)
            
            # if df.name[k]!='ICE_CAPS_NWx':
            if sectorx[k]!='ICE_CAPS_NWx':
            # if df.name[k][0:3]=='IC_':
            # if df.name[k]=='SERMILIK':

                        # if df.name[k]=='DAUGAARD-JENSEN':
        # if df.name[k]=='OSTENFELD_GLETSCHER':
#        if df.name[k]=='SERMILIK':
                # if df.name[k]=='STORSTROMMEN':
            # if df.name[k]=='JAKOBSHAVN_ISBRAE':
            # if df.name[k]=='KOGE_BUGT_C':

                #            if df.name[k]=='PETERMANN_GLETSCHER':

            # if df.name[k]=='UKAASORSUAQ':
        # if df.name[k]=='HUMBOLDT_GLETSCHER':
            # if df.name[k]=='NIOGHALVFJERDSFJORDEN': 
            # if df.name[k]=='HELHEIMGLETSCHER': 
            # if df.name[k]=='IC_1659': #KR ice arm
            # if df.name[k]=='IC_981': # CE ice cap
            # if df.name[k]=='IC_684': # CE ice cap

                if region_type=='polygons': sector=df.id[k]
                if region_type=='PROMICE': sector=sectorx[k]
            
                if wo:
                    ofile='/Users/jason/Dropbox/ELA/stats/TSL/'+df.name[k]+'_ELA_v'+versionx+'_'+devname[ALB_dev_index]+'.csv'
                    out_annual_max_tsl=open(ofile,'w+')
                    out_annual_max_tsl.write('year,AAR,ELA,ELA_doy,lat,lon\n')
            
                plt.close()
                
                for yy in range(iyear,fyear+1):
            
                    if ((yy != 20000)):
#                    if ((yy < 2005)):
    #                if ((yy == 2012)):
                        fn='/Users/jason/Dropbox/ELA/stats/TSL/regional/'+region_type+'/'+sectorx[k]+'_'+str(yy)+'_ELAs_MOD10A1_1000m_mean_vfit.csv'
                        # fn='/Users/jason/Dropbox/ELA/stats/TSL/regional/'+region_type+'/'+str(df.name[k])+'_'+str(yy)+'_ELAs_MOD10A1_1000m_mean_v'+versionx+'.csv'
                        # print(fn)
    #                    os.system('ls -lF '+fn) 
#                        os.system('head '+fn) 
    #                    os.system('cat '+fn) 
    #                    os.system('open '+fn) 
                        df_TSL = pd.read_csv(fn, delimiter=",")
                        print(df_TSL.columns)
                
            #year,day,snowline_selection,snowline_selection2,aar,aar2,meanalb_abl,meanalb_accum,meanalb_all,minalb_abl,minalb_all,area,lat or ELA,lon of ELA
                        
                        year = df_TSL["year"]
                        doyx = df_TSL["day"] ; doy=doyx.values
                        TSLx = df_TSL["snowline_selection_"+devname[ALB_dev_index]] ; TSL=TSLx.values
                        aarxx = df_TSL["aar_"+devname[ALB_dev_index]] ; AAR=aarxx.values
                        tsl_lat = df_TSL["tsl_lat"] ; tsl_lat=tsl_lat.values
                        tsl_lon = df_TSL["tsl_lon"] ; tsl_lon=tsl_lon.values

                        if df.name[k]=='IC_153': #!!! site specific treatment is scary
                            lo=202 ; hi=235
                            TSL = np.where(doy < lo, np.nan, TSL);TSL = np.where(doy > hi, np.nan, TSL) 
                            AAR = np.where(doy < lo, np.nan, AAR);AAR = np.where(doy > hi, np.nan, AAR) 
                            # df.name='FLADE_ISBLINK'
                        if df.name[k]=='IC_6': #!!! site specific treatment is scary
                            lo=160 ; hi=240
                            TSL = np.where(doy < lo, np.nan, TSL);TSL = np.where(doy > hi, np.nan, TSL) 
                            AAR = np.where(doy < lo, np.nan, AAR);AAR = np.where(doy > hi, np.nan, AAR) 
                        if df.name[k]=='IC_1637': #!!! site specific treatment is scary
                            lo=100 ; hi=260
                            TSL = np.where(doy < lo, np.nan, TSL);TSL = np.where(doy > hi, np.nan, TSL) 
                            AAR = np.where(doy < lo, np.nan, AAR);AAR = np.where(doy > hi, np.nan, AAR)                             

                        if df.name[k]=='IC_75': #!!! site specific treatment is scary
                            lo=100 ; hi=250
                            TSL = np.where(doy < lo, np.nan, TSL);TSL = np.where(doy > hi, np.nan, TSL) 
                            AAR = np.where(doy < lo, np.nan, AAR);AAR = np.where(doy > hi, np.nan, AAR)            

                        if df.name[k]=='IC_516': #!!! site specific treatment is scary
                            lo=205 ; hi=235
                            TSL = np.where(doy < lo, np.nan, TSL);TSL = np.where(doy > hi, np.nan, TSL) 
                            AAR = np.where(doy < lo, np.nan, AAR);AAR = np.where(doy > hi, np.nan, AAR)            

                        if df.name[k]=='IC_467': #!!! site specific treatment is scary
                            lo=205 ; hi=235
                            TSL = np.where(doy < lo, np.nan, TSL);TSL = np.where(doy > hi, np.nan, TSL) 
                            AAR = np.where(doy < lo, np.nan, AAR);AAR = np.where(doy > hi, np.nan, AAR)            

                        if df.name[k]=='IC_1470': #!!! site specific treatment is scary
                            lo=200 ; hi=245
                            TSL = np.where(doy < lo, np.nan, TSL);TSL = np.where(doy > hi, np.nan, TSL) 
                            AAR = np.where(doy < lo, np.nan, AAR);AAR = np.where(doy > hi, np.nan, AAR)            

                        if df.name[k]=='IC_1686': #!!! site specific treatment is scary
                            lo=205 ; hi=250
                            TSL = np.where(doy < lo, np.nan, TSL);TSL = np.where(doy > hi, np.nan, TSL) 
                            AAR = np.where(doy < lo, np.nan, AAR);AAR = np.where(doy > hi, np.nan, AAR)            

                        if df.name[k]=='IC_1634': #!!! site specific treatment is scary
                            lo=200 ; hi=280
                            TSL = np.where(doy < lo, np.nan, TSL);TSL = np.where(doy > hi, np.nan, TSL) 
                            AAR = np.where(doy < lo, np.nan, AAR);AAR = np.where(doy > hi, np.nan, AAR)            

                        if df.name[k]=='IC_1335': #!!! site specific treatment is scary
                            lo=170 ; hi=240
                            TSL = np.where(doy < lo, np.nan, TSL);TSL = np.where(doy > hi, np.nan, TSL) 
                            AAR = np.where(doy < lo, np.nan, AAR);AAR = np.where(doy > hi, np.nan, AAR)            

                        if df.name[k]=='IC_1': #!!! site specific treatment is scary
                            lo=210 ; hi=245
                            TSL = np.where(doy < lo, np.nan, TSL);TSL = np.where(doy > hi, np.nan, TSL) 
                            AAR = np.where(doy < lo, np.nan, AAR);AAR = np.where(doy > hi, np.nan, AAR)            

                        if df.name[k]=='IC_857': #!!! site specific treatment is scary
                            lo=195 ; hi=240
                            TSL = np.where(doy < lo, np.nan, TSL);TSL = np.where(doy > hi, np.nan, TSL) 
                            AAR = np.where(doy < lo, np.nan, AAR);AAR = np.where(doy > hi, np.nan, AAR)            

                        y=TSL
                        x=doy
                        
                        for ii in range(1,len(x)):
                            if AAR[ii] < 0 and TSL[ii]>0.1:
    #                            print('before',doy[ii],AAR[ii],AAR[ii-1])
                                AAR[ii]=AAR[ii-1]
    #                            print('after',doy[ii],AAR[ii],AAR[ii-1])
                        
                        
                        ELA=0.
                        ELA_day=0.
                        AAR_min=0.
                        
                        for ii in range(0,len(x)):
                            if y[ii]>0:
                                sums[x[ii]-1]+=y[ii]
                                counts[x[ii]-1]+=1.
        #                    print(yy,counts)
        
                        AAR = np.where(TSL < 0.1, np.nan, AAR)  # Set all AAR < 0 to NaN
                        TSL = np.where(TSL < 0.1, np.nan, TSL)  # Set all AAR < 0 to NaN
        
        #                inv=np.where(TSL < 0) ; TSL[inv[0]]=0. ; AAR[inv[0]]=0.
        #                inv=np.where(TSL > 2100) ; TSL[inv[0]]=0. ; AAR[inv[0]]=0.
        #                inv=np.where(AAR < 0) ; AAR[inv[0]]=0.
                
        #                AAR = np.where(AAR < 0., np.nan, AAR)  # Set all AAR < 0 to NaN

                        # v=np.where(np.isfinite(TSL))
                        # coefs = np.polyfit(doy[v[0]], TSL[v[0]], 2)  # quadratic
                        # fit=coefs[0]*doy**2+coefs[1]*doy+coefs[2]
                        # if coef                        

        
                        plotvar=TSL
                        ytit='meters above sea level'
                    

                        # plt.plot(doy,fit,'r',linewidth=5)
                        # print(k, coefs[0])
                        # if coefs[0]>0:plotvar[:]=np.nan
                        if TSL_or_AAR=='AAR':
                            plotvar=AAR
                            ytit='AAR'
                            #                v=np.where(plotvar < 0.3) ; plotvar[v[0]]=np.nan 
                            plotvar = np.where(plotvar < 0.1, np.nan, plotvar)  # Set all AAR < 0 to NaN
        
        #                    v=np.where(plotvar < 0.3) ; plotvar[v[0]]=np.nan 
                        
            #            print("--------------------------------------------------",yy)
        #                print(TSL)
        #                v=np.where(TSL < 3000)
        #                v=np.where((TSL != 0)&(TSL != np.nan))
        #                print('before')
        #                print('doy',doy)
        #                print('TSL',TSL)
        #                print('AAR',AAR)
                        doy = np.ma.array(doy, mask=np.isnan(TSL)) # Use a mask to mark the NaNs
                        AAR = np.ma.array(AAR, mask=np.isnan(TSL)) # Use a mask to mark the NaNs
                        TSL = np.ma.array(TSL, mask=np.isnan(TSL)) # Use a mask to mark the NaNs
        #                print('after')
        #                print('doy',doy)
        #                print('TSL',TSL)
        #                print('AAR',AAR)
    
                        v2=np.where(TSL > 0)
                        c2=len(v2[0])
                        lon=0.
                        lat=0.                        
                        if c2 == 0:print(df.name[k],df.area[k])
                        if c2 > 0:
                            v=np.where(TSL == np.max(TSL))
                            c=len(v[0])
                           
                            if c==1:
                                ELA=np.max(TSL)
                                ELA_day=doy[v[0]]
                                AAR_min=AAR[v[0]]
                                lat=tsl_lat[v[0]]
                                lon=tsl_lon[v[0]]

            #                    print(yy,c)
                
                            if c > 1:
                                ELA=np.mean(TSL[v[0]])
                                ELA_day=np.mean(doy[v[0]])
                                AAR_min=np.mean(AAR[v[0]])
                                lat=np.mean(tsl_lat[v[0]])
                                lon=np.mean(tsl_lon[v[0]] )
            ##                    print(yy,c)
            #    
            ##                if yy==2012:
            ##                    print('AAR',AAR)
            ##                    print('ELA',ELA)
            ##                    print('ELA_day',ELA_day)
            ##                    print('np.max(TSL)',np.max(temp_TSL))
            ##                    print(yy,c)
            ##                    print(temp_TSL)
            ##                    v=np.where(TSL != np.nan)
            ##                    print(v)
            ##                    print(TSL[v[0]])
            #
        
#                        print(yy,c2,lat,lon)

                        
                        if wo:
                            out_annual_max_tsl.write(\
                                          str(year[yy-2000])+\
                                          ','+str("%8.5f"%AAR_min).lstrip()+\
                                          ','+str("%8.1f"%ELA).lstrip()+\
                                          ','+str("%6.0f"%ELA_day).lstrip()+\
                                          ','+str("%9.4f"%lat).lstrip()+\
                                          ','+str("%9.4f"%lon).lstrip()+\
                                          '\n')
                        if do_plot:
                            # if ((yy == 2002) or (yy == 2010) or (yy == 2018)): #UKAASORSUAQ
                            # if ((yy == 2002) or (yy == 2012) or (yy == 2018)): #KR ice arm
                            if ((yy == 2015) or (yy == 2012) or (yy == 2018)): # Helheim

                            # if ((yy == 2012) or (yy == 2000) or (yy == 2015) or (yy == 2006)):
                            # if ((yy == 2013) or (yy == 2015) or (yy == 2006)): #Humboldt
#                            if ((yy == 2016) or (yy == 2011) or (yy == 2019) or (yy == 2014)):
#                            if ((yy == 2010) or (yy == 2012)):
#                            if ((yy == 2005) or (yy == 2015) or (yy == 2000)):
#                            if ((yy == 2012) or (yy == 2005) or (yy == 2010)):
                            # if ((yy < 20019)):
                
                                if df.name[k]=='NIOGHALVFJERDSFJORDEN'  and yy == 2018:plotvar[130:]=np.nan
                                if df.name[k]=='IC_981'  and yy == 2018:plotvar[150:]=np.nan
                                if df.name[k]=='HUMBOLDT_GLETSCHER'  and yy == 2018:plotvar[130:]=np.nan

                                plt.plot(doy, plotvar, linewidth=th,marker=syms[yy-iyear],
                                         color=co[yy-iyear],
                                         label=str(yy))
                                # if coefs[0]<0:
                                #     print(k, "--------------------------------------------------- invalid")
                                # input("Press Enter to continue...")
                                if TSL_or_AAR=='TSL':
                                    plt.plot(ELA_day, ELA,marker='s',
                                             color=co[yy-iyear],markersize=20)#,label='ELA')
                                    # plt.plot(ELA_day, ELA,marker='s',
                                             # color=co[yy-iyear],markersize=13,fillstyle='none')#,label='ELA')
                #                if TSL_or_AAR=='AAR':
                #                    plt.plot(ELA_day, AAR,marker='o',color=co[yy-iyear],markersize=10,fillstyle='none')
                                
                                plt.xlabel('day of year')
                                plt.ylabel(ytit)
                                if region_type=='PROMICE':
                                    tit=sectorx[k]+' transient snowline and equilibrium line altitude'
                                if region_type=='polygons':
                                    fancy_title=df.name[k].replace("_", " ").title()
                                    fancy_title=fancy_title.replace("strom","strøm")
                                    fancy_title=fancy_title.replace("ae","æ")
                                    fancy_sector_name=df.sector_type[k].replace("x", "")
                                    tit=fancy_title+'\n'+fancy_sector_name+' sector, '+', lat: '+"%4.1f"%df.lat[k]+' N, lon: '+str("%5.1f"%df.lon[k])+', '+f"{df.area[k]:,.0f}"+' $km^2$'
                                    print(tit)
                                if plt_title:plt.title(tit)
                                plt.xlim(145,295)
        

                for ii in range(0,366):
                    doys[ii]=ii+1.
                    if counts[ii]>thresh:means[ii]=sums[ii]/counts[ii]
                plt.plot(doys,means,marker='.',color='#666666',linewidth=th*2,label='mean')        
        #             v=np.where(np.isfinite(means))
        #             coefs = np.polyfit(doys[v[0]], means[v[0]], 2)  # quadratic
        #             fit=coefs[0]*doys**2+coefs[1]*doys+coefs[2]

        #             plt.plot(doys,fit,'r',linewidth=5)
        #             print(k, coefs[0])
        #             # if coefs[0]<0:
        #             #     print(k, "--------------------------------------------------- invalid")
        #             # input("Press Enter to continue...")
                if do_annotation:

                    ax = plt.subplot(111)

                    # rect = [0.88,0.1,0.7,0.7]
                    # ax1 = add_subplot_axes(ax,rect)

                    if plt_legend:
                        ax.legend(prop={'size': fs}) #loc='center left', bbox_to_anchor=(1, 0.5)
                        leg = ax.legend()
                        leg.get_frame().set_linewidth(th/2.)
    
                    if annotatex:
                        props = dict(boxstyle='round', facecolor='w',edgecolor='grey')
                        plt.text(1.02, 0., 'J.Box, GEUS', transform=ax.transAxes, fontsize=9,
                                verticalalignment='top', bbox=props)
                        props = dict(boxstyle='round', facecolor='w',edgecolor='grey')
                        plt.text(1.02, 0.04, devname[ALB_dev_index], transform=ax.transAxes, fontsize=9,
                                verticalalignment='top', bbox=props)        
                    
                    if plt_map:
                    
                        # ax1 = plt.subplot(121)
                        rect = [0.88,0.43,0.7,0.7]
                    
                        ax1 = add_subplot_axes(ax,rect)
    # new
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
                        cm=colors.ListedColormap(['C0', 'indianred'])
                        # plt.set_cmap(cm)
                        gdf.plot(gdf.temp,vmin=0.,vmax=1,ax=ax1,cmap=cm)
                        # current_cmap = plt.cm.get_cmap()                        
                        # current_cmap.set_over('red')
                        # current_cmap.set_under('')
    
                        ax1.axis('off')
                        # plt.show()
                    
                if do_plot:   
                    if annotatex:
                        # ax = plt.subplot(111)
                        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
                        props = dict(boxstyle='round', facecolor='w',edgecolor='grey')
                        plt.text(1.02, 0., 'J.Box, GEUS', transform=ax.transAxes, fontsize=9,
                                verticalalignment='top', bbox=props)
                        props = dict(boxstyle='round', facecolor='w',edgecolor='grey')
                        plt.text(1.02, 0.04, devname[ALB_dev_index], transform=ax.transAxes, fontsize=9,
                                verticalalignment='top', bbox=props) 
                    if ly=='p':
                        figname='/Users/jason/Dropbox/ELA/Figs/TSL/'+region_type+'/'+df.name[k]+'_'+TSL_or_AAR+'_v'+versionx+'_'+devname[ALB_dev_index]+'.png'
                        figname_eps='/Users/jason/Dropbox/ELA/Figs/TSL/'+region_type+'/'+df.name[k]+'_'+TSL_or_AAR+'_v'+versionx+'_'+devname[ALB_dev_index]+'.eps'
                        plt.savefig(figname, bbox_inches='tight',dpi=250)#
                        plt.savefig(figname_eps, bbox_inches='tight')
                    if ((ly == 'p') &  (open_plot==1)):os.system('open '+figname)
                    if ly == 'x': plt.show()
                    if do_break:
                        print(k,"break")
                        break    
                if wo:
                    out_annual_max_tsl.close()
                    
        #    os.system('/bin/cp '+ofile+' /Users/jason/Dropbox/ELA/stats/TSL/'+sector+'_ELA_v20191127.csv')
#                os.system('cat '+ofile) 
                    df_ELA = pd.read_csv(ofile, delimiter=",")
                # os.system('ls -lF '+fn)
#                out_concept.write('year,AAR,ELA,ELA_doy\n')

                    ofilex='/Users/jason/Dropbox/ELA/stats/ELA/'+str(df.name[k])+'_ELA_v'+versionx+'_'+devname[ALB_dev_index]+'_mean.csv'
                    out_concept=open(ofilex,'w+')
                    out_concept.write('mean ELA,stdev ELA,mean doy,stdev doy,mean lat,mean lon,std lat,std lon\n')
    
    
                    year = df_ELA["year"]
                    ela = df_ELA["ELA"]
                    ELA_doy = df_ELA["ELA_doy"]
                    lat = df_ELA["lat"]
                    lon = df_ELA["lon"]
                    prt=0
                    x0=0 ; x1=19
                    if prt:print("mean ELA",np.mean(ela[x0:x1]))
                    if prt:print("stdev ELA",np.std(ela[x0:x1]))
                    lo=np.mean(ela[x0:x1])-np.std(ela[x0:x1])
                    if prt:print("mean ELA - 1 std",lo)
                    hi=np.mean(ela[x0:x1])+np.std(ela[x0:x1])
                    if prt:print("mean ELA + 1 std",hi)
                    if prt:print("range std ELA",hi-lo)
                    lo=np.min(ela[x0:x1])
                    if prt:print("min ELA",lo)
                    hi=np.max(ela[x0:x1])
                    if prt:print("max ELA",hi)
                    if prt:print("range ELA",hi-lo)
    
                    out_concept.write(str("%8.1f"%np.mean(ela[x0:x1])).lstrip()+\
                                          ','+str("%8.1f"%np.std(ela[x0:x1])).lstrip()+\
                                                  ','+str("%6.0f"%np.mean(ELA_doy[x0:x1])).lstrip()+\
                                                  ','+str("%6.0f"%np.std(ELA_doy[x0:x1])).lstrip()+\
                                                  ','+str("%9.4f"%np.mean(lat[x0:x1])).lstrip()+\
                                                          ','+str("%9.4f"%np.mean(lon[x0:x1])).lstrip()+\
                                                  ','+str("%9.4f"%np.std(lat[x0:x1])).lstrip()+\
                                                          ','+str("%9.4f"%np.std(lon[x0:x1])).lstrip() )
                    if wo_all_catchments_table:
                        out_concept_all.write(str(df.name[k])+\
                                          ','+str(sector)+\
                                          ','+str(df.gl_type[k])+\
                                          ','+str(df.region[k])+\
                                          ','+str("%8.1f"%np.mean(ela[x0:x1])).lstrip()+\
                                          ','+str("%8.1f"%np.std(ela[x0:x1])).lstrip()+\
                                                  ','+str("%6.0f"%np.mean(ELA_doy[x0:x1])).lstrip()+\
                                                  ','+str("%6.0f"%np.std(ELA_doy[x0:x1])).lstrip()+\
                                                  ','+str("%9.4f"%np.mean(lat[x0:x1])).lstrip()+\
                                                          ','+str("%9.4f"%np.mean(lon[x0:x1])).lstrip()+\
                                                  ','+str("%9.4f"%np.std(lat[x0:x1])).lstrip()+\
                                                          ','+str("%9.4f"%np.std(lon[x0:x1])).lstrip()+\
                                                          '\n' )
                    out_concept.close()


                # os.system('cat '+ofile) 
                # os.system('ls -lF '+ofile) 
    if wo_all_catchments_table: out_concept_all.close()
