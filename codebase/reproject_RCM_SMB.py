# -*- coding: utf-8 -*-
"""
@author: Adrien Wehrlé, GEUS (Geological Survey of Denmark and Greenland)
"""

from osgeo import gdal, gdalconst
import rasterio
import time
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import calendar

def loadtiff(filename):
    dataset = gdal.Open(filename,0)
    ncol = dataset.RasterXSize # x = columns
    nrow = dataset.RasterYSize 
    rasterBand = dataset.GetRasterBand(1)
    GD = rasterBand.ReadAsArray(0,0,ncol,nrow)
    return GD

RCM="MAR3.10"; RCM2='MAR' ;prepath='/Users/jason/0_dat/'

RCM="RACMO2.3p2" ; RCM2='RACMO' ; prepath='/Volumes/2Tb/'


# ------------------------------------------------------------------

fn = '/Users/jason/Dropbox/1km_grid2/sectors_IS_1km_1485x2684.tif'
IS=loadtiff(fn)
fn = '/Users/jason/Dropbox/1km_grid2/sectors_IC_1km_1485x2684.tif'
IC=loadtiff(fn)

sectors=IS
v=(IS<1)
sectors[v]=IC[v]
plt.imshow(sectors,cmap='jet')

n_sectors=473
wo=0

# ------------------------------------------------------------------

year='2000'
day_string='001'

iyear=1999 ; fyear=2019
n_years=fyear-iyear+1.

smb_all=np.zeros((n_sectors,7670))

cc=0

# ------------------------------------------------------------------ loop over years
# for yy in range(2017,2020):
# for yy in range(2012,2013):
for yy in range(1999,2001):
# for yy in range(1999,2020):
    os.system('mkdir -p '+'/Users/jason/0_dat/'+RCM+'/tif_reprojected/'+str(yy))
    print(yy)
    n_days=365
    if calendar.isleap(yy):n_days=366
    smb=np.zeros((n_sectors,n_days))

    for dd in range(1,n_days+1):
    # for dd in range(1,2):
    # for dd in range(210,211):
        day_string="{:03d}".format(dd)

        # ------------------------------------------------------------------ reproject RCM SMB       
        src_fn = prepath+RCM+'/tif/'+str(yy)+'/'+str(yy)+'_'+day_string+'.tif'
        target_crs_fn='/Users/jason/0_dat/Greenland_L3_1km_1485_2685/2001/2001_300.tif'
        ofile = '/Users/jason/0_dat/'+RCM+'/tif_reprojected/'+str(yy)+'/'+str(yy)+'_'+day_string+'.tif'
        # ofile = '/tmp.tif'
        print(day_string,src_fn)
        start_time = time.time()
        # print("start")
        #source
        src = gdal.Open(src_fn, gdalconst.GA_ReadOnly)
        src_proj = src.GetProjection()
        src_geotrans = src.GetGeoTransform()
        
        #raster to match
        match_ds = gdal.Open(target_crs_fn, gdalconst.GA_ReadOnly)
        match_proj = match_ds.GetProjection()
        match_geotrans = match_ds.GetGeoTransform()
        wide = match_ds.RasterXSize
        high = match_ds.RasterYSize
        
        #output/destination
        dst = gdal.GetDriverByName('Gtiff').Create(ofile, wide, high, 1, gdalconst.GDT_Float32)
        dst.SetGeoTransform( match_geotrans )
        dst.SetProjection( match_proj)
        
        # print("run")
        #run
        gdal.ReprojectImage(src, dst, src_proj, match_proj, gdalconst.GRA_NearestNeighbour) #.GRA_Bilinear
        del dst # Flush
        
        #print("final")
        islands=rasterio.open(target_crs_fn)
        profile=islands.profile
        islands_data=islands.read(1)
        #islands_data+=260
        #sectors_data=rasterio.open(ofile).read(1)
        #v=(islands_data!=260)
        #sectors_data[v]=islands_data[v]
        
        wo=0
        if wo:
            with rasterio.open(ofile, 'w', **profile) as dst:
                dst.write(dst, 1)
        # print("done")
            
        # ------------------------------------------------------------------ obtain SMB on sectors
        a=loadtiff(ofile)
        # plt.imshow(a,cmap='jet')
        # os.system('ls -lF '+ofile)

        # for k in range(0,n_sectors):
        for k in range(0,1):
            b=a
            v=np.where(sectors==k+1)
            # print(k,len(v[0]))
            sumx=np.sum(a[v])
            smb[k,dd-1]=sumx
            # smb_all[k,cc]=sumx
            # print(yy,day_string,k,cc,dd,sumx)
            # b[v]=-30
            # plt.imshow(b,cmap='jet')
            # plt.axis('off')
            # plt.show()
            # time.sleep(1)
        
        cc+=1
        # os.system('/bin/rm '+ofile)

        end_time = time.time()
        dt=end_time - start_time
        # print("time: "+str("%8.1f"%dt).lstrip()+'s')

    if wo:
        # df.iloc[2,:]=a[0]
        # df = pd.DataFrame(smb)
        ofn='/Users/jason/Dropbox/'+RCM2+'/output/csv/'+str(yy)+'.csv'
        # df.to_csv(ofn, header=False, index=False,sep=',',float_format='%15.5f')
    
        np.savetxt(ofn, smb, fmt='%.10e', delimiter=',', newline='\n')
        # df.to_csv(ofn)

# if wo:
#     ofn='/Users/jason/Dropbox/'+RCM2+'/output/csv/all.csv'
#     np.savetxt(ofn, smb_all, fmt='%.10e', delimiter=',', newline='\n')

