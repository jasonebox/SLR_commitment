pro stitch_mod10a1_not_for_NRT

sf=0.47
ni=2400 & nj=2400
xsize=sf*ni & ysize=sf*nj
set_plot,'x'
device,decomposed=0

plt=1

fday=227
iday=fday-10
;iday=182

iday=271
fday=300

;iday=60
;fday=91
;
;iday=1
;fday=59

;iday=247
;fday=253

;fday=201
;iday=fday-8
;
;iday=90
;fday=121
;
;;iday=152
;;fday=153
;
;iday=134 & fday=144 ; these are day minus 1

;iday=118
;fday=151

imac=0
NRT=0
close,/all

iyear=2000
fyear=2019
n_years=fyear-iyear+1.
year=strtrim(fix(indgen(n_years)+iyear),2)

yearchoice=19

  collection=['5','6']
  colx=1

print,'-------------------------------------------------------------- beginning STITCH_MOD10A1'



gd_id=0

get_500m_grid,lat,lon,elev,maskx,ni,nj,greenland,segments

v=where(greenland and maskx,c_greenland)
c_greenland*=1.
;print,c*0.5^2
;print,c
;stop

ice=where(maskx gt 0)

; extract (lst and QA) data and stitch greenland tiles of MOD10A1 data


for yy=yearchoice,yearchoice do begin
;for yy=15,0,-1 do begin
;for yy=18,18 do begin
;for yy=7,16 do begin

cyear=year(yy)

; initialized the 3x3 tile stitched arrays
gl_albedo=uintarr(7200,7200)
gl_QA=bytarr(7200,7200)

day_previous=0 & year_previous=0
nfiles=0

fn_hdf=''
close,/all

ancpath='~/Dropbox/MOD10A1/NRT/prog/ancil/'

hdfpath='/Volumes/Ice/Jason/MOD10A1/HDF/'
;hdfpath='/Volumes/Tb2/0_dat/MOD10A1/HDF/'
;hdfpath='/users/jason/0_dat/MOD10A1/HDF/'

dir_in=hdfpath+collection(colx)+'/'+cyear+'/'
;dir_in='~/0_dat/MOD10A1/HDF/'+collection(colx)+'/'+cyear+'/'

base_path='/Volumes/LaCie/'
;base_path='/Volumes/Tb2/'
;base_path='/users/jason/'
dir_out=base_path+'0_dat/MOD10A1/500m.00'+collection(colx)+'/'+cyear+'/'

dir_out=base_path+'0_dat/MOD10A1/500m.'+collection(colx)+'/'+cyear+'/'
dir_out_QA=base_path+'0_dat/MOD10A1/500m.'+collection(colx)+'.QA/'+cyear+'/'
dir_out_QA_txt='~/Dropbox/MOD10A1/stats/500m.'+collection(colx)+'.QAtxt/'+cyear+'/'

spawn,'mkdir '+dir_out
spawn,'mkdir '+dir_out_QA
spawn,'mkdir '+dir_out_QA_txt

tmp_path='/tmp/'

;-------------------------------------------
; read the names of the files to stitch together from an ascii file
;
; example of the hdf filename listfile:
;
;MOD11A1.A2009206.h15v02.005.2009209113559.hdf
;MOD11A1.A2009206.h16v00.005.2009209115247.hdf
;MOD11A1.A2009206.h16v01.005.2009209113357.hdf
;MOD11A1.A2009206.h16v02.005.2009209113747.hdf
;MOD11A1.A2009206.h17v00.005.2009209114242.hdf
;MOD11A1.A2009206.h17v01.005.2009209114200.hdf
;MOD11A1.A2009206.h17v02.005.2009209115633.hdf
;-------------------------------------
msg='ls '+dir_in+'*.hdf > '+'/tmp/hdf_'+cyear+'_list.txt'
;print,msg
spawn,msg
hdf_listfile='/tmp/hdf_'+cyear+'_list.txt'
print,hdf_listfile
spawn,'cat '+hdf_listfile
;stop
openr,1,hdf_listfile

; LOOP through the MODIS tiles HDF files
;
ifile=0
while NOT EOF(1) do begin
 temp=''
 readf,1,temp
 ;print,temp
 ;stop
for k=0,50 do begin
cutx=strmid(temp,k,9)
;print,k,' ',cutx
if cutx eq 'MOD10A1.A' then begin
  ;print,k
  char_col=k
endif
endfor
;print,char_col

fn_hdf=strtrim(strmid(temp,char_col,char_col+100),2)
print,'filename hdf ',fn_hdf
;stop
; extract year, day, H, V tile numbers
 
years=fix(strmid(fn_hdf,9,4))
;print,'year ',years
;stop
 if (year_previous eq 0) then year_previous=years
; day=fix(strmid(fn_hdf,13,3))
 day_string=strmid(fn_hdf,13,3)
 day=fix(strmid(fn_hdf,13,3))
;print,'day',day
;print,'day_string',day_string
;stop
 h=fix(strmid(fn_hdf,18,2))
 v=fix(strmid(fn_hdf,21,2))
;--current


;if NRT then begin
;openr,2,'~/Dropbox/MOD10A1/NRT/prog/temp/doy_processess_to.txt'
;fday=0 & readf,2,fday & close,2
;iday=fday-7
;;fday+=1
;endif


;print,day
;print,iday,fday,day
;stop
;print,day,iday+1

if day ge iday and day le fday then begin

;print,'day_previous',day_previous
;if day ne day_previous and day ge iday and day le fday then begin
if day ne day_previous and day ge iday and day le fday then begin
  day_previous=day
;  print,'day_previous',day_previous
;  print,iday,fday

if colx eq 0 then begin
  inv=where(gl_QA eq 1,c)
  if c gt 0 then gl_albedo(inv)=0.
;  print,c
;  stop
endif

if colx eq 1 then begin
  inv=where(gl_QA eq 2 or gl_QA eq 3,c)
  if c gt 0 then gl_albedo(inv)=0.
endif





;loadct,4,/silent
;sf=0.2 & xsize=ni*sf & ysize=nj*sf
;window,0,xsize=xsize,ysize=ysize
;tvscl,congrid(gl_QA,xsize,ysize)

;if day_previous gt 96 then rdpix,congrid(gl_QA,xsize,ysize)



if max(gl_QA) ge 0 then begin
gl_QA(0:2399,0:2399)=255

;wait,0.5
;stop
if plt then begin
	loadct,4,/silent
	!order=1
	sf=0.1 & xsize=ni*sf & ysize=nj*sf
	window,0,xsize=xsize,ysize=ysize
	tvscl,congrid(gl_QA,xsize,ysize)
endif
print,day,iday+1
;print,min(gl_QA),max(gl_QA)
;rdpix,congrid(gl_QA,xsize,ysize)
;help,gl_QA
;stop

;outfile=dir_out_QA+string(year_previous,format='(i4)')+'.'+string(day_previous,format='(i3.3)');+'_500m_MOD10A1_QA_7200x7200_clever.int'
;openw,10,outfile;,/swap_if_little_endian
;print,outfile
;writeu,10,gl_QA
;;spawn,'ls -lF '+outfile
;close,10

;stop
;outfile=dir_out_QA+string(year_previous,format='(i4)')+'.'+string(day_previous,format='(i3.3)')+'.land';+'_500m_MOD10A1_QA_7200x7200_clever.int'
;openw,10,outfile;,/swap_if_little_endian
;writeu,10,gl_land(ice)
;;spawn,'ls -lF '+outfile
;close,10
;sf=0.1
;loadct,4
;ni=7200 & nj=7200
;window,0,xsize=ni*sf,ysize=nj*sf
;tvscl,congrid(gl_QA,ni*sf,nj*sf)
;if max(gl_QA) gt 0 then rdpix,congrid(gl_QA,ni*sf,nj*sf)

;help,gl_QA

;print,max(gl_albedo)
;if day_previous eq 191 then rdpix,congrid(gl_QA,ni*sf,nj*sf)
;stop
v=where(gl_QA eq 239 and greenland,c_ocean)
v=where(gl_QA eq 125 and greenland,c_land)
v=where(gl_QA eq 0 and greenland,c_best); & print,'fraction best',float(c_best)/float(c_ocean)
v=where(gl_QA eq 1 and greenland,c_good) ;& print,'fraction good',float(c_good)/float(c_ocean)
v=where(gl_QA eq 2 and greenland,c_OK) ;& print,'fraction OK',float(c_OK)/float(c_ocean)
v=where(gl_QA eq 3 and greenland,c_poor) ;& print,'fraction poor, unusable or night',float(c)/float(c_ocean)
v=where(gl_QA eq 211 and greenland,c_night) ;& print,'fraction poor, unusable or night',float(c)/float(c_ocean)
v=where(gl_QA eq 255 and greenland,c_unusable) ;& print,'fraction poor, unusable or night',float(c)/float(c_ocean)
v=where(gl_albedo eq 125 and greenland,c_land) ;& print,'fraction poor, unusable or night',float(c)/float(c_ocean)
v=where(gl_albedo eq 150 and greenland,c_cloud) ;& print,'fraction poor, unusable or night',float(c)/float(c_ocean)
v=where(gl_albedo eq 151 and greenland,c_cloud_detected_as_snow) ;& print,'fraction poor, unusable or night',float(c)/float(c_ocean)

outfile=dir_out_QA_txt+string(year_previous,format='(i4)')+'.'+string(day_previous,format='(i3.3)')+'.txt'
openw,11,outfile;,/swap_if_little_endian
printf,11,year(yy),day_previous,c_best,c_good,c_OK,c_poor,c_unusable,c_night,c_ocean,c_land,c_cloud,c_cloud_detected_as_snow,format='(a4,1x,i3,70i10)'
print,year(yy),day_previous,c_best,c_good,c_OK,c_poor,c_unusable,c_night,c_ocean,c_land,c_cloud,format='(a4,1x,i3,70i10)'
;spawn,'ls -lF '+outfile
close,11

if c_best gt 0 then begin
outfile=dir_out+string(year_previous,format='(i4)')+'.'+string(day_previous,format='(i3.3)');+'_500m_MOD10A1_alb_7200x7200_clever.int'
openw,10,outfile;,/swap_if_little_endian
writeu,10,gl_albedo(ice)
;spawn,'ls -lF '+outfile
close,10
endif
endif ; max gt 0

  if fix(day_previous) gt 0 then begin
   day_previous=day
   year_previous=years
   gl_albedo=gl_albedo*0
   gl_QA=byte(gl_QA*0)
endif ; day_previous ne 0

; get new day's year, day, h, v info
;
  years=fix(strmid(fn_hdf,9,4))
  day=fix(strmid(fn_hdf,13,3))
  h=fix(strmid(fn_hdf,18,2))
  v=fix(strmid(fn_hdf,21,2))

  day_previous=day

 endif ; day ne day_previous

 ifile=ifile+1
 print,ifile,' Reading ',dir_in+fn_hdf

 infile=dir_in+fn_hdf
;print,infile
;stop

 fid=EOS_GD_OPEN(infile,/READ) 

 if (fid lt 0) then begin
  print,'EOS_GD_OPEN: failed on ',dir_in+fn_hdf,format='(a,/1x,a)'
  goto, BOTTOM
 endif
; gridname='MODIS_Grid_Daily_500m_Albedo'
 gridname='MOD_Grid_Snow_500m'
 gd_id=eos_gd_attach(fid,gridname) 
;print,gd_id
;print,infile
;stop
 if (gd_id lt 0) then begin
  print,'EOS_GD_ATTACH: failed on ',fn_hdf,format='(a,/1x,a)'
  print,'GridName Searched: ',gridname,format='(a,a)'
  result=eos_query(fn_hdf,fn_hdfinfo)
  print,'File Info...'
  help,/str,fn_hdfinfo
  gd_id=eos_gd_attach(fid,gridname) 
  if (gd_id lt 0) then begin
   print,'EOS_GD_ATTACH: failed on ',fn_hdf,format='(a,/1x,a)'
   print,'GridName Searched: ',gridname,format='(a,a)'
   result=eos_query(fn_hdf,fn_hdfinfo)
   print,'File Info...'
   help,/str,fn_hdfinfo
   result=eos_gd_close(fid); ok
   goto, BOTTOM
  endif
 endif

result=eos_gd_readfield(gd_id,'Snow_Albedo_Daily_Tile',albedo);
gridname='Snow_Spatial_QA'
if colx then gridname='NDSI_Snow_Cover_Basic_QA
result=eos_gd_readfield(gd_id,gridname,QA)
result=eos_gd_readfield(gd_id,'NDSI',NDSI)

;help,gd_id
;help,NDSI
;help,result
;help,qa

;vland=where(ndsi lt 0,c_land)
;qa(vland)=125

if colx then begin
vland=where(albedo eq 125,c_land)
qa(vland)=125
endif

vx=where(albedo eq 150,c_cloud)
qa(vx)=150

;stop
;inv=where(qa gt 100)
;qa(inv)=5
;v=where(qa eq 239,c_ocean)
;v=where(qa eq 125,c_land)
;v=where(qa eq 0,c) & print,'fraction best',float(c)/float(c_ocean)
;v=where(qa eq 1,c) & print,'fraction good',float(c)/float(c_ocean)
;v=where(qa eq 2,c) & print,'fraction OK',float(c)/float(c_ocean)
;v=where(qa eq 3 or aq eq 211 or qa eq 255,c) & print,'fraction poor, unusable or night',float(c)/float(c_ocean)
;
sf=0.47
ni=2400 & nj=2400
xsize=sf*ni & ysize=sf*nj
set_plot,'x'
device,decomposed=0
;loadct,13
;!order=1
;
;print,'c_land',c_land
;if c_land gt 100 then begin
;a=intarr(2400,2400)
;a(v)=1
;window,1,xsize=xsize,ysize=ysize
;  x=congrid(a,xsize,ysize)
;  tvscl,x
;stop
;endif
;window,0,xsize=xsize,ysize=ysize
;  x=congrid(albedo,xsize,ysize)
;  tvscl,x
;  x=congrid(albedo,xsize,ysize)
;  
;  rdpix,x
;  stop

 result=eos_gd_readfield(gd_id,'Snow_Spatial_QA',QA);

; added gd_detach July 2009
; without it, would crash after around 200 files.
 result=eos_gd_detach(gd_id)

; BOTTOM:
; result=eos_gd_close(fid)
result=eos_gd_close(fid)

; move this tile's data to the appropriate stitched array location
;
; is=(h-14)*2400 & ie=is+2399
 is=(h-15)*2400 & ie=is+2399
 js=v*2400 & je=js+2399
; print,h,is,ie,v,js,je
 gl_albedo(is:ie,js:je) = albedo
 gl_QA(is:ie,js:je) = qa

endif

end ; while NOT EOF

;spawn,'/bin/rm ~/0_dat/MOD10A1/500m/'+year(yy)+'/*.000_500m_MOD10A1_alb_7200x7200.img'
; write out the last day
 
;
;print,'Writing ',dir_out+string(year_previous,format='(i4)')+day_string,' files.'

;stop
;msg='/bin/rm '+dir_out+outfile
;print,msg
;spawn,msg

print,'Done ',hdf_listfile

 BOTTOM:
 if gd_id gt 0 then result=eos_gd_close(fid)

endfor ; yy
;stop

;destripe_alb_500m_daily,fday

end
