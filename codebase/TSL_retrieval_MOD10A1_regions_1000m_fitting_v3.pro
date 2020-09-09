pro TSL

close,/all

plt_img=0
prt=1
wo=1
PLT_CURVES=0

k=1 ; PROMICE
k=2 ; polygons

sf=0.4

albedo_deviation=0.025

get_1km_grid3,msk,ni,nj,lat,lon,elevation_array,sectors_IS,sectors_IC

if k eq 1 then begin
	region_type='PROMICE'
	basin_name=['QAS','NUK','KAN','UPE','THU','KPC','SCO','TAS']
	n_basins=8
	min_sample_size=8
	fn='/Users/jason/Dropbox/1km_grid2/PROMICE_sectors.byte'
	sector=bytarr(ni,nj) & openr,1,fn & readu,1,sector & close,1
endif

if k eq 2 then begin
	region_type='polygons'

	min_sample_size=16
fn='/Users/jason/Dropbox/1km_grid2/names_v3.csv'
N_BASINS=file_lines(fn)
print,N_BASINS
name=strarr(N_BASINS)
openr,1,fn & readf,1,name & close,1

endif

	xs=ni & ys=nj
       if plt_img or PLT_CURVES then begin
         xsize=xs*SF
         ysize=ys*SF
         set_plot,'x'
         device,decomposed=0
         xsize=xsize & ysize=ysize
         window,0,xsize=xsize,ysize=ysize
         !order=1
       endif


;for dev=1,2 do begin
for dev=0,0 do begin
devname=['mean','high','low']
if dev eq 2 then alb_at_ELA=0.532-albedo_deviation
if dev eq 0 then alb_at_ELA=0.532
if dev eq 1 then alb_at_ELA=0.532+albedo_deviation

;alb_at_ELA+=0.034

stats_path='~/Dropbox/ELA/stats/TSL/regional/'+region_type+'/'
spawn,'mkdir '+stats_path

close,/all
 

;device,decompose=0
;!order=1
;loadct,4,/silent
;
;xsize=ni*sf & ysize=nj*sf
;window,0,xsize=xsize,ysize=ysize
;x=congrid(sector,xsize,ysize)
;tvscl,x
;

;data = READ_ASCII('/Users/jason/Dropbox/1km_grid2/sector_info_v3.csv', DATA_START=1,header=header,delimeter=",")
;
;help,data
;print,data.name


;print,name[0:3]
;print,name[N_BASINS-4:N_BASINS-1]
;stop

bbx=where(name eq 'NIOGHALVFJERDSFJORDEN')

;inv=where(greenland eq 0)


iyear=2000 & fyear=2019
;iyear=2000 & fyear=2004
n_years=fyear-iyear+1.
year=strtrim(fix(indgen(n_years)+iyear),2)

;inv=where(greenland eq 0)


if plt_img then begin
	window,0,xsize=xsize,ysize=ysize
	device,decompose=0
	!order=1
	loadct,4,/silent
endif

;for bb=0,n_basins-1 do begin
;for bb=0,100 do begin
for bb=103,200 do begin
discrete='c'
;for bb=201,300 do begin
;discrete='b'
;for bb=301,n_basins-1 do begin
;discrete='a'
;for bb=54,54 do begin ; Flade 
;for bb=0,0 do begin ; NIOGHALVFJERDSFJORDEN  
;for bb=3,3 do begin ; PETERMANN_GLETSCHER 

if strmid(name[bb],0,3) ne 'IC_' then sector=sectors_IS
if strmid(name[bb],0,3) eq 'IC_' then sector=sectors_IC

print,name[bb]
if strtrim(name[bb],2) eq 'NIOGHALVFJERDSFJORDEN' then begin
;stop

openr,1,'/Users/jason/Dropbox/1km_grid2/NIOGHALVFJERDSFJORDEN'
gmsk=bytarr(1485,2684) & readu,1,gmsk & close,1
v=where(gmsk,c)
print,c
sector(v)=1

;v=where(sector eq 1)
;msk(v)=10
;ly='x'
;sf=0.4
;
;xsize=ni*sf & ysize=nj*sf
;
;set_plot,'x'
;window,xsize=xsize,ysize=ysize
;device,decomposed=0
;loadct,13,/silent
;!order=1
;
;if ly eq 'x' then begin
;  set_plot,'x'
;  device,DECOMPOSED=0
;  window,0,xsize=xsize,ysize=ysize
;  cs=2.
;  ct=2
;  th=1
;endif
;
;openw,1,'/Users/jason/Dropbox/1km_grid2/NIOGHALVFJERDSFJORDEN_1485x2684.byt'
;writeu,1,msk
;close,1
;
;x=congrid(msk,ni*sf,nj*sf)
;tvscl,x
;stop
endif

if strtrim(name[bb],2) eq 'PETERMANN_GLETSCHER' then begin
;stop

	openr,1,'/Users/jason/Dropbox/1km_grid2/PETERMANN_GLETSCHER'
	gmsk=bytarr(1485,2684) & readu,1,gmsk & close,1
	v=where(gmsk,c)
	print,c
	sector(v)=4
	
;ly='x'
;	sf=0.4
;
;	xsize=ni*sf & ysize=nj*sf
;
;	set_plot,'x'
;	window,xsize=xsize,ysize=ysize
;	device,decomposed=0
;	loadct,13,/silent
;	!order=1
;
;	if ly eq 'x' then begin
;	  set_plot,'x'
;	  device,DECOMPOSED=0
;	  window,0,xsize=xsize,ysize=ysize
;	  cs=2.
;	  ct=2
;	  th=1
;	endif

;	openw,1,'/Users/jason/Dropbox/1km_grid2/PETERMANN_GLETSCHER_1485x2684.byt'
;	writeu,1,msk
;	close,1
;	
;	x=congrid(msk,ni*sf,nj*sf)
;	tvscl,x
;	stop
endif

if name(bb) ne '10019' then begin
print,'basin ',bb,'of ',n_basins-1

;read,s
;stop
;yearchoice=16

;for yy=yearchoice,yearchoice do begin
for yy=0,n_years-1 do begin
;for yy=0,0 do begin
;for yy=5,10 do begin
;for yy=12,12 do begin
;for yy=18,18 do begin
;for yy=17,0,-1 do begin

print,name(bb),' ',dev,devname(dev),' year ',yy,' basin ',bb,'remaining; ',n_basins-bb
;
;path='/Volumes/Ice/Jason/MOD10A1/Greenland_L3_2970_5370/'+year(yy)+'/'
path='/Users/jason/0_dat/Greenland_L3_1km_1485_2685/'+year(yy)+'/'

file=stats_path+name(bb)+'_'+year(yy)+'_ELAs_MOD10A1_1000m_'+devname(dev)+'_v20200320.csv'
if wo then begin
openw,2,file
printf,2,'year,day,snowline_selection_lo,snowline_selection_mid,snowline_selection_hi,aar_lo,aar_mid,aar_hi,meanalb_abl,meanalb_accum,meanalb_all,minalb_abl,tsl_lat,tsl_lon'
endif


a=fltarr(ni,nj)

snowline_selection=fltarr(366)
counts=intarr(366)
  
tmpfile='/tmp/list'+discrete+'.txt'

msg='ls '+path+' >'+tmpfile
spawn,msg
;spawn,'cat /tmp/list.txt'
n=file_lines(tmpfile)
;stop

openr,1,tmpfile
file=strarr(n)
readf,1,file
close,1

days=(strmid(file,5,3)) ; this will compain of type conversion error unless the term after file, is lined up to the 3 digit day of year
int_days=fix(days)

;for dday_index=100,290 do begin
;for dday_index=150,290,3 do begin
for dday_index=110,290 do begin
;for dday_index=190,200 do begin
; for dday_index=228,229 do begin
  
;stop

valid_day=where(int_days eq dday_index,c_valid_day)

snowline_selection=-1.
snowline_max=-1
meanalb_abl=-1.
meanalb_accum=-1.
meanalb_all=-1.
minalb_abl=-1.
minalb_all=-1.
aar=-1.
areax=-1.
lon_at_ela=0.
lat_at_ela=0.

if c_valid_day eq 1 then begin

 
temp=intarr(ni,nj)
fn=path+year(yy)+'_'+days(valid_day(0))+'.tif'
;read_and_scale_grid,fn,temp,prt
	b = READ_TIFF(fn)
;	help,b
	inv = FINITE(b,/NaN) 
	inv=where(inv gt 0,c)
	if c gt 0 then b(inv)=0.
	inv = FINITE(b,/infinity) 
	inv=where(inv gt 0,c)
	if c gt 0 then b(inv)=0.

	temp=congrid(b,1485,2685)
	
inv=where(msk ne 2)
temp(inv)=0.

;help,sector,bb
;print,max(sector)
;inv=where(sector ne bb)
;temp(inv)=0.

;loadct,13,/silent
;tvscl,congrid(sector,xsize,ysize)
;;rdpix,congrid(temp,xsize,ysize)
;stop

a=temp

;v=where(temp gt 0.)
;cumulated(v)=temp(v)
;
;a(ice)=cumulated(*)


      snowline_selection_lo=-1
      snowline_selection_mid=-1
      snowline_selection_hi=-1
      snowline_max=-1
      meanalb_abl=-1.
      meanalb_accum=-1.
      meanalb_all=-1.
      minalb_abl=-1.
      minalb_all=-1.
      aar_lo=-1.
      aar_mid=-1.
      aar_hi=-1.
      areax=-1.
      lon_at_ela=-1
      lat_at_ela=-1
		  lat_mid=-1.
		  lon_mid=-1.
      alb_tolerance=0.03

  all_region=where(sector eq bb+1 and a gt 0.08 and a lt 1,c_all)
  areax=float(c_all)
  abl_region=where(sector eq bb+1 and a gt 0.08 and a lt alb_at_ELA,c_abl)
  accum_region=where(sector eq bb+1 and a gt 0.08 and a lt 1 and a gt alb_at_ELA,c_accum)
  if plt_img then near_ELA=where(sector eq bb+1 and abs(a-alb_at_ELA) lt alb_tolerance,c_abl)

  if c_abl gt 1 then begin
	  meanalb_abl=mean(a(abl_region))
	  minalb_abl=min(a(abl_region))
  endif
  if c_accum gt 1 then meanalb_accum=mean(a(accum_region))
  meanalb_all=mean(a(all_region))
  
 n_elevs=250
 elev_bins=findgen(n_elevs)*10+1.
 counts_elev=intarr(n_elevs)
 means_elev=fltarr(n_elevs)
 means_lat=fltarr(n_elevs)
 means_lon=fltarr(n_elevs)
 temp_alb=a(all_region)
 temp_lat=lat(all_region)
 temp_lon=lon(all_region)
 
 for kkkk=0,n_elevs-1 do begin
 	v=where(abs(elevation_array(all_region)-elev_bins(kkkk)) le 100,c_elev_bins)
 	if c_elev_bins ge 8 then begin
 		counts_elev(kkkk)=c_elev_bins
 		means_elev(kkkk)=mean(temp_alb(v))
 		means_lat(kkkk)=mean(temp_lat(v))
 		means_lon(kkkk)=mean(temp_lon(v))
 	endif
 endfor
  
;------------------------------------------------------------------------
retrieve_TSL,a,bb,sector,elevation_array,c_all,dday_index,alb_at_ela,elev_bins,$
	snowline_selection_lo,aar_lo,snowline_selection_mid,aar_mid,snowline_selection_hi,aar_hi,$
	means_elev,plt_curves,all_region,ALBEDO_DEVIATION,$
	means_lat,means_lon,lat_mid,lon_mid

  elevsx=reform(elevation_array(abl_region))
  latsx=reform(lat(abl_region))
  lonsx=reform(lon(abl_region))
  alb_sample_abl_region=reform(a(abl_region))
  

if wo then begin
	printf,2,$
	year(yy),",",dday_index,",",snowline_selection_lo,",",$
	snowline_selection_mid,",",snowline_selection_hi,",",aar_lo,",",aar_mid,",",aar_hi,",",$
	meanalb_abl,",",meanalb_accum,",",meanalb_all,",",minalb_abl,",",lat_mid,",",lon_mid,$
	format='(a4,a1,i3,a1,3(f6.1,a1),3(f9.6,a1),6(f8.3,a1),f8.3)'
endif

if prt then begin
	print,$
	year(yy),",",dday_index,",",snowline_selection_lo,",",$
	snowline_selection_mid,",",snowline_selection_hi,",",aar_lo,",",aar_mid,",",aar_hi,",",$
	meanalb_abl,",",meanalb_accum,",",meanalb_all,",",minalb_abl,",",lat_mid,",",lon_mid,$
	format='(a4,a1,i3,a1,3(f6.1,a1),3(f9.6,a1),6(f8.3,a1),f8.3)'
endif

        if plt_img then begin
			temp=a
			temp(abl_region)=0.8
			temp(accum_region)=1.2
			temp(near_ELA)=1.4

		   tvscl,congrid(temp,xsize,ysize)
	;;          rdpix,congrid(elev,xsize*4,ysize*4)
	;          ;  print,dday_index
	;          ;    read,s
			   wait,0.4
        endif
        
        if snowline_selection lt 1 then begin
          snowline_selection=-1
          snowline_selection2=-1
          snowline_max=-1
          meanalb_abl=-1.
          meanalb_accum=-1.
          meanalb_all=-1.
          aar=-1.
          aar2=-1.
          areax=-1.
		  lat_mid=-1.
		  lon_mid=-1.
        endif
        
        if aar eq 1. then meanalb_abl=-1.
        if meanalb_abl eq 0. then meanalb_abl=-1.
   

      endif ; c valid day


      if c_valid_day eq 0 then begin
      
      snowline_selection=-1
      snowline_selection2=-1
      snowline_max=-1
      meanalb_abl=-1.
      meanalb_accum=-1.
      meanalb_all=-1.
      aar=-1.
      aar2=-1.
      areax=-1.
      lat_mid=-1.
      lon_mid=-1.

if wo then begin
  printf,2,$
	year(yy),",",dday_index,",",snowline_selection_lo,",",$
	snowline_selection_mid,",",snowline_selection_hi,",",aar_lo,",",aar_mid,",",aar_hi,",",$
	meanalb_abl,",",meanalb_accum,",",meanalb_all,",",minalb_abl,",",lat_mid,",",lon_mid,$
	format='(a4,a1,i3,a1,3(f6.1,a1),3(f9.6,a1),6(f8.3,a1),f8.3)'
endif

if prt then begin
     print,$
	year(yy),",",dday_index,",",snowline_selection_lo,",",$
	snowline_selection_mid,",",snowline_selection_hi,",",aar_lo,",",aar_mid,",",aar_hi,",",$
	meanalb_abl,",",meanalb_accum,",",meanalb_all,",",minalb_abl,",",lat_mid,",",lon_mid,$
	format='(a4,a1,i3,a1,3(f6.1,a1),3(f9.6,a1),6(f8.3,a1),f8.3)'
endif    

endif
        
endfor ; dday_index

  close,2
;        endif ; some basin
  

    endfor ; bb
 endif ; bb

endfor ; yy

endfor ; dev

print,'done'

end

;------------------------------------------------------------------------
pro retrieve_TSL,a,bb,sector,elevation_array,c_all,dday_index,alb_at_ela,elev_bins,$
	snowline_selection_lo,aar_lo,snowline_selection_mid,aar_mid,snowline_selection_hi,aar_hi,$
	means_elev,plt_curves,all_region,ALBEDO_DEVIATION,$
	means_lat,means_lon,lat_mid,lon_mid
; - takes average of 10 m binned elevation where albedo is within 0.02 of recently exposed bare ice albedo

v=where(means_elev gt 0,c_means_elev)

yes_lo=where(abs(means_elev-alb_at_ELA+ALBEDO_DEVIATION) lt ALBEDO_DEVIATION,cyes_lo)
if cyes_lo gt 0 then begin
	snowline_selection_lo=mean(elev_bins(yes_lo))
	accum_region_lo=where(sector eq bb+1 and a gt 0.08 and a lt 1 and elevation_array ge snowline_selection_lo,c_accum_lo)
	aar_lo=float(c_accum_lo)/float(c_all)
endif ; yes_lo

yes_mid=where(abs(means_elev-alb_at_ELA) lt ALBEDO_DEVIATION,cyes_mid)
if cyes_mid gt 0 then begin
	snowline_selection_mid=mean(elev_bins(yes_mid))
	accum_region_mid=where(sector eq bb+1 and a gt 0.08 and a lt 1 and elevation_array ge snowline_selection_mid,c_accum_mid)
	aar_mid=float(c_accum_mid)/float(c_all)
	lat_mid=mean(means_lat(yes_mid))
	lon_mid=mean(means_lon(yes_mid))
endif ; yes_mid

yes_hi=where(abs(means_elev-alb_at_ELA-ALBEDO_DEVIATION) lt ALBEDO_DEVIATION,cyes_hi)
if cyes_hi gt 0 then begin
	snowline_selection_hi=mean(elev_bins(yes_hi))
	accum_region_hi=where(sector eq bb+1 and a gt 0.08 and a lt 1 and elevation_array ge snowline_selection_hi,c_accum_hi)
	aar_hi=float(c_accum_hi)/float(c_all)
endif ; yes_hi

if plt_curves then begin
	loadct,0,/silent
	plot,[0,1],$
		min_value=0.08,line=0,thick=2,background=255,color=0,/nodata,yrange=[0.08,0.9],$
		xrange=[0,1800],title=strtrim(string(dday_index),2)
;		plot,elev_bins(v),yf,min_value=0.08,line=0,thick=2,background=255,color=0,/nodata
		tvlct,0,180,0
		oplot,elevation_array(all_region),a(all_region),psym=1,color=0

		tvlct,0,0,0
		oplot,elev_bins(v),means_elev(v),line=0,thick=2,color=0
	tvlct,0,0,250
	if cyes_lo gt 0 then plots,snowline_selection_lo,alb_at_ela-albedo_deviation,psym=6,color=0,symsize=2,thick=2
	tvlct,0,0,0
	if cyes_mid gt 0 then plots,snowline_selection_mid,alb_at_ela,psym=6,color=0,symsize=2,thick=2
	tvlct,200,0,0
	if cyes_hi gt 0 then plots,snowline_selection_hi,alb_at_ela+albedo_deviation,psym=6,color=0,symsize=2,thick=2
		wait,0.2
;	read,s
endif ; plt curves


;print,aar_mid,c_accum_mid,c_all


end


