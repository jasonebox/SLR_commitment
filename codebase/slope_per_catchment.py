# -*- coding: utf-8 -*-
"""
@author: Jason Box, GEUS, jeb@geus.dk and Adrien Wehrlé, GEUS (Geological Survey of Denmark and Greenland)

Obtain average below ELA slope angles for different Greenland ice sheet regions

"""

from osgeo import gdal, gdalconst
import rasterio
import time
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# src_fn = '/Users/jason/Dropbox/1km_grid2/slope_3413.tif'
# target_crs_fn='/Users/jason/Dropbox/1km_grid2/sectors_IS_1km_1485x2684.tif'
# ofile = '/Users/jason/Dropbox/1km_grid2/slope_1km_1485_2684.tif'

# start_time = time.time()

# print("start")
# #source
# src = gdal.Open(src_fn, gdalconst.GA_ReadOnly)
# src_proj = src.GetProjection()
# src_geotrans = src.GetGeoTransform()

# #raster to match
# match_ds = gdal.Open(target_crs_fn, gdalconst.GA_ReadOnly)
# match_proj = match_ds.GetProjection()
# match_geotrans = match_ds.GetGeoTransform()
# wide = match_ds.RasterXSize
# high = match_ds.RasterYSize

# #output/destination
# dst = gdal.GetDriverByName('Gtiff').Create(ofile, wide, high, 1, gdalconst.GDT_Float32)
# dst.SetGeoTransform( match_geotrans )
# dst.SetProjection( match_proj)

# print("run")
# #run
# gdal.ReprojectImage(src, dst, src_proj, match_proj, gdalconst.GRA_NearestNeighbour) #.GRA_Bilinear
# del dst # Flush

# #print("final")
# islands=rasterio.open(target_crs_fn)
# profile=islands.profile
# islands_data=islands.read(1)
# #islands_data+=260
# #sectors_data=rasterio.open(ofile).read(1)
# #v=(islands_data!=260)
# #sectors_data[v]=islands_data[v]

# wo=0
# if wo:
#     with rasterio.open(ofile, 'w', **profile) as dst:
#         dst.write(dst, 1)

# import os
# ofile2 = '/tmp/x.tif'
# msg='gdal_translate -co COMPRESS=DEFLATE '+ofile+' '+ofile2
# print(msg)
# os.system(msg)
# os.system('/bin/mv '+ofile2+' '+ofile)
# print("done")

# end_time = time.time()

# dt=end_time - start_time
# print("time: "+str("%8.1f"%dt).lstrip()+'s')


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
print(df.columns)

fn='/Users/jason/Dropbox/1km_grid2/slope_1km_1485_2684.tif'
slope_reader=rasterio.open(fn)
slope=slope_reader.read(1)

fn='/Users/jason/Dropbox/1km_grid2/sectors_IS_1km_1485x2684.tif'
sector_reader=rasterio.open(fn)
sector=sector_reader.read(1)

fn='/Users/jason/Dropbox/1km_grid2/elev_1km_1485x2684_nn_from_500m.tif'
temp=rasterio.open(fn)
elev=temp.read(1)

inv=slope>5
slope[inv]=np.nan


mean_slopes=np.zeros(7)
regions=['SW','CW','NW','NO','NE','CE','SE'] ; n_regions=len(regions)

oksum=0.

for j,regionx in enumerate(regions):
    ok=np.zeros((2684,1485))
    # for k,idx in enumerate(df.id):
    for k,idx in enumerate(df.sector_id):
        fn='/Users/jason/Dropbox/ELA/stats/ELA/'+df.name[k]+'_ELA_v20200121_mid_mean.csv'
        if os.path.isfile(fn):
            ela=pd.read_csv(fn)
            if k<20e3:
                val=ela["mean ELA"]
                # v=((sector==df.id[k])&(elev<val[0]+1000))
                v=sector==df.id[k]
                # if df.name[k]=='SAQQAP-MAJORQAQ-SOUTHTERRUSSEL_SOUTHQUARUSSEL':
                # if df.name[k]=='DAUGAARD-JENSEN':
                # if region[k]=='SW':
                if region[k]==regionx:
                    # if df.name[k]=='JAKOBSHAVN_ISBRAE':
                # if df.name[k]=='HELHEIMGLETSCHER':
                    # slope[v]=10.
                    # print('hi',v)
                    ok[v]=1
                    oksum+=np.nansum(v)
                    # print(df.name[k],df.id[k],df.sector_id[k],np.sum(v),np.nanmean(slope[v]))
    mean_slopes[j]=np.nanmean(slope[ok>0])
    
    print(regionx,mean_slopes[j],np.nansum(ok>0),oksum)

print(mean_slopes[[r=='SE' for r in regions]])
print('SE/SE',mean_slopes[6]/mean_slopes[0])
print('E/W',np.mean(mean_slopes[4:7])/np.mean(mean_slopes[0:3]))

plt.imshow(slope)
plt.axis('off')