#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 08:08:56 2020

@author: jeb
"""
#import matplotlib.pyplot as plt
from netCDF4 import Dataset
import os
import numpy as np
import calendar
import time
from pathlib import Path
    
#from scipy.io import netcdf 

fn='/Users/jason/Dropbox/RACMO/Icemask_Topo_Iceclasses_lon_lat_average_1km_GrIS.nc'
fh = Dataset(fn, mode='r')

#print(fh.variables)

maskx = fh.variables['Promicemask'][:]
elev = fh.variables['Topography'][:]
lon = fh.variables['LON'][:]
lat = fh.variables['LAT'][:]

fh.close()

ni=len(lat) ; nj=len(lat[1,:])

print(ni,nj)
v=np.where(maskx>0)

print(np.min(lat),np.min(lon))
print(np.max(lat),np.max(lon))

#plt.imshow(lon, cmap = 'jet')

wo_latlon2=0

if wo_latlon2:
    out_lat=open('/Users/jason/Dropbox/RACMO/ancil/lat2.csv','w')
    out_lon=open('/Users/jason/Dropbox/RACMO/ancil/lon2.csv','w')
    
    cc=0
    
    c=len(v[0][:])
    
    for i in range(0,c):
#        print(i,c,c-i)
        latt=lat[v][i]
        lonn=lon[v][i]
        out_lat.write(str("%8.5f"%latt).lstrip()+'\n')
        out_lon.write(str("%8.5f"%lonn).lstrip()+'\n')
        cc+=1
                
    print(cc)
    
    out_lat.close()
    out_lat.close()
    
    os.system('head '+'/Users/jason/Dropbox/RACMO/ancil/lon.csv')


wo_latlon=0

if wo_latlon:
    out_lat=open('/Users/jason/Dropbox/RACMO/ancil/lat2.csv','w')
    out_lon=open('/Users/jason/Dropbox/RACMO/ancil/lon2.csv','w')
    
    cc=0
    
    for i in range(0,ni):
        print(ni-i)
        for j in range(0,nj):
            if ((maskx[i,j]>0)&(lon[i,j]<0)):
#            if maskx[i,j]>0:
                out_lat.write(str("%8.5f"%lat[i,j]).lstrip()+'\n')
                out_lon.write(str("%8.5f"%lon[i,j]).lstrip()+'\n')
                cc+=1
                
    print(cc)
    
    out_lat.close()
    out_lat.close()
    
    os.system('head '+'/Users/jason/Dropbox/RACMO/ancil/lon.csv')

du=1

wo=1

if du:
    season=['JFM','AMJ','JAS','OND']
    
    iyear=1999 ; fyear=2019
    n_years=fyear-iyear+1.
    
   
    #for yy in range(0,n_years):
#    for yy in range(1999,2000):
    for yy in range(2011,2012):
    # for yy in range(1999,1999+5):
    # for yy in range(1999+5,1999+10):
    # for yy in range(1999+10,1999+15):
    # for yy in range(2018,2020):
        for ss in range(3,4):
            day0=[1,91,182,274]
            print(yy,ss,calendar.isleap(yy))
            if calendar.isleap(yy):
                day0=[1,92,183,275]

            # os.system('ls /Users/jason/0_dat/RACMO2.3p2/_nc/*'+str(yy)+'_'+season[ss]+'* > /tmp/t')
            # # os.system('cat /tmp/t')
            # with open('/tmp/t', 'r') as file:fn=file.read()
            # indexes=fn.find('.nc')
            # print('fn',fn)
            # dest_file=fn[0:indexes]+'.nc'
            # print(len(fn))
            # print(fn[0:len(fn)-1])
            # print('dest_file',dest_file)
            # os.rename(fn[0:len(fn)-1],dest_file)

            # msg='/bin/cp \"'+fn+'\" '+dest_file
            # print(msg)
            # os.system(msg)
            # os.system('ls -lF '+dest_file)
            
            print(fn)
            fn='/Users/jason/0_dat/RACMO2.3p2/_nc/smb_rec_WJB_int.'+str(yy)+'_'+season[ss]+'.BN_RACMO2.3p2_FGRN055_1km.DD.nc'
            # fn=dest_file
            fh2 = Dataset(fn, mode='r')
            
            # print(fh2.variables)
            
            smb = fh2.variables['SMB_rec'][:]

            fh2.close()
    #        
            opath='/Volumes/2Tb/RACMO2.3p2/txt/'+str(yy)+'/'
            os.system('mkdir -p '+opath)
            
            n=len(smb[:,0,0])
            print("n days",n,len(smb[1,:]),len(smb[1,1,:]))

            for dd in range(0,n):
                start_time = time.time()
                ofile=opath+str(yy)+'_'+"{:03d}".format(dd+day0[ss])+'.txt'
                print(ofile)
    
                if wo:
                    my_file = Path(ofile)
                    if my_file.is_file()==False:
                        out=open(ofile,'w')
                        for i in range(0,ni):
            #                print('writing smb',ni-i)
                            for j in range(0,nj):
                                if maskx[i,j]>0:
                                    out.write(str("%8.5f"%smb[dd,i,j]).lstrip()+'\n')
                        out.close()
                    end_time = time.time();dt=end_time - start_time;print("time: "+str("%8.1f"%dt).lstrip()+'s')


