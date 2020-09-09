pro regrid_daily_500m_to_pp,fday,plt

;plt=1

;scaling_factor=0.1
;sf=scaling_factor
;ni=7200 & nj=7200
;
;if plt then begin
; set_plot,'x'
; device,decomposed=0
; xsize=ni*scaling_factor & ysize=nj*scaling_factor
; window,0,xsize=xsize,ysize=ysize
; !order=1
;endif


iday=92
;fday=125
;iday=fday-1
collection=['5','6']

cx=1
;for col=1,0,-1 do begin
  for col=cx,cx do begin

dx=1

for destripe=dx,dx do begin
namx=''
if destripe then namx='_d'

SF=0.15

ni=7200 & nj=ni

ni=301 & nj=561 & SF=1.5

;ni=1650 & nj=2750 & SF=0.4

xsize=ni*SF
ysize=nj*SF

if plt then begin
 set_plot,'x'
 device,decomposed=0
 xsize=xsize & ysize=ysize
 window,0,xsize=xsize,ysize=ysize
 !order=1
 loadct,4,/silent
endif

close,/all

iyear=2000 & fyear=2020
n_years=fyear-iyear+1.
year=strtrim(fix(indgen(n_years)+iyear),2)

get_500m_grid,lat,lon,elev,maskx,ni,nj,greenland,segments
print,'done reading 500m grids'

ice=where(maskx gt 0,c_clever)

yx=20
;file='/Users/jason/Dropbox/500m_grid/age_'+year(yy)+'_7200x7200.byt'
;agex=bytarr(c_clever) & openr,1,file & readu,1,agex & close,1
;uncert=where(agex gt 55)

days=strmid(strtrim(string(indgen(366)+1001),2),1,3)

;---------------------------------------------------------------------
;for yy=0,n_years-1 do begin
;  for yy=15,0,-1 do begin
  for yy=yx,yx do begin

  print,ni,nj

  base_path='/Volumes/LaCie/'
;  base_path='/Volumes/Tb2/'
base_path='~/'


  cum=fltarr(c_clever)

  invar=fltarr(7200,7200)
;iday=60 & fday=300 ; these are day minus 1
;iday=91  ; these are day minus 1
;iday=90 & fday=142 ; these are day minus 1 and since this cumulates should start early
;iday=160 & fday=240 ; these are day minus 1 and since this cumulates should start early

  for dd=iday,fday-1 do begin
;    for dd=92,95 do begin

    b=fltarr(ni,nj)
; ----------------------------------------------------------------------------------- stitched and raw
    path=base_path+'0_dat/MOD10A1/500m'+namx+'.'+collection(col)+'/'+year(yy)+'/'
    file=path+year(yy)+'.'+days(dd)
    spawn,'ls -lF '+file
; stop
    flag=1
    on_ioerror,jump
    openr,2,file
    flag=0

    raw=intarr(c_clever)
    readu,2,raw
    close,2
   
   v=where(raw gt 0 and raw lt 10000)
   cum(v)=raw(v)/10000.


;b=intarr(ni,nj)
;b(ice)=raw(*)
;x=congrid(b*0.01,xsize,ysize)
;tvscl,x

    jump: x=!ERROR_STATE.SYS_MSG+' '+file
    if flag then print,x

;cum(uncert)=0

;print,min(cum),max(cum)

du_now=1

if du_now then begin
invar(ice)=cum(*)

fname='/tmp/t'
openw,1,fname & writeu,1,invar & close,1

;opath2=base_path+'0_dat/MOD10A1/5km'+namx+'.'+collection(col)+'/'+year(yy)+'/'
;spawn,'mkdir '+opath2
;ofile=opath2+year(yy)+'.'+days(dd)

ni=301 & nj=561 & to_gpd='~/Dropbox/5km_grid/Polar_MM5_Greenland_x3_5km.gpd'
opath2=base_path+'0_dat/MOD10A1/5km'+namx+'.'+collection(col)+'/'+year(yy)+'/'
print,opath2
;stop
regrid_me,ni,nj,to_gpd,opath2,ofile,plt,sf,year,yy,days,dd


du_1km=0

if du_1km then begin
  opath2='/Volumes/Ice/Jason/MOD10A1/1000m'+namx+'.'+collection(col)+'/'+year(yy)+'/'
  spawn,'mkdir '+opath2
  ni=1650 & nj=2750 & to_gpd='~/Dropbox/1000m_grid/Glea1000.txt'
  regrid_me,ni,nj,to_gpd,opath2,ofile,plt,sf,year,yy,days,dd
endif

endif ; du_now

endfor ; dd

endfor ; yy

endfor ; destripe

endfor ; col

make_cube,fday,plt

end

pro regrid_me,ni,nj,to_gpd,opath2,ofile,plt,sf,year,yy,days,dd

  ofile=opath2+year(yy)+'.'+days(dd)

  regridpath='/usr/local/ms2gt/bin/'
  
  from_gpd='~/Dropbox/500m_grid/sinus_h15h17_v00v02_500m.gpd'

  fname='/tmp/t'

  msg=regridpath+'regrid -F -i -0. '+from_gpd+' '+to_gpd+' '+fname+' '+ofile
  print,msg
  spawn,msg
  
  a=fltarr(ni,nj) & openr,1,ofile & readu,1,a & close,1
  
  spawn,'ls -lF '+ofile
  print,min(a),max(a)
  if plt then tvscl,congrid(a,ni*sf,nj*sf)
  ;rdpix,congrid(invar,ni*sf,nj*sf)
  ;stop

end