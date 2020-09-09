#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 08:08:56 2020

@author: Jason Box, GEUS, jeb@geus.dk

creates a per sector dataframe containing name, area, volume, glacier type (ice sheet IS or ice cap IC), merging Mouginot ice sheet sectors with individual peripheral ice caps and glaciers, integrates volume to confirm it adds up to expected value

output /Users/jason/Dropbox/1km_grid2/sector_info_ice_caps_v3.csv

"""
import os
import locale
locale.setlocale(locale.LC_ALL, '')  # Use '' for auto, or force e.g. to 'en_US.UTF-8'
import geopandas as gpd
import numpy as np
import pandas as pd
import gdal
import matplotlib.pyplot as plt
# -----------------------------------------------------------------------------  paths
#shapefile_path='/Users/jason/0_dat/catchments/merge_rasters/shapefiles/'
# opath='/Users/jason/0_dat/catchments/merge_rasters/output/'

# -----------------------------------------------------------------------------  
shapefiles=['/Users/jason/Dropbox/ELA/ancil/mouginot/Mouginot_2019/Greenland_Basins_PS_v1.4.2.shp','/Users/jason/Dropbox/ELA/ancil/mouginot/ICECAPS/Mouginot_2019_Islands/islands.shp']
region_type=['ice_sheet','ice_cap']

def loadtiff(filename):
    dataset = gdal.Open(filename,0)
    ncol = dataset.RasterXSize # x = columns
    nrow = dataset.RasterYSize 
    rasterBand = dataset.GetRasterBand(1)
    GD = rasterBand.ReadAsArray(0,0,ncol,nrow)
    return GD

tmpfile='/tmp/t.csv'
fn='/Users/jason/Dropbox/1km_grid2/thickness_1km_1485x2684.tif' ; thickness = loadtiff(fn) #; thickness/=1e6
fn='/Users/jason/Dropbox/1km_grid2/sectors_IS_1km_1485x2684.tif' ; sectors_IS= loadtiff(fn)
fn='/Users/jason/Dropbox/1km_grid2/sectors_IC_1km_1485x2684.tif' ; sectors_IC= loadtiff(fn)
# v=((sectors_IS==0)&&(sectors_IC>0))
sectors_all=np.zeros((2684,1485))
sectors_accounted=np.zeros((2684,1485))
# sectors_all=sectors_IS

# plt.imshow(sectors_IC,cmap='jet')
plt.imshow(sectors_IS,cmap='jet')

v=np.where(sectors_IS>0)
sectors_all[v]=sectors_IS[v]
print("ice sheet area",len(v[0]),"ice sheet volume",np.nansum(thickness[v])/1e9,np.nansum(thickness[v])/1e9*0.9)
v=(sectors_IS>0)
print(min(sectors_IS[v]))
print(max(sectors_IS[v]))
# print(sectors_IS[v])

v=np.where(sectors_IC>0)
sectors_IC[v]+=397
sectors_all[v]=sectors_IC[v]
print("ice caps area",len(v[0]),"ice cap volume",np.nansum(thickness[v])/1e9,np.nansum(thickness[v])/1e9*0.9)
# x()
v=(sectors_IC>0)
print(min(sectors_IC[v]))
print(max(sectors_IC[v]))

# unaccounted=np.zeros(260)
# unaccounted[:]=1
# x()
du=1
if du:
    outconcept_area_etc_captured=open(tmpfile,'w')
    outconcept_area_etc_captured.write('name,region,gl_type,region_type,area,volume,lat,lon,vol_sum\n')
    
    out_fn_small_ice_caps='/Users/jason/Dropbox/1km_grid2/sector_info_ice_caps_v3.csv'
    out_ice_caps=open(out_fn_small_ice_caps,'w')
    out_ice_caps.write('name,region,gl_type,region_type,area,volume,lat,lon\n')

    # print(sectors_IC[v])
    # x()
    captured_ic=np.zeros((2684,1485))
    captured_is=np.zeros((2684,1485))
    plt.imshow(sectors_all,cmap='jet')
    
    # nj=1485;ni=2684
    # msk=np.zeros((ni,nj))
    # v=np.where(sectors_all>0)
    # msk[v]=1
    # plt.imshow(msk)
    
    # v=np.where(msk>0)
    # print(len(v[0]),np.nansum(thickness[v]))
    
    # v=np.where(thickness>0)
    # print(len(v[0]))
    
    # v=np.where(sectors_all>0)
    # print(len(v[0]),np.nansum(thickness[v])/1e6)
    # x() 
    # print(np.nanmin(thickness),np.nanmax(thickness))
    # -----------------------------------------------------------------------------  loop over 2 region_types
    
    vol_sum=0.
    area_sum=0.
    area_all_ice=1861346.45 # km**2
    captured_ice_area=1818958
    cc=0
    
    for i in range(0,2):
    #    ofile=opath+'sector_list_'+region_type[i]+'.txt'
        print(i)
    #    print(ofile)
        fn=shapefiles[i]
    #    fn=shapefile_path+shapefiles[i]
        final_crs = {'init': 'epsg:3413'}
        BASINS = (gpd.read_file(fn).to_crs(final_crs))
        b=BASINS
        
        df_wgs84=BASINS#.to_crs(epsg=4326)
        geometries=BASINS['geometry']
        df_wgs84_real=BASINS.to_crs(epsg=4326)
    
    #    out=open(ofile,'w')
        msg=''
        if i==0:n=len(BASINS.NAME)
        if i==1:n=len(BASINS.cat)
        for k in range(0,n):
    
            ice_area=df_wgs84.iloc[k].geometry.area/1E6
            if i==0: # ----------------------------------------------- ice sheet
                if BASINS.NAME[k][0:3]!='ICE':
                    # unaccounted[k]=0
                    area_sum+=ice_area
                    v=np.where(k+1==sectors_IS)
                    volumex=np.nansum(thickness[v])
                    vol_sum+=volumex
                    captured_is[v]=1
                    gic = df_wgs84_real.iloc[k] # gic = generic ice cap
                    lonx=gic.geometry.exterior.coords.xy[0][:]
                    latx=gic.geometry.exterior.coords.xy[1][:]
                    
                    coords=np.array([lonx,latx]).T
                    
                    cenlon=gic.geometry.centroid.coords.xy[0][0]
                    cenlat=gic.geometry.centroid.coords.xy[1][0]
                    
                    s1=str(BASINS.NAME[k])+' '
                    msg+=s1
                    # print(BASINS.NAME[k],\
                    #       region_type[i],\
                    #       str("%8.1f"%ice_area).lstrip(),\
                    #       cc+1,\
                    #       str("%8.5f"%cenlon).lstrip(),str("%8.5f"%cenlat).lstrip())
                    cc+=1
                    outconcept_area_etc_captured.write(\
                          BASINS.NAME[k].lstrip()+\
                          ', '+BASINS.SUBREGION1[k].lstrip()+\
                          ', '+BASINS.GL_TYPE[k].lstrip()+\
                          ', '+region_type[i].lstrip()+\
                          ', '+str("%8.1f"%ice_area).lstrip()+\
                          ', '+str("%6.0f"%volumex)+\
                          ', '+str("%8.5f"%cenlat).lstrip()+\
                          ', '+str("%8.5f"%cenlon).lstrip()+\
                          ', '+str("%8.5f"%vol_sum).lstrip()+\
                          ' \n')
            if i==1: # ----------------------------------------------- ice caps
                v=np.where(BASINS.cat[k]==sectors_IC)
                captured_ic[v]=1
                volumex=np.nansum(thickness[v])
    
                area_sum+=ice_area
                gic = df_wgs84_real.iloc[k] # gic = generic ice cap
                lonx=gic.geometry.exterior.coords.xy[0][:]
                latx=gic.geometry.exterior.coords.xy[1][:]
                
                coords=np.array([lonx,latx]).T
                
                cenlon=gic.geometry.centroid.coords.xy[0][0]
                cenlat=gic.geometry.centroid.coords.xy[1][0]
                
                # regions=['SW','CW','NW','NO','NE','CE','SE'] ; n_regions=len(regions)
                regionx='NO'
                if ((cenlat<68.28946)and(cenlon < -44)):regionx='SW'
                if ((cenlat>=68.28946)and(cenlat<72.84333)and(cenlon < -44)):regionx='CW'
                if ((cenlat>=72.84333)and(cenlat<78.09527)and(cenlon < -44)):regionx='NW'
                if ((cenlat>=72.048)and(cenlat<81.52147)and(cenlon > -44)):regionx='NE'
                if ((cenlat>=66.671)and(cenlat<72.048)and(cenlon > -44)):regionx='CE'
                if ((cenlat<66.671)and(cenlon > -44)):reigonx='SE'
                if (ice_area>30):
                    s1=str(BASINS.cat[k])+' '
                    msg+=s1
    #                print(BASINS.cat[k],region_type[i],str("%8.1f"%ice_area).lstrip(),cc+1,cenlon,cenlat)
                    cc+=1
                    outconcept_area_etc_captured.write(\
                          'IC_'+str(BASINS.cat[k]).lstrip()+\
                          ', '+regionx+\
                          ', '+'LT'+\
                          ', '+region_type[i].lstrip()+\
                          ', '+str("%8.1f"%ice_area).lstrip()+\
                          ', '+str("%6.0f"%volumex)+\
                          ', '+str("%8.5f"%cenlat).lstrip()+\
                          ', '+str("%8.5f"%cenlon).lstrip()+\
                          ', '+str("%8.5f"%vol_sum).lstrip()+\
                          ' \n')
    
                if (ice_area<30):
                    out_ice_caps.write(\
                          'IC_'+str(BASINS.cat[k]).lstrip()+\
                          ', '+regionx+\
                          ', '+'LT'+\
                          ', '+region_type[i].lstrip()+\
                          ', '+str("%8.2f"%ice_area).lstrip()+\
                          ', '+str("%6.0f"%volumex)+\
                          ', '+str("%8.5f"%cenlat).lstrip()+\
                          ', '+str("%8.5f"%cenlon).lstrip()+\
                                  ' \n')
    v=np.where(captured_ic==1)
    print("IC",np.sum(captured_ic),np.sum(thickness[v])/1e9)
    v=np.where(captured_is==1)
    print("IS",np.sum(captured_is),np.sum(thickness[v])/1e9)
    print("area_sum",area_sum)
    # plt.imshow(captured_ic+captured_is)
    # plt.imshow(captured_is)
    # x()
    #    out.write(msg)
    
    print("vol_sum",vol_sum)
    
    outconcept_area_etc_captured.close()
    out_ice_caps.close()
    
    
    # print(BASINS.NAME[unaccounted>0])
    # os.system('head '+tmpfile)
    # os.system('tail '+tmpfile)
        
    # print(area_sum)
    # plt.imshow(sectors_all)
    # plt.plot(sectors_all)
    # print(cc,"catchments")
    # x()
du=1
if du:
    # -------------------------------------------------- reread in tmp output
    fn = tmpfile ; df = pd.read_csv(fn)
    print(df.name)
    n_basins=len(df.name)
    # x()
    s=sorted(range(n_basins), key=lambda k: df.area[k])
    s=s[::-1]
    
    # print(df.area[s])
    
    # -------------------------------------------------- read in regions info etc
    fn='/Users/jason/Dropbox/ELA/ancil/mouginot/sectors.txt'
    mouginot = pd.read_csv(fn, delimiter="|")
    n=len(mouginot.name)
    
    out_fn='/Users/jason/Dropbox/1km_grid2/sector_info_v3.csv'
    out_concept=open(out_fn,'w')
    out_concept.write('id,sector_id,name,region,sector_type,gl_type,area,volume,lat,lon\n')

    out_fn_names='/Users/jason/Dropbox/1km_grid2/names_v3x.csv'
    out_names=open(out_fn_names,'w')
#    out_names.write('id,count,name,region,sector_type,gl_type,area,lat,lon,volume\n')
    
    vol_sum=0.
    area_sum=0.
    
    for kk in range(0,n_basins):
    # for kk in range(0,10):
        
        k=s[kk]
        v=(sectors_all==kk+1)
        sectors_accounted[v]=1
        volume=0.
        if np.sum(v)>0:volume=np.nansum(thickness[v])/1e6
        vol_sum+=volume
        area_sum+=df.area[k]

        # print(kk+1,k,df.name[k],len(v[0]),df.area[k],area_sum,volume,vol_sum,np.sum(v))
        print(kk+1,np.sum(v),np.sum(thickness[v])/1e6,vol_sum)
        
        if df.name[k] == 'ICE_CAPS_CE': df.gl_type[k]='LT'
        if df.name[k] == 'STORSTROMMEN': df.gl_type[k]='LT'
        if df.name[k] == 'ICE_CAPS_NE': df.gl_type[k]='LT'
        if df.name[k] == 'USULLUUP_SERMIA': df.gl_type[k]='LT'
        if df.name[k] == 'AB_DRACHMANN_GLETSCHER_L_BISTRUP_BRAE': df.gl_type[k]='LT'
        if df.name[k] == 'NORDENSKIOLD_GLETSCHER': df.gl_type[k]='LT'
        if df.name[k] == 'ICE_CAPS_NO': df.gl_type[k]='LT'
        if df.name[k] == 'SERMEQ-KANGAASARSUUP': df.gl_type[k]='LT'
        if df.name[k] == 'ISUNNGUATA-RUSSELL': df.gl_type[k]='LT'
        if df.name[k] == 'NE_NONAME1': df.gl_type[k]='LT'
        if df.name[k] == 'FREDERIKSHABS-NAKKAASORSUAQ': df.gl_type[k]='LT'
        if df.name[k] == 'DODGE': df.gl_type[k]='LT'
        if df.name[k] == 'WORDIE-VIBEKE': df.gl_type[k]='LT'
        if df.name[k] == 'SORANERBRAEEN-EINAR_MIKKELSEN-HEINKEL-TVEGEGLETSCHER-PASTERZE': df.gl_type[k]='LT'
        if df.name[k] == 'INUPPAAT_QUUAT': df.gl_type[k]='LT'
        if df.name[k] == 'ICE_CAPS_SW': df.gl_type[k]='LT'
        # if df.name[k] == 'IKERTIVAQ_S': df.gl_type[k]='LT'
        if df.name[k] == 'ICE_CAPS_NW': df.gl_type[k]='LT'
        if df.name[k] == 'LEIDY-MARIE-SERMIARSUPALUK': df.gl_type[k]='LT'
        if df.name[k] == 'ADMIRALTY_TREFORK_KRUSBR_BORGJKEL_PONY': df.gl_type[k]='LT'
        if df.name[k] == 'BLSEBR_GAMMEL_HELLERUP_GLETSJER': df.gl_type[k]='LT'
        if df.name[k] == 'WAHLENBERG_VIOLINGLETSJER': df.gl_type[k]='LT'
        if df.name[k] == 'NW_NONAME1': df.gl_type[k]='LT'
        if df.name[k] == 'ICE_CAPS_CW': df.gl_type[k]='LT'
        if df.name[k] == 'KANGILINNGUATA_SERMIA': df.gl_type[k]='LT'
        if df.name[k] == 'NEWMAN_BUGT': df.gl_type[k]='LT'
        if df.name[k] == 'SIORALIK-ARSUK-QIPISAQQU': df.gl_type[k]='LT'
        if df.name[k] == 'ICE_CAPS_SE': df.gl_type[k]='LT'
        # if df.name[k] == 'IKERTIVAQ_N': df.gl_type[k]='LT'
        if df.name[k] == 'AVANNARLEQ_N': df.gl_type[k]='LT'
        if df.name[k] == 'NO_NONAME1': df.gl_type[k]='LT'
        if df.name[k] == 'BUSSEMAND': df.gl_type[k]='LT'
        if df.name[k] == 'SE_NONAME6': df.gl_type[k]='LT'
        if df.name[k] == 'KNUD-RASMUSSEN': df.gl_type[k]='LT'
        if df.name[k] == 'VERHOEFF': df.gl_type[k]='LT'
        if df.name[k] == 'QALERALLIT_SERMIAT': df.gl_type[k]='LT'
        if df.name[k] == 'GEIKIE4': df.gl_type[k]='LT'
        if df.name[k] == 'TUGTO': df.gl_type[k]='LT'
        if df.name[k] == 'ILORLIIT-SERMINNGUAQ': df.gl_type[k]='LT'
        if df.name[k] == 'SE_NONAME7': df.gl_type[k]='LT'
        if df.name[k] == 'GEIKIE5': df.gl_type[k]='LT'
        if df.name[k] == 'UNNAMED_SORGENFRI_W': df.gl_type[k]='LT'
        if df.name[k] == 'SE_NONAME5': df.gl_type[k]='LT'
        if df.name[k] == 'PASSAGE_CHARPENTIER_GLETSCHER': df.gl_type[k]='LT'
        if df.name[k] == 'GEIKIE1': df.gl_type[k]='LT'
        if df.name[k] == 'MOHN_GLETSJER': df.gl_type[k]='LT'
        if df.name[k] == 'NW_NONAME3': df.gl_type[k]='LT'
        if df.name[k] == 'STORM': df.gl_type[k]='LT'
        if df.name[k] == 'SAVISSUAQ_WWW': df.gl_type[k]='LT'
        if df.name[k] == 'HUBBARD': df.gl_type[k]='LT'
        if df.name[k] == 'SE_NONAME8': df.gl_type[k]='LT'
        if df.name[k] == 'SAVISSUAQ_UNNAMED3': df.gl_type[k]='LT'
        if df.name[k] == 'CW_NONAME3': df.gl_type[k]='LT'
        if df.name[k] == 'PITUGFIK': df.gl_type[k]='LT'
        if df.name[k] == 'SE_NONAME9': df.gl_type[k]='LT'
        if df.name[k] == 'KOLVEGLETSJER': df.gl_type[k]='LT'
        if df.name[k] == 'BAMSE': df.gl_type[k]='LT'
        if df.name[k] == 'SUN': df.gl_type[k]='LT'
        if df.name[k] == 'GEIKIE2': df.gl_type[k]='LT'
        if df.name[k] == 'SAVISSUAQ_UNNAMED4': df.gl_type[k]='LT'
        if df.name[k] == 'SAVISSUAQ_WWWWW': df.gl_type[k]='LT'
        if df.name[k] == 'SAVISSUAQ_UNNAMED1': df.gl_type[k]='LT'
        if df.name[k] == 'SIORARSUAQ': df.gl_type[k]='LT'
        if df.name[k] == 'NW_NONAME2': df.gl_type[k]='LT'
        if df.name[k] == 'SE_NONAME4': df.gl_type[k]='LT'
        if df.name[k] == 'SE_NONAME10': df.gl_type[k]='LT'
        if df.name[k] == 'HART': df.gl_type[k]='LT'
        if df.name[k] == 'GABLE_MIRROR': df.gl_type[k]='LT'
        if df.name[k] == 'MEEHAN': df.gl_type[k]='LT'
        if df.name[k] == 'MORRIS_JESUP_W': df.gl_type[k]='LT'
        if df.name[k] == 'SAVISSUAQ_UNNAMED2': df.gl_type[k]='LT'
        if df.name[k] == 'NW_NONAME4': df.gl_type[k]='LT'
        if df.name[k] == 'VERHOEFF_W': df.gl_type[k]='LT'
        if df.name[k] == 'HART_W': df.gl_type[k]='LT'
        if df.name[k] == 'SUN_W': df.gl_type[k]='LT'
        if df.name[k] == 'MEEHAN_W': df.gl_type[k]='LT'
        if df.name[k] == 'SHARP_W': df.gl_type[k]='LT'
        if df.name[k] == 'SAVISSUAQ-HELLAND-YNGVAR_NIELSEN-MOHN-CARLOS': df.gl_type[k]='LT'
        if df.name[k] == 'SORTEBRAE': df.gl_type[k]='LT'
        if df.name[k] == 'SYDBR': df.gl_type[k]='LT'
        if df.name[k] == 'CHARCOT': df.gl_type[k]='LT'
        if df.name[k] == 'NORDFJORD': df.gl_type[k]='LT'
        if df.name[k] == 'UNNAMED_POLARIC_C': df.gl_type[k]='LT'
        
        # m=0.0013774867481259792 ;b=-0.676473084312934
        m=0.0019754323100825088 ;b=-3.2835005362544103

        lo_area_thresh=7000
        if df.area[k]<lo_area_thresh and volume<=1:
            volume=df.area[k]*m+b
            if volume<0.:volume=0.09
        volumex2=volume*1000.
        out_concept.write(\
                          str('%03d'%(kk+1))+\
                          ','+str('%03d'%k)+\
                          ','+df.name[k].lstrip()+\
                          ','+df.region[k].lstrip()+\
                          ','+str(df.gl_type[k]).lstrip()+\
                          ','+df.region_type[k]+\
                          ', '+str("%8.1f"%df.area[k]).lstrip()+\
                          ', '+str("%8.2f"%volumex2).lstrip()+\
                          ', '+str("%8.5f"%df.lat[k]).lstrip()+\
                          ', '+str("%8.5f"%df.lon[k]).lstrip()+\
                          ' \n')
        out_names.write(str(df.name[k]).lstrip()+'\n')
    
    out_concept.close()
    out_names.close()
    # os.system('head '+out_fn)
    # os.system('head '+out_fn_names)

    msg="ice sheet area 1717078 ice sheet volume 2.943092992 2.6487836928\nice caps area 65833 ice cap volume 0.002748594 0.0024737346"
    print(msg)
    print(vol_sum)

    plt.imshow(sectors_accounted,cmap='jet')
    v=np.where(sectors_accounted>0)
    print("vol check",np.nansum(thickness[v]))
    print("ice sheet vol 2942.588")
#out_fn='/Users/jason/Dropbox/1km_grid2/sector_info_TW.csv'
#out_concept=open(out_fn,'w')
#out_concept.write('count,name,region,lat,lon,area,volume\n')
#
#cc=0
#for k in range(0,n_sectors):
#    v=np.where(gl_type[k] == 'TW')
#    if len(v[0]):
#        cc+=1
##        print(cc,str(gl_type[k]),name[k],str("%5.0f"%area[k]))
#        out_concept.write(\
#                      str('%03d'%cc)+\
#                      ','+name[sectorx[k]-1]+\
#                      ','+str(region[sectorx[k]-1])+\
#                      ','+str("%4.1f"%latmean[k])+\
#                      ','+str("%5.1f"%lonmean[k])+\
#                      ', '+str("%5.0f"%area[k])+\
#                      ', '+str("%6.0f"%volume[k])+\
#                      ' \n')
#
#out_concept.close()
#os.system('cat '+out_fn)
#
#
#
#out_fn='/Users/jason/Dropbox/1km_grid2/sector_info_LT.csv'
#out_concept=open(out_fn,'w')
#out_concept.write('count,name,region,lat,lon,area,volume\n')
#
#cc=0
#for k in range(0,n_sectors):
#    v=np.where(gl_type[k] == 'LTx' or gl_type[k] == 'LT')
#    if len(v[0]):
#        cc+=1
##        print(cc,str(gl_type[k]),name[k],str("%5.0f"%area[k]))
#        out_concept.write(\
#                      str('%03d'%cc)+\
#                      ','+name[sectorx[k]-1]+\
#                      ','+str(region[sectorx[k]-1])+\
#                      ','+str("%4.1f"%latmean[k])+\
#                      ','+str("%5.1f"%lonmean[k])+\
#                      ', '+str("%5.0f"%area[k])+\
#                      ', '+str("%6.0f"%volume[k])+\
#                      ' \n')
#
#out_concept.close()
#os.system('cat '+out_fn)