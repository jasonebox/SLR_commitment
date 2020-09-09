#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 08:08:56 2020

@author: Jason Box, GEUS, jeb@geus.dk

Output monthly ERA5 temperatures for regional polygons drawn unambiguously in photoshop with ocean buffer but obtaining land using ERA5 mask data

"""
wo=1
du=1

ppt=0
outname='t2m'
varnam='T2m'

if ppt:
    varnam='mtpr'
    varnam='msr'
#import matplotlib.pyplot as plt
from netCDF4 import Dataset
# import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import misc

fn='/Users/jason/0_dat/ERA5/mask_and_terrain.nc'
fh = Dataset(fn, mode='r')
print(fh.variables)

ni=1440 ; nj=721

lon=np.zeros((nj,ni))#[[ni,nj]]
lat=np.zeros((nj,ni))

for i in range(0,ni):
    temp=fh.variables['latitude'][:]
    temp=np.ma.filled(temp, np.nan)
    lat[:,i] = temp[:]
    
for j in range(0,nj):
    # print(j)
    temp=fh.variables['longitude'][:]
    # print(temp)
    temp=np.ma.filled(temp, np.nan)
    lon[j,:] = temp[:]

lon-=360

print(np.min(lon),np.max(lon))

a = fh.variables['z'][0,:,:]
msk = fh.variables['lsm'][0,:,:]

# G=np.where((lat>60)&(lat<84)&(lon>-60)&(lon<-20)&(msk>0))
# AO=np.where((lat>67)&(msk==0))
# v=np.where((lat>60)&(lat<80))
# v=G
# msk[v]=1.1
# print(v)

# a = fh.variables['t2m'][0,0,:,:]
# lat = fh.variables['lat'][0,0,:,:]

# plt.imshow(msk, cmap = 'jet')
# plt.axis('off')

if du:
    if wo:
        ofile='/Users/jason/Dropbox/ERA5/stats/ERA5_'+varnam+'_monthly.csv'
        out_concept=open(ofile,'w+')
        header='year,month,Greenland,Alaska,Canada,Scandinavia,Svalbard,Iceland,Russian Arctic,Arctic Land,North America,Eurasia,Northern Hemisphere,Arctic Ocean,Arctic,Finland,Global\n'
        out_concept.write(header)
        
    fn='/Users/jason/0_dat/ERA5/T2m_ERA5.nc'
    kk=273.15

    if ppt:
        fn='/Users/jason/0_dat/ERA5/PPT_ERA5_monthly_1979-2020.nc'
        fn='/Users/jason/0_dat/ERA5/PPT_msr_mtpr_ERA5_monthly_1979-2020.nc'
        kk=0.
    fh = Dataset(fn, mode='r')
    
    print()
    print(fn)
    print(fh.variables)
    
    if ppt==0:
        era5_var=fh.variables['t2m'][:,0,:,:]-kk
    # if ppt:era5_var=fh.variables['tp'][0:12,0,:,:]
    if ppt:
        # era5_var=fh.variables[varnam][0:12,0,:,:]
        era5_var=fh.variables[varnam][:,0,:,:]
    # plt.plot(era5_var[:,103,1267]*1000*86400*30.5)
    # t2m=np.ma.filled(temp, np.nan)
   # plt.imshow(fh.variables['tp'][7,0,:,:])
    iyear=1979 ; fyear=2019
    n_years=fyear-iyear+1
    
    cc=0
    for yy in range(0,n_years):
    # for yy in range(0,1):
        ann=np.zeros((nj,ni))
        temp1=0.
        for ss in range(0,12):

            var=era5_var[cc,:,:]
            ann+=var
            # v=np.where((lat>=70)&(lat<=72)&(lon<-37)&(lon>=-40))
            # print(ss,ann[v])
            cc+=1
            # plt.imshow(var, cmap = 'jet')
            # plt.axis('off')
            if cc==11:
                plt.imshow(ann, cmap = 'jet') ; plt.axis('off')
            regions=['G','AK',       'NAm',   'Sc','Sv','Il','RHA','NAm',   'NAm','Eu','NAm','AO','NAm','NAm','NAm']
            regions_actual=['G','AK','Canada','Sc','Sv','Il','RHA','ArcLand','NAm','Eu','NHem','AO','Arctic','Finland','Global']
            results=np.zeros(len(regions))

            # for i,region in enumerate(regions[0:1]):
            # for i,region in enumerate(regions[-1:]):
            for i,region in enumerate(regions):
                fn='/Users/jason/Dropbox/ERA5/ancil/'+region+'.png'
                msk2 = misc.imread(fn) ; msk2[msk2==0]=1 ; msk2[msk2==255]=0
                
                v=np.where((msk2==1)&(msk>0))
                tmp=np.zeros((nj,ni)) ; tmp[v]=1

                if regions_actual[i]=='Global':
                    msk2[:,:]=1
                    v=np.where((msk2==1))
                    tmp=np.zeros((nj,ni)) ; tmp[v]=1
                    # plt.imshow(tmp, cmap = 'jet') ; plt.axis('off')                
                
                if regions_actual[i]=='Canada':
                    fn='/Users/jason/Dropbox/ERA5/ancil/AK.png'
                    v2 = misc.imread(fn) ; v2[v2==0]=1 ; v2[v2==255]=0
                    msk2[v2==1]=0
                    v=np.where((msk2==1)&(msk>0))

                    # results[i]=np.mean(var[v])
                    tmp=np.zeros((nj,ni)) ; tmp[v]=1
                    # plt.imshow(tmp, cmap = 'jet') ; plt.axis('off')

                if regions_actual[i]=='ArcLand':
                    v=np.where((lat>=60)&(msk>0))
                    # results[i]=np.mean(var[v])
                    tmp=np.zeros((nj,ni)) ; tmp[v]=1
                    # plt.imshow(tmp, cmap = 'jet') ; plt.axis('off')
                    
                if regions_actual[i]=='NHem':
                    v=np.where(lat>=0)
                    # results[i]=np.mean(var[v])
                    tmp=np.zeros((nj,ni)) ; tmp[v]=1
                    # plt.imshow(tmp, cmap = 'jet') ; plt.axis('off')

                if regions_actual[i]=='Arctic':
                    v=np.where(lat>=60)
                    # results[i]=np.mean(var[v])
                    tmp=np.zeros((nj,ni)) ; tmp[v]=1
                    # plt.imshow(tmp, cmap = 'jet') ; plt.axis('off')

                if regions_actual[i]=='AO':
                    fn='/Users/jason/Dropbox/ERA5/ancil/AO.png'
                    v2 = misc.imread(fn) ; v2[v2==0]=1 ; v2[v2==255]=0
                    tmp=np.zeros((nj,ni))
                    tmp2=np.zeros((nj,ni))
                    tmp[v2==1]=1
                    v=np.where((tmp==1)&(msk<1)&(lat>=66.6))
                    tmp2[v]=1
                    tmp[v]=1
                    # results[i]=np.mean(var[v])

                v=np.where(tmp)
                if ppt==0:results[i]=np.mean(var[v])
                if ppt==1:results[i]=np.sum(var[v])/1000*771.60*1e6*86400*30.5/1e9/4.49
                temp1+=results[i]
                # if regions_actual[i]=='G':
                    # plt.imshow(tmp, cmap = 'jet') ; plt.axis('off')
                # print(regions_actual[i],len(v[1])*771.60/1e6,results[i],temp1)#*31.**2/1e3)
                # break

            print(yy+iyear,ss)

            if wo:
                out_concept.write(\
                      str(yy+1979)+\
                      ','+str(ss+1)+\
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

