# -*- coding: utf-8 -*-
"""
@author: Adrien Wehrlé, GEUS (Geological Survey of Denmark and Greenland)
"""

import matplotlib.pyplot as plt
from osgeo import gdal, gdalconst
import rasterio
from collections import Counter
import numpy as np
import geopandas as gpd
import pandas as pd

# -------------------------------------------------- read in regions info etc
fn='/Users/jason/Dropbox/1km_grid2/sector_info_v3.csv'
df = pd.read_csv(fn)
n=len(df.name)

region_type='IC'
sectors=np.zeros((26522,14776))
region_type='IS'
sectors=np.zeros((26530,14790))
sectors=sectors.astype('float32')

# -----------------------------------------------------------------------------  loop over catchments
#cc=1
#
#from glob import glob
#catchments_path='/Users/jason/0_dat/catchments/'
#dirs = sorted(glob(catchments_path+'*.tif'))
#for f in dirs[1:]:

for k in range(0,n):
#for k in range(0,2):
#for k in range(0,n_basins):
#for kk in range(0,n_basins):
#    k=s[kk]
#    print(BASINS.NAME[k])
#    gic_area=df_wgs84.iloc[k].geometry.area/1E6
#    if ((BASINS.NAME[k][0:3]!='ICE') & (gic_area>30)):
#        print(BASINS.NAME[k],df.name[k],gic_area,sectorx[k])
#        du=1
#        if du:
#    match_filename = catchments_path+BASINS.NAME[k]+'.tif'
#    match_filename = f
    match_filename='/Users/jason/0_dat/catchments/'+df.name[k]+'.tif'
    print(k, match_filename)
    if df.name[k][0:3]!='IC_':
        src_filename = '/Users/jason/Dropbox/1km_grid2/sectors_1km.tif'
        dst_filename = '/tmp/'+region_type
        
    #    tifname=f.split('/')[-1]
    #    sector_name=tifname.split('.')[0]
    #    v=np.where(df.name==sector_name)
    #    print(sector_name,df.id[v[0]])
    
        du=1
        if du:    
            #source
            src = gdal.Open(src_filename, gdalconst.GA_ReadOnly)
            src_proj = src.GetProjection()
            src_geotrans = src.GetGeoTransform()
            
            #raster to match
            match_ds = gdal.Open(match_filename, gdalconst.GA_ReadOnly)
            match_proj = match_ds.GetProjection()
            match_geotrans = match_ds.GetGeoTransform()
            wide = match_ds.RasterXSize
            high = match_ds.RasterYSize
            
            #output/destination
            dst = gdal.GetDriverByName('Gtiff').Create(dst_filename, wide, high, 1, gdalconst.GDT_Float32)
            dst.SetGeoTransform( match_geotrans )
            dst.SetProjection( match_proj)
            
            #run
            gdal.ReprojectImage(src, dst, src_proj, match_proj, gdalconst.GRA_NearestNeighbour)
            del dst # Flush
            
            gic=rasterio.open(match_filename)
            profile=gic.profile
            gic_data=gic.read(1)
            sectors_data=rasterio.open(dst_filename).read(1)
            v=(gic_data>0)
    #        sectors_data[v]=cc
            sectors[v]=k+1
        
        wo=1
        if wo:
            ofile='/Users/jason/0_dat/sectors_'+region_type+'_1km_'+"{:03d}".format(k+1)+'.tif'
            with rasterio.open(ofile, 'w', **profile) as dst:
    #            dst.write(sectors_data, 1)
                dst.write(sectors, 1)


#    plt.imshow(sectors_data)