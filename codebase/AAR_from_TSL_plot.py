#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Jason Box, GEUS, jeb@geus.dk

produces Fig. S1, Examples of daily accumulation area ratio (AAR) and minimum AAR (stars) for Greenland ice sheet sectors. 

"""
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import locale
locale.setlocale(locale.LC_ALL, '')  # Use '' for auto, or force e.g. to 'en_US.UTF-8'

ly='x'
do_plot=1
open_plot=0
do_means=1
annotatex=0
wo_all_catchments_table=0
wo=0

versionx='20200320'
versionx='20200121'

TSL_or_AAR='TSL'
TSL_or_AAR='AAR' 

region_type='polygons'
#region_type='PROMICE'
th=2

fs=30
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
plt.rcParams['grid.color'] = "#cccccc"
plt.rcParams['grid.linewidth'] = 1
plt.rcParams["legend.facecolor"] ='w'
plt.rcParams["mathtext.default"]='regular'
plt.rcParams['figure.figsize'] = 12, 12.3

if region_type=='PROMICE':
    sectorx=['QAS','NUK','KAN','UPE','THU','KPC','SCO','TAS']
    name2=sectorx

if region_type=='polygons':
    fn='/Users/jason/Dropbox/1km_grid2/sector_names_sorted_headered.csv'
    df = pd.read_csv(fn, delimiter=",")
    os.system('ls -lF '+fn) 
    sectorx = df["name"]
    
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
    

# name=sectorx

n_sectors=len(sectorx)

i=0

#https://matplotlib.org/3.1.0/gallery/color/named_colors.html
co=['m','c','g','m','r','b','tab:orange','limegreen','blueviolet','purple',
    'k','pink','maroon','m','c','g','tab:orange','limegreen','b','tab:orange','m']
syms=['+','+','+','+','+','+','+','+','+','+',
      '*','+','.','+','+','+','2','1','4','3']

syms=['.','.','.','.','.','.','.','.','.','.',
      '.','.','.','.','.','.','.','.','.','.']

iyear=2000
fyear=2019

#v=np.where(name=="UPERNAVIK_ISSTROM_SS")
#print("v",v)

devname=["lo","mid","hi"]

#for dev_index in range(0,3):
for dev_index in range(1,2):

    if wo_all_catchments_table:
                ofile_all='/Users/jason/Dropbox/ELA/stats/ELA/ELA_average_all_catchments_v'+versionx+'_'+devname[dev_index]+'.csv'
                out_concept_all=open(ofile_all,'w+')
                out_concept_all.write('catchment name,sector id,gl_type,region,mean ELA meters,stdev ELA meters,mean day of year,stdev day of year,mean lat,mean lon,std lat,std lon\n')

    for i in range(0,n_sectors):
    #for i in range(n_sectors-1,n_sectors):
    #for i in range(100,200):
    #for i in range(39,260):
    # for i in range(0,1):
    
    #    print("i",i,name[i],name2[i])
        
#        if name2[i]=='SERMILIK':
        if region[i]!='SWx':
            counts=[0.]*366
            sums=[0.]*366
            means=[np.nan]*366
            doys=[0.]*366
            
            # if name[i]!='ICE_CAPS_NWx':
            # if name[i]=='JAKOBSHAVN_ISBRAE':
            #     cutoff2018=275
            # if name[i]=='NIOGHALVFJERDSFJORDEN':
            #     cutoff2018=245
            # if name[i]=='HELHEIMGLETSCHER':
            #     cutoff2018=275
            if name[i]=='SAQQAP-MAJORQAQ-SOUTHTERRUSSEL_SOUTHQUARUSSEL':
                cutoff2018=275
                if region_type=='polygons': sector=str(sectorx[i]).zfill(3)
                if region_type=='PROMICE': sector=sectorx[i]
            
                if wo:
                    ofile='/Users/jason/Dropbox/ELA/stats/TSL/'+name[i]+'_ELA_v'+versionx+'_'+devname[dev_index]+'.csv'
                    out_concept=open(ofile,'w+')
                    out_concept.write('year,AAR,ELA,ELA_doy,lat,lon\n')
            
                if do_plot:plt.close()
                
                for yy in range(iyear,fyear+1):
            
                    if ((yy != 20000)):
    #                if ((yy == 2012)):
            #            fn='/Users/jason/Dropbox/ELA/stats/TSL/regional/'+region_type+'/'+sector+'_'+str(yy)+'_ELAs_MOD10A1_1000m_mean_vfit.csv'
                        fn='/Users/jason/Dropbox/ELA/stats/TSL/regional/'+region_type+'/'+sector+'_'+str(yy)+'_ELAs_MOD10A1_1000m_mean_v'+versionx+'.csv'
    #                    os.system('ls -lF '+fn) 
#                        os.system('head '+fn) 
    #                    os.system('cat '+fn) 
    #                    os.system('open '+fn) 
                        df = pd.read_csv(fn, delimiter=",")
                
            #year,day,snowline_selection,snowline_selection2,aar,aar2,meanalb_abl,meanalb_accum,meanalb_all,minalb_abl,minalb_all,area,lat or ELA,lon of ELA
                        
                        year = df["year"]
                        doyx = df["day"] ; doy=doyx.values
                        TSLx = df["snowline_selection_"+devname[dev_index]] ; TSL=TSLx.values
                        aarxx = df["aar_"+devname[dev_index]] ; AAR=aarxx.values
                        tsl_lat = df["tsl_lat"] ; tsl_lat=tsl_lat.values
                        tsl_lon = df["tsl_lon"] ; tsl_lon=tsl_lon.values
    
                        y=TSL
                        if TSL_or_AAR=='AAR':y=AAR
                        x=doy
                        
                        for ii in range(1,len(x)):
                            if AAR[ii] < 0 and TSL[ii]>0.1:
    #                            print('before',doy[ii],AAR[ii],AAR[ii-1])
                                AAR[ii]=AAR[ii-1]
    #                            print('after',doy[ii],AAR[ii],AAR[ii-1])
                        
                        
                        ELA=0.
                        ELA_day=0.
                        AAR_min=0.
                        
                        if do_means:
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
        
                        plotvar=TSL
                        ytit='meters above sea level'
                
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
                        lonx=0.
                        latx=0.                      
                        if c2 == 0:print(name2[i],area[i])
                        if c2 > 0:
                            v=np.where(TSL == np.max(TSL))
                            c=len(v[0])
                            
                           
                            if c==1:
                                ELA=np.max(TSL)
                                ELA_day=doy[v[0]]
                                AAR_min=AAR[v[0]]
                                latx=tsl_lat[v[0]]
                                lonx=tsl_lon[v[0]]

            #                    print(yy,c)
                
                            if c > 1:
                                ELA=np.mean(TSL[v[0]])
                                ELA_day=np.mean(doy[v[0]])
                                AAR_min=np.mean(AAR[v[0]])
                                latx=np.mean(tsl_lat[v[0]])
                                lonx=np.mean(tsl_lon[v[0]] )
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
                            out_concept.write(\
                                          str(year[yy-2000])+\
                                          ','+str("%8.5f"%AAR_min).lstrip()+\
                                          ','+str("%8.1f"%ELA).lstrip()+\
                                          ','+str("%6.0f"%ELA_day).lstrip()+\
                                          ','+str("%9.4f"%latx).lstrip()+\
                                          ','+str("%9.4f"%lonx).lstrip()+\
                                          '\n')
                        if do_plot:
                            # if ((yy == 2012) or (yy == 2005) or (yy == 2010) or (yy == 2015)):
                            # if ((yy == 2012) or (yy == 2018) or (yy == 2010)):
                            if ((yy == 2012) or (yy == 2018) or (yy == 2002)):
#                            if ((yy == 2016) or (yy == 2011) or (yy == 2019) or (yy == 2014)):
#                            if ((yy == 2010) or (yy == 2012)):
#                            if ((yy == 2005) or (yy == 2015) or (yy == 2000)):
#                            if ((yy == 2012) or (yy == 2005) or (yy == 2010)):
#                            if ((yy < 20019)):
                
                                cs=10
                                if yy==2018:
                                    v=doy>=cutoff2018
                                    plotvar[v]=np.nan
                                plt.plot(doy, plotvar, linewidth=th*2,#marker='.',#syms[yy-iyear]
                                         color=co[yy-iyear],
        #                                 markersize=10,fillstyle='none',
                                         label=str(yy))
                                        
                                if TSL_or_AAR=='TSL':
                                    plt.plot(ELA_day, ELA,marker='s',color=co[yy-iyear],markersize=13)#,label='ELA')#,fillstyle='none'
                                if TSL_or_AAR=='AAR':
                                    plt.plot(ELA_day, AAR_min,marker='*',color=co[yy-iyear],markersize=40)#,label='ELA')#,fillstyle='none'
                                
                                plt.xlabel('day of year')
                                plt.ylabel(ytit)
                                if region_type=='PROMICE':
                                    tit=sectorx[i]+' transient snowline and equilibrium line altitude'
                                if region_type=='polygons':
                                    # f'{area[i]:n}'
                                    # tit=name[i]+'\n'+str(gl_type[i])+' sector '+sector+', lat: '+"%.1f"%lat[i])+' N, lon: '+str("%.1f"%lon[i])+', '+str("%.0f"%area[i])+' $km^2$'
                                    fancy_title=name[i].replace("_", " ").title()
                                    fancy_title=fancy_title.replace("strom","strøm")
                                    fancy_title=fancy_title.replace("ae","æ")
                                    fancy_area=f"{area[i]:,.0f}"
                                    plt.title(fancy_title+'\n'+gl_type[i]+' sector, '+"%4.1f"%lat[i]+' N, '+str("%5.1f"%abs(lon[i]))+' W, '+fancy_area+' $km^2$', fontsize=fs*0.95)
                                    # plt.title(str(name[i].title()+'\n'+sector+', lat: '+"%4.1f"%lat[i])+' N, lon: '+str("%5.1f"%lon[i])+', '+f'{area[i]:n}'+' $km^2$')
                                plt.xlim(145,295)
                
                if do_means:
                    for ii in range(0,366):
                        doys[ii]=ii+1
                        if counts[ii]>5:means[ii]=sums[ii]/counts[ii]
    
                    if do_plot:
                        plt.plot(doys,means,marker='.',color='#666666',
            #                 markersize=10,fillstyle='none',
                        linewidth=th*2,label='mean')        
                        
                        v=np.where(means==np.nanmin(means))
                        plt.plot(doys[v[0][0]], means[v[0][0]],marker='*',color='#666666',markersize=40)#,label='ELA')#,fillstyle='none'

        
                plt.legend()
        
                if do_plot:
                    ax = plt.subplot(111)
                    # ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
                    # ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    
                    if annotatex:
                        props = dict(boxstyle='round', facecolor='w',edgecolor='grey')
                        plt.text(1.02, 0., 'J.Box, GEUS', transform=ax.transAxes, fontsize=9,
                                verticalalignment='top', bbox=props)
                        props = dict(boxstyle='round', facecolor='w',edgecolor='grey')
                        plt.text(1.02, 0.04, devname[dev_index], transform=ax.transAxes, fontsize=9,
                                verticalalignment='top', bbox=props)        
                    #    plt.savefig('/Users/jason/Dropbox/ELA/Figs/TSL/'+sector+'_'+TSL_or_AAR+'.png', bbox_inches='tight',dpi=250)
                    if ly=='p':
                        figname='/Users/jason/Dropbox/ELA/Figs/TSL/'+region_type+'/'+name2[i]+'_'+TSL_or_AAR+'_v'+versionx+'_'+devname[dev_index]+'.png'
                        plt.savefig(figname, bbox_inches='tight',dpi=250)
                    if ((ly == 'p') &  (open_plot==1)):os.system('open '+figname)
                    if ly == 'x': plt.show()

                    if wo:
                        out_concept.close()
                    
        #    os.system('/bin/cp '+ofile+' /Users/jason/Dropbox/ELA/stats/TSL/'+sector+'_ELA_v20191127.csv')
#                os.system('cat '+ofile) 
                        df = pd.read_csv(ofile, delimiter=",")
#                os.system('ls -lF '+fn)
#                out_concept.write('year,AAR,ELA,ELA_doy\n')

                if wo:
                    ofile='/Users/jason/Dropbox/ELA/stats/ELA/'+name2[i]+'_ELA_v'+versionx+'_'+devname[dev_index]+'_mean.csv'
                    out_concept=open(ofile,'w+')
                    out_concept.write('mean ELA,stdev ELA,mean doy,stdev doy,mean lat,mean lon,std lat,std lon\n')


                    year = df["year"]
                    ela = df["ELA"]
                    ELA_doy = df["ELA_doy"]
                    lat = df["lat"]
                    lon = df["lon"]
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
                    out_concept_all.write(name2[i]+\
                                          ','+sector+\
                                          ','+gl_type[i]+\
                                          ','+region[i]+\
                                          ','+str("%8.1f"%np.mean(ela[x0:x1])).lstrip()+\
                                          ','+str("%8.1f"%np.std(ela[x0:x1])).lstrip()+\
                                                  ','+str("%6.0f"%np.mean(ELA_doy[x0:x1])).lstrip()+\
                                                  ','+str("%6.0f"%np.std(ELA_doy[x0:x1])).lstrip()+\
                                                  ','+str("%9.4f"%np.mean(lat[x0:x1])).lstrip()+\
                                                          ','+str("%9.4f"%np.mean(lon[x0:x1])).lstrip()+\
                                                  ','+str("%9.4f"%np.std(lat[x0:x1])).lstrip()+\
                                                          ','+str("%9.4f"%np.std(lon[x0:x1])).lstrip()+'\n' )
                    out_concept.close()

                    os.system('cat '+ofile) 
                    os.system('ls -lF '+ofile) 
    if wo:out_concept_all.close()
