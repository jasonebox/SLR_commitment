#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 08:08:56 2020

@author: jeb
"""
import matplotlib.pyplot as plt
from netCDF4 import Dataset
import os
import numpy as np
#import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import geopandas as gpd
import locale
locale.setlocale(locale.LC_ALL, '')  # Use '' for auto, or force e.g. to 'en_US.UTF-8'
from shapely.geometry import Point, Polygon

#from scipy.io import netcdf 

ni=2700 ; nj=1496

inpath='/Volumes/2Tb/MAR3.10/'
#inpath='/Users/jason/0_dat/MAR3.10/'

fn=inpath+'MARv3.10-daily-ERA5-1999.nc'
fh = Dataset(fn, mode='r')

#print(fh.variables)

msk = fh.variables['MSK'][:]
#    elev = fh.variables['Topography'][:]
lon = fh.variables['LON'][:]
lat = fh.variables['LAT'][:]

#msk[msk==1]=3
#
#plt.imshow(msk,cmap='jet')
#plt.gca().invert_yaxis()


ni=len(lat) ; nj=len(lat[1,:])

print(ni,nj)


du=0

if du:    
#    print(np.min(lat),np.min(lon))
#    print(np.max(lat),np.max(lon))
#        print(fh.variables)

    plt.imshow(msk, cmap = 'jet')
    
    wo_latlon=1
    
    if wo_latlon:
        out_lat=open('/Users/jason/Dropbox/MAR/ancil/lat.csv','w')
        out_lon=open('/Users/jason/Dropbox/MAR/ancil/lon.csv','w')
        
        cc=0
        
        for i in range(0,ni):
            print(ni-i)
            for j in range(0,nj):
#                if ((msk[i,j]>0)&(lon[i,j]<0)):
                if msk[i,j]>1:
                    out_lat.write(str("%8.5f"%lat[i,j]).lstrip()+'\n')
                    out_lon.write(str("%8.5f"%lon[i,j]).lstrip()+'\n')
                    cc+=1
                    
        print(cc)
        
        out_lat.close()
        out_lon.close()
        
        os.system('head '+'/Users/jason/Dropbox/MAR/ancil/lon.csv')
    
    fh.close()
    
    
    
du=1


#/Users/jason/0_dat/MAR3.10/MARv3.10-daily-ERA5-2001.nc
if du:
    
    iyear=1999 ; fyear=2019
    n_years=fyear-iyear+1.
    
    #for yy in range(0,n_years):
    for yy in range(2017,2020):
#        for yy in range(2000,2020):
        fn=inpath+'MARv3.10-daily-ERA5-'+str(yy)+'.nc'

        fh = Dataset(fn, mode='r')
                    
        smb = fh.variables['SMBcorr'][:]

        n_days=len(smb[:,0,0])

        print(n_days,fn)

        opath='/Users/jason/0_dat/MAR3.10/txt/'+str(yy)+'/'
#        opath='/Volumes/2Tb/MAR/txt/'+str(yy)+'/'
        os.system('mkdir -p '+opath)
        
        for dd in range(0,n_days):
            ofile=opath+str(yy)+'_'+"{:03d}".format(dd+1)+'.txt'
            print(ofile)

            out=open(ofile,'w')
            
            for i in range(0,ni):
#                print('writing smb',ni-i)
                for j in range(0,nj):
                    if msk[i,j]>1:
                        out.write(str("%8.5f"%smb[dd,i,j]).lstrip()+'\n')
            out.close()            
#            os.system('head '+ofile)
#            os.system('/bin/cp '+ofile+' '+opath+str(yy)+'_'+"{:03d}".format(dd+1)+'.txt')
