; ============================================================================================
pro rv
; ============================================================================================
;part 1 ... part 2 is read_MAR_on_basins_output_SMB_AAR_etc.pro

ly='x'

wo=1
plt=0

ni=301 & nj=561

leap_years,l_years

iyear=1999 & fyear=2019
n_years=fyear-iyear+1.
year=strtrim(fix(indgen(n_years)+iyear),2)

cc=0
for yy=0,n_years-1 do begin
  v=where(fix(year(yy)) eq l_years,c)
  n_days=365
  if c then n_days=366
  cc+=n_days
  print,year(yy),c,n_days,cc
endfor
n_days_all=cc+1
;stop



sf=2 ; smaller for smaller display sizes
if plt then begin
	set_plot,'x'
	device,decomposed=0
	xsize=ni*sf & ysize=nj*sf
	window,0,xsize=xsize,ysize=ysize
	!order=1
	loadct,4,/silent
endif

for yx0=0,n_years-2 do begin
for yy=yx0,yx0 do begin

; -------------------------------------------------------------- phase 2
file='/Volumes/LaCie/0_dat/MAR3.10/MARv3.10-daily-ERA5-'+year(yy)+'.nc'
 print,year(yy)
 id=ncdf_open(file)
; fileinq_struct = ncdf_inquire(id)
; nvars = fileinq_struct.nvars
;
; for var = 0,nvars-1 do begin
;   varstruct = ncdf_varinq(ID,var)
;   for attndx = 0, varstruct.natts-2 do begin
;     attname = ncdf_attname(ID,var,attndx)
;     ncdf_attget,ID,var,attname,value
;     print,var,attndx,' ',attname, '     ',string(value)
;     ncdf_varget,ID,var,temp
;     
;     help,temp
;
;   endfor ; attribute loop
; endfor ; variable loop
;stop


  ncdf_varget,ID,7,maskx

  ncdf_varget,ID,10,SMB
;  ncdf_varget,ID,17,SF
;  ncdf_varget,ID,18,RF
;  ncdf_varget,ID,19,SU

inv=where(SMB gt 8000)
smb(inv)=0.

  NCDF_CLOSE,id

!order=0
print,min(maskx)
inv=where(maskx gt 2.1,c)
print,c
maskx(inv)=0.
;tvscl,maskx
;rdpix,maskx
;stop
  n_days=n_elements(smb(0,0,*))
 print,'n_days',n_days

days=strmid(strtrim(string(indgen(366)+1001),2),1,3)

close,/all

sum=fltarr(ni,nj)

for dd=270,n_days-1 do begin
;for dd=0,0 do begin

print,'phase 1 ',year(yy)+'_'+days(dd)

temp=reform(SMB(*,*,dd))
sum+=temp
if plt then tvscl,congrid(sum,ni*sf,nj*sf)
;read,s

	endfor ; dd

close,/all

endfor ; yy

; -------------------------------------------------------------- phase 2

for yy=yx0+1,yx0+1 do begin
;for yy=0,0 do begin
; for yy=12,12 do begin

;  if yy eq 0 then file='/Volumes/LaCie/0_dat/MAR/raw/MARv3.7.1-daily-ERA-Interim-'+year(2)+'.nc'
;  if yy gt 0 then file='/Volumes/LaCie/0_dat/MAR/raw/MARv3.7.1-daily-ERA-Interim-'+year(yy)+'.nc'

file='/Volumes/LaCie/0_dat/MAR3.10/MARv3.10-daily-ERA5-'+year(yy)+'.nc'
 print,year(yy)
 id=ncdf_open(file)
; fileinq_struct = ncdf_inquire(id)
; nvars = fileinq_struct.nvars
;
; for var = 0,nvars-1 do begin
;   varstruct = ncdf_varinq(ID,var)
;   for attndx = 0, varstruct.natts-2 do begin
;     attname = ncdf_attname(ID,var,attndx)
;     ncdf_attget,ID,var,attname,value
;     print,var,attndx,' ',attname, '     ',string(value)
;     ncdf_varget,ID,var,temp
;     
;     help,temp
;
;   endfor ; attribute loop
; endfor ; variable loop
;stop


  ncdf_varget,ID,7,maskx

  ncdf_varget,ID,10,SMB
;  ncdf_varget,ID,17,SF
;  ncdf_varget,ID,18,RF
;  ncdf_varget,ID,19,SU

inv=where(SMB gt 8000)
smb(inv)=0.

  NCDF_CLOSE,id

!order=0
print,min(maskx)
inv=where(maskx gt 2.1,c)
print,c
maskx(inv)=0.
;tvscl,maskx
;rdpix,maskx
;stop
  n_days=n_elements(smb(0,0,*))
 print,'n_days',n_days

days=strmid(strtrim(string(indgen(366)+1001),2),1,3)

close,/all

for dd=0,269 do begin
;for dd=0,0 do begin

print,'phase 2 ',year(yy)+'_'+days(dd)

temp=reform(SMB(*,*,dd))
sum+=temp
if plt then tvscl,congrid(sum,ni*sf,nj*sf)
;read,s

	endfor ; dd

close,/all

endfor ; yy

openw,1,'/Users/jason/Dropbox/MAR/output_MAR_3_10/SMB_'+year(yy-2)+'-'+year(yy-1)+'_301_561.flt'
writeu,1,rotate(sum,7)
close,1

tvscl,congrid(sum,ni*sf,nj*sf)

endfor ; yx0

end




